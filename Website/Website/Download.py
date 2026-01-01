# -*- coding: utf-8 -*-

from Website import  Repository
from os import path

class DownloadableFile:

    name = "None"
    fullname = ""
    extension = ""
    download_path = ""
    description = "Not found"

    def __init__(self, name):
        self.fullname = name
        self.name = name[0:name.rfind('.')]
        self.extension = name[name.rfind('.'):]
        self.download_path = path.join(Repository.downloads_directory, name)
        if not path.isfile(self.download_path):
            raise Exception("Такого файла не существует")

        # Получение данных из файла
        self.description = getDownloadDescription(self.name)

# Глобальные функции
def getFilesList():
    try:
        directory = Repository.downloads_directory
        filesList = [fileName for fileName in Repository.getDirsList(directory) if
                     (path.isfile(path.join(directory, fileName)) and fileName[0:2] != '__')]
        return filesList
    except:
        return list()


def getDownloadDescription(file_name):
    result = "Not found"

    try:
        file_description = open(path.join(Repository.downloads_directory, "__description_" + file_name + ".desc"), 'r', encoding="utf-8")
        result = file_description.readline()

        file_description.close()
    except:
        pass

    return result
