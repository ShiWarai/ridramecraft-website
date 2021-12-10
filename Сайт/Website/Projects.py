from os import path
from flask_babel import lazy_gettext as _l

from Website import DatabaseClasses


class Project:
    def __init__(self, project_object):
        self.id = project_object.id
        self.name = _l(project_object.name)
        self.description = _l(project_object.description)

        self.tags = list()
        for tag in project_object.tags.split(';'):
            self.tags.append({'name': tag})

        self.image = path.join("projects", "static", "images", project_object.images.split(';')[0])

        self.images = list()
        if project_object.images:
            for image in project_object.images.split(';'):
                self.images.append(path.join("projects", "static", "images", image))

        self.link = project_object.link
        self.is_full = project_object.is_full
        self.is_app = project_object.is_app
        self.full_description = _l(project_object.full_description)

        self.videos = list()
        if project_object.videos:
            for video in project_object.videos.split(';'):
                self.videos.append(path.join("projects", "static", "videos", video))

        self.source_link = project_object.source_link
        self.github_link = project_object.github_link

def getProject(id):
    project_obj = DatabaseClasses.Project.query.filter_by(id=id).first()

    try:
        project = Project(project_obj)
    except AttributeError:
        return None

    return project


def getProjects():

    sql_project_objects = list()
    try:
        sql_project_objects = DatabaseClasses.Project.query.order_by(DatabaseClasses.Project.name).all()
    except:
        pass

    projects_list = list()
    for obj in sql_project_objects:
        projects_list.append(Project(obj))

    return projects_list
