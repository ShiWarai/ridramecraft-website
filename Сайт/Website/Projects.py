from os import path
from flask_babel import lazy_gettext as _l

from Website import DatabaseClasses

class Project:
    def __init__(self, project_object):
        self.name = project_object.name
        self.description = _l(project_object.description)
        self.image = path.join("projects", "static", project_object.image)
        if project_object.link[:2] == "$$" and project_object.link[-2:] == "$$":
            self.link = project_object.link[2:-2]
        else:
            self.link = "location.href='%s';" % (project_object.link)

# Глобальные функции
def getProjectsList():
    try:
        projects_list = DatabaseClasses.Project.query.order_by(DatabaseClasses.Project.name).all()
        return projects_list
    except:
        return list()

def getProject(project_name):
    project_obj = DatabaseClasses.Project.query.filter_by(name=project_name).first()

    try:
        project = Project(project_obj)
    except AttributeError:
        return None

    return project

def getProjects(sql_project_objects):
    projects_list = list()

    for obj in sql_project_objects:
        projects_list.append(Project(obj))

    return projects_list


def createProject(name, description=None, image="not_found.jpg", link=None):
    try:
        DatabaseClasses.database.session.add(
            DatabaseClasses.Project(
                name=name,
                description=description,
                image=image,
                link=link
            )
        )

        DatabaseClasses.database.session.commit()
        return True
    except:
        DatabaseClasses.database.session.rollback()
        return False

def editProject(name, description=None, image=None, link=None):
    try:
        project = DatabaseClasses.Project.query.get(name)
        if description != None:
            project.description = description
        if image != None:
            project.image = image
        if link != None:
            project.link = link
        DatabaseClasses.database.session.commit()
    except:
        print("Ошибка с изменением")

def removeProject(name):
    try:
        DatabaseClasses.Project.query.filter_by(name = name).delete()
        DatabaseClasses.database.session.commit()
    except:
        print("Ошибка с удалением")

# editProject("Screen Translator", "Простой экранный переводчик на основе сторонних библиотек.","screen_translator.jpg","https://github.com/ShiWarai/ScreenTranslator")
# editProject("Color Combinations", "Нейронная сеть для определения цветовых комбинаций.","color_combinations.jpg","/projects/color_combinations")
# editProject("Quinkokolobicky.net", "Настольное приложение с полностью реализованной серверно-клиентской частью. Клиент и сервер написаны на разных языках.","quinkokolobicky.jpg","https://yadi.sk/d/0rzx7UJRT36Oxw")
# editProject("Sasha's Shop", "Мое первое приложение, написанное на C++ с использованием Windows Forms. Осуществляет учёт товаров на складе.","sasha_shop.jpg","https://yadi.sk/d/BVUT6MuLZxUiBQ")
# editProject("Neural Network C++", "Нейронная сеть для распознавания чисел, написанная как проект по дисциплине процедурного программирования в университете. Было запрещено использовать ООП.","neural_network.jpg","https://github.com/ShiWarai/neural-network")
# createProject("Test project", description="Нажми на меня", image="project_test.png", link="$$showProject('Test project')$$")
# editProject("Робот спасатель", description="Робот спасатель, основанный на базе конструктора Lego, с применением машинного зрения на базе Raspberry Pi 4b (1GB).", image="robot.jpg", link="$$showProject('Робот спасатель')$$")