from os import path
from flask_babel import lazy_gettext as _l

from Website import DatabaseClasses

class Project:
    def __init__(self, project_object):

        self.name = project_object.name
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

# createProject("Screen Translator",
#               description="Простой экранный переводчик на основе сторонних библиотек.",
#               images="screen_translator.jpg",
#               link="/downloads/ScreenTranslator.zip",
#               is_full=True,
#               full_description="Простой экранный переводчик на основе сторонних библиотек. Основной задачей данного приложения была помощь в работе с иностранными ресурсами и их быстрым переводом.",
#               source_link="/downloads/ScreenTranslator.zip",
#               github_link="https://github.com/ShiWarai/ScreenTranslator")
#
# createProject("Color Combinations",
#             description="Нейронная сеть для определения цветовых комбинаций.",
#             images="color_combinations_1.jpg color_combinations_2.jpg",
#             link="/projects/color_combinations",
#             is_full=True,
#             is_app=True,
#             full_description="Нейронная сеть для определения цветовых комбинаций. Приложение обладает такими функциями как формирование базы цветовых сочетаний, пополняемых с помощью пользователя, а также генерация цветовых сочетаний посредством предварительной обработки нейронной сетью БД.",
#             source_link=None,
#             github_link=None)
#
# createProject("Quinkokolobicky.net",
#             description="Настольное приложение с полностью реализованной серверно-клиентской частью. Клиент и сервер написаны на разных языках.",
#             images="quinkokolobicky.jpg",
#             link="https://yadi.sk/d/0rzx7UJRT36Oxw",
#             is_full=True,
#             full_description="Настольное приложение с полностью реализованной серверно-клиентской частью. Клиент и сервер написаны на разных языках.",
#             source_link="https://yadi.sk/d/0rzx7UJRT36Oxw",
#             github_link="https://github.com/ShiWarai/quinkokolobicky")
#
# createProject("Sasha's Shop",
#             description="Мое первое приложение, написанное на C++ с использованием Windows Forms. Осуществляет учёт товаров на складе.",
#             images="sasha_shop.jpg",
#             link="https://yadi.sk/d/BVUT6MuLZxUiBQ",
#             is_full=True,
#             full_description="Мое первое приложение, написанное на C++ с использованием Windows Forms. Осуществляет учёт товаров на складе. Главной целью являлось решение прикладной задачи после изучения языка C++.",
#             source_link="https://yadi.sk/d/BVUT6MuLZxUiBQ",
#             github_link=None)
#
# createProject("Neural Network C++",
#             description="Нейронная сеть для распознавания чисел, написанная как проект по дисциплине процедурного программирования в университете. Было запрещено использовать ООП.",
#             images="neural_network.jpg not_found.jpg",
#             link="https://disk.yandex.ru/d/-WL5VsIEGNKfJA",
#             is_full=True,
#             full_description="Нейронная сеть для распознавания чисел, написанная как проект по дисциплине процедурного программирования в университете. Было запрещено использовать ООП. Полный код можно получить по ссылке ниже, а также на GitHub.",
#             source_link="https://disk.yandex.ru/d/-WL5VsIEGNKfJA",
#             github_link="https://github.com/ShiWarai/neural-network")