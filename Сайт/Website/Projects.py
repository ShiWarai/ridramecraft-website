from os import path
from flask_babel import lazy_gettext as _l

from Website import DatabaseClasses


class Project:
    def __init__(self, project_object):
        self.id = project_object.id
        self.name = _l(project_object.name)
        self.description = _l(project_object.description)
        self.image = path.join("projects", "static", project_object.images.split(' ')[0])

        self.images = []
        for image in project_object.images.split(' '):
            self.images.append(path.join("projects", "static", image))

        self.link = project_object.link
        self.is_full = project_object.is_full
        self.is_app = project_object.is_app
        self.full_description = _l(project_object.full_description)
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


def createProject(name,
                  description=None,
                  images="not_found.jpg",
                  link=None,
                  is_full=False,
                  is_app=False,
                  full_description=None,
                  source_link=None,
                  github_link=None):
    try:
        DatabaseClasses.database.session.add(
            DatabaseClasses.Project(
                name=name,
                description=description,
                images=images,
                link=link,
                is_full=is_full,
                is_app=is_app,
                full_description=full_description,
                source_link=source_link,
                github_link=github_link
            )
        )

        DatabaseClasses.database.session.commit()
        return True
    except:
        DatabaseClasses.database.session.rollback()
        return False


def editProject(name,
                description=None,
                images=None,
                link=None,
                is_full=False,
                is_app=False,
                full_description=None,
                source_link=None,
                github_link=None):
    try:
        project = DatabaseClasses.Project.query.get(name)
        if description != None:
            project.description = description
        if images != None:
            project.images = images
        if link != None:
            project.link = link

        project.is_full = is_full
        if is_full:
            if full_description != None:
                project.full_description = full_description
            if source_link != None:
                project.source_link = source_link
            if github_link != None:
                project.github_link = github_link
            project.is_app = is_app

        DatabaseClasses.database.session.commit()
    except:
        print("Ошибка с изменением")


def removeProject(name):
    try:
        DatabaseClasses.Project.query.filter_by(name=name).delete()
        DatabaseClasses.database.session.commit()
    except:
        print("Ошибка с удалением")
