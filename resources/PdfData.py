from os import getenv
from dotenv import load_dotenv
from json import loads
import pdfplumber as plb
from resources.Files import Files
from re import sub
from resources.Pdf import Pdf
from use_cases.MongoDB import MongoDB
from loguru import logger
from resources.PathManager import PathManager
load_dotenv()

class PdfData:
    def __init__(self) -> None:
        self.pathmanager = PathManager()
        self.pdf = Pdf()
        self.files = Files()
        self.dict_marks = loads(getenv("DICT_MARKS"))
        self.files_by_mark, self.dict_pdfs, self.inscricoes = {key: [] for key in self.dict_marks}, {}, {}
        self.mongodb = MongoDB(collection=getenv('COLLECTION'))
        for data in self.mongodb.consult(filter={}):
            if not data['IE'].__eq__(""): self.inscricoes[data['IE']] = data['CPF/CNPJ']
            if not data['IM'].__eq__(""): self.inscricoes[data['IM']] = data['CPF/CNPJ']
            if not data['IPTU'].__eq__(""): self.inscricoes[data['IPTU']] = data['CPF/CNPJ']
    
    def read_pdf(self, file: str) -> list:
        lines = []
        with plb.open(path_or_fp=file) as pdf_open:
            for page in range(len(pdf_open.pages)):
                extracted_data = pdf_open.pages[page].extract_text()
                lines.extend(extracted_data.split("\n"))
        return lines
    
    def verify_pdf(self, file: str) -> str:
        data = self.read_pdf(file=file)
        for line in data:
            if line.__contains__(getenv('LINE_RS')): return 'ESTADUAL'
            if line.__contains__(getenv('LINE_POA')): return 'MUNICIPAL'
        return 'FEDERAL'
    
    def verify_format(self, line) -> str:
        if len(line).__ge__(16):
            if line[2].__eq__('.') and line[6].__eq__('.') and line[10].__eq__('/') and line[15].__eq__('-'): return sub("\D", "", line.split(" ")[0])
            if line[3].__eq__('.') and line[7].__eq__('.') and line[11].__eq__('-'): return sub("\D", "", line.split(" ")[0])
            if len(line).__ge__(26):
                if line[12].__eq__('.') and line[16].__eq__('.') and line[20].__eq__('/') and line[25].__eq__('-'):
                    return sub("\D", "", line.split(" ")[1])
        if len(line).__ge__(62):
            if line[48].__eq__('.') and line[52].__eq__('.') and line[56].__eq__('/') and line[61].__eq__('-'):
                return sub("\D", "", line.split(" ")[-1])
        if line.__contains__(getenv('LINE_CNPJ1')): return sub("\D", "", line.split(" ")[-1])
        if line.__contains__(getenv('LINE_CNPJ2')): return self.inscricoes[sub("\D", "", line.split(" - ")[1])]
        if line.__contains__(getenv('LINE_CNPJ3')):
            if self.inscricoes.__contains__(str(sub("\D", "", line.split(" ")[2]))): return self.inscricoes[str(sub("\D", "", line.split(" ")[2]))]
    
    def verify_cpf_cnpj(self, file: str) -> str:
        data = self.read_pdf(file=file)
        for line in data:
            cnpj = self.verify_format(line.upper())
            if cnpj is not None: return cnpj

    def verify_all_cpf_cnpjs(self) -> None:
        for file in self.files.serch_types():
            if not file.__contains__('MERGED_'):
                cpf_cnpj = self.verify_cpf_cnpj(file)
                if not self.dict_pdfs.__contains__(cpf_cnpj):
                    self.dict_pdfs[cpf_cnpj] = [file]
                else:
                    self.dict_pdfs[cpf_cnpj].append(file)
                logger.info(f'CPF_CNPJ: {cpf_cnpj} | {file}')

    def concat_data(self) -> None:
        for key, values in self.dict_pdfs.items():
            self.pdf.concat_files_federal(cpf_cnpj=key, files=values)
            self.pdf.concat_files_estadual(cpf_cnpj=key, files=values)
            self.pdf.concat_files_municipal(cpf_cnpj=key, files=values)
