from resources.TimeConsult import TimeConsult
from dotenv import load_dotenv
from os import getenv, listdir, walk, remove, path as _path
from shutil import copy, move, rmtree
from resources.PdfData import PdfData
from resources.PathManager import PathManager
load_dotenv()

class FilesManager:
    def __init__(self) -> None:
        self.pathmanager = PathManager()
        self.timeconsult = TimeConsult()
        self.pdfdata = PdfData()
        self.path_target = getenv('PATH_TARGET').format(year=self.timeconsult.actual_year, month=self.timeconsult.actual_month)
        self.path_clients = getenv('PATH_CLIENTS')
        self.path_xlsx = getenv('PATH_XLSX')
        self.dir_clients_cnpj = {empresa.split(" - ")[-1]: empresa for empresa in listdir(self.path_clients) if _path.isdir(f'{self.path_clients}\\{empresa}')}
        self.dir_clients_id = {empresa.split(" - ")[0]: empresa for empresa in listdir(self.path_clients) if _path.isdir(f'{self.path_clients}\\{empresa}')}
        if self.path_target: self.paths = [f'{self.path_target}\\{path}' for path in listdir(self.path_target) if _path.isdir(f'{self.path_target}\\{path}')]
        self.path_new_pdfs = self.pathmanager.path_pdfs
        self.federal = [f'{self.pathmanager.paths_types[0]}\\{file}' for file in listdir(self.pathmanager.paths_types[0])]
        self.estadual = [f'{self.pathmanager.paths_types[1]}\\{file}' for file in listdir(self.pathmanager.paths_types[1])]
        self.municipal = [f'{self.pathmanager.paths_types[2]}\\{file}' for file in listdir(self.pathmanager.paths_types[2])]

    def __clean_path__(self) -> None:
        [rmtree(f'{self.pathmanager.path_pdfs}\\{path}') if _path.isdir(f'{self.pathmanager.path_pdfs}\\{path}') else remove(f'{self.pathmanager.path_pdfs}\\{path}') for path in listdir(self.pathmanager.path_pdfs)]
    
    def __clean_path_after__(self) -> None:
        [remove(f'{self.pathmanager.path_pdfs}\\{path}\\{file}') for path in listdir(self.pathmanager.path_pdfs) for file in listdir(f'{self.pathmanager.path_pdfs}\\{path}') if not file.startswith('MERGED_')]
    
    def copy_all_pdfs(self) -> None:
        self.__clean_path__()
        self.pathmanager.verify_paths()
        for root, dirs, files in walk(self.path_target):
            for file in files:
                if file.lower().endswith('.pdf'):
                    copy(f'{root}\\{file}', f'{self.path_new_pdfs}\\' + root.split("\\")[-1] + f'_{file}')

    def move_pdf(self, file: str) -> None:
        tipo = self.pdfdata.verify_pdf(file=file)
        move(f'{file}', f'{self.path_new_pdfs}\\{tipo}\\' + file.split("\\")[-1])

    def move_all_pdfs(self) -> None:
        [self.move_pdf(f'{self.pathmanager.path_pdfs}\\{file}') for file in listdir(self.pathmanager.path_pdfs) if file.lower().endswith('.pdf')]

    def __verify_client__(self, cpf_cnpj: str) -> bool:
        if self.dir_clients_cnpj.__contains__(cpf_cnpj): return True

    def __verify_file__(self, file: str) -> bool:
        if file.startswith('MERGED_') and not file.__eq__('None.pdf'):
            if self.__verify_client__(cpf_cnpj=file.split("_")[-2]):
                if _path.exists(f'{self.path_clients}\\{self.dir_clients_cnpj[file.split("_")[-2]]}\\{self.timeconsult.actual_year}\\{self.timeconsult.competence}\\PARCELAMENTOS\\{file}'): remove(f'{self.path_clients}\\{self.dir_clients_cnpj[file.split("_")[-2]]}\\{self.timeconsult.actual_year}\\{self.timeconsult.competence}\\PARCELAMENTOS\\{file}')
                return True

    def files_to_client(self) -> None:
        for path in self.pathmanager.paths_types:
            for file in listdir(path):
                if self.__verify_file__(file=file): [move(src=f'{path}\\{file}', dst=f'{self.path_clients}\\{self.dir_clients_cnpj[file.split("_")[-2]]}\\{self.timeconsult.actual_year}\\{self.timeconsult.competence}\\PARCELAMENTOS')]
        self.__clean_path_after__()
