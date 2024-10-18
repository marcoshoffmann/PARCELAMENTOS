from os import listdir, path
from resources.PathManager import PathManager

class Files:
    def __init__(self) -> None:
        self.pathmanager = PathManager()
        self.pathmanager.verify_paths()
        self.federal = [f'{self.pathmanager.paths_types[0]}\\{file}' for file in listdir(self.pathmanager.paths_types[0])]
        self.estadual = [f'{self.pathmanager.paths_types[1]}\\{file}' for file in listdir(self.pathmanager.paths_types[1])]
        self.municipal = [f'{self.pathmanager.paths_types[2]}\\{file}' for file in listdir(self.pathmanager.paths_types[2])]
    
    def serch_types(self) -> list:
        all_types = [f'{path_type}\\{file}' for path_type in self.pathmanager.paths_types for file in listdir(path_type)]
        return all_types
