from resources.FilesManager import FilesManager
from resources.PdfData import PdfData

if __name__ == '__main__':
    filesmanager = FilesManager()
    pdfdata = PdfData()

    filesmanager.copy_all_pdfs()
    filesmanager.move_all_pdfs()
    pdfdata.verify_all_cpf_cnpjs()
    pdfdata.concat_data()
    filesmanager.files_to_client()
