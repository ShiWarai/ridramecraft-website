#!/yadisk/Проекты/ridramecraft-website/Сайт/.venv/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path, listdir
from bs4 import BeautifulSoup

main_path = sys.argv[1]
template_path = path.join(main_path, "templates")

def getDirsList(path):
    return listdir(path)

def getFilesList(directory):
    return [path.join(directory, fileName) for fileName in getDirsList(directory) if path.isfile(path.join(directory, fileName))]

for template in getFilesList(template_path):
    file_data = str()
    with open(template, 'r', encoding='utf-8') as file:
        file_data = file.read()

    if not (path.basename(template) in ["layout.html", "project.html"]):
        # добавление расширения шаблона flask
        file_data = "{% extends \"layout.html\" %}\n" + file_data

        # установка блока скриптов
        soup = BeautifulSoup(file_data, 'html.parser')

        scripts = soup.findAll('script')
        last_script = scripts[len(scripts) - 1]
        first_script = last_script.findPrevious()

        while first_script.findPrevious().name == 'script':
            first_script = first_script.findPrevious()

        first_script.insert_before("{% block scripts %}")
        last_script.insert_after("{% endblock scripts %}")

    else:
        soup = BeautifulSoup(file_data, 'html.parser')

        # установка блока скриптов
        scripts = soup.findAll('script')
        last_script = scripts[len(scripts) - 1]
        first_script = last_script.findPrevious()

        while first_script.findPrevious().name == 'script':
            first_script = first_script.findPrevious()

        first_script.insert_before("{% block scripts %}")
        last_script.insert_after("{% endblock scripts %}")

    with open('test', 'wb') as file:
        file.write(soup.prettify("utf-8"))
