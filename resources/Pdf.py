from PyPDF2 import PdfWriter
from resources.PathManager import PathManager

class Pdf:
    def __init__(self) -> None:
        self.pathmanager = PathManager()

    def concat_files_federal(self, cpf_cnpj: str, files: list) -> None:
        merger_federal = PdfWriter()
        output_path = f'{self.pathmanager.path_pdfs}\\' + 'FEDERAL' + f'\\MERGED_FEDERAL_{cpf_cnpj}_.pdf'  # Usar ./ ao invés de .\
        for file in files:
            if file.__contains__('\\FEDERAL\\'):
                merger_federal.append(file)
                merger_federal.write(output_path)
        merger_federal.close()

    def concat_files_estadual(self, cpf_cnpj: str, files: list) -> None:
        merger_estadual = PdfWriter()
        output_path = f'{self.pathmanager.path_pdfs}\\' + 'ESTADUAL' + f'\\MERGED_ESTADUAL_{cpf_cnpj}_.pdf'  # Usar ./ ao invés de .\
        for file in files:
            if file.__contains__('\\ESTADUAL\\'):
                merger_estadual.append(file)
                merger_estadual.write(output_path)
        merger_estadual.close()

    def concat_files_municipal(self, cpf_cnpj: str, files: list) -> None:
        merger_municipal = PdfWriter()
        output_path = f'{self.pathmanager.path_pdfs}\\' + 'MUNICIPAL' + f'\\MERGED_MUNICIPAL_{cpf_cnpj}_.pdf'  # Usar ./ ao invés de .\
        for file in files:
            if file.__contains__('\\MUNICIPAL\\'):
                merger_municipal.append(file)
                merger_municipal.write(output_path)
        merger_municipal.close()
