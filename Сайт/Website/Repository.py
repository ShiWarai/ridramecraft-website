from os import path, listdir, curdir, remove

root_dir = path.abspath(curdir)
downloads_directory = path.join(root_dir, "download")
projects_directory = path.join(root_dir,"Website", "projects")
templates_directory = path.join(root_dir,"Website", "templates")
static_directory = path.join(root_dir,"Website", "assets")
model_path = path.join(root_dir, "Website", "model.h5")
pot_file_path = path.join(root_dir, "req_translation.pot")

def get_po_file_path(lang):
    return path.join(root_dir, "Website", "translations", lang, "LC_MESSAGES", "messages.po")

def get_mo_file_path(lang):
    return path.join(root_dir, "Website", "translations", lang, "LC_MESSAGES", "messages.mo")

def removeModel():
    try:
        remove(model_path)
        return True
    except:
        return False

def getDirsList(path):
    return listdir(path)

def getFilesList(directory):
    return [path.join(directory,fileName) for fileName in getDirsList(directory) if path.isfile(path.join(directory, fileName))]

def fileExist(file_path):
    if path.isfile(file_path):
        return True
    else:
        return False