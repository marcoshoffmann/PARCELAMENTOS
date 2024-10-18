from os import getenv, path, mkdir
from dotenv import load_dotenv
load_dotenv()

class PathManager:
    def __init__(self) -> None:
        self.path_pdfs = getenv("PATH_PDFS")
        self.paths_types = getenv("PATHS_TYPES").split(";")

    def verify_paths(self) -> None:
        if not path.exists(self.path_pdfs): mkdir(self.path_pdfs)
        [mkdir(_path) for _path in self.paths_types if not path.exists(_path)]
