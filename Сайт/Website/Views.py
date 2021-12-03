# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, send_from_directory, abort, request, redirect, session
from math import ceil, floor

from flask_babel import _

from Website import app, babel
from Website import Download
from Website import Projects
from Website import ColorCombinations

websiteName = "RidrameCraft"
hostName = "ridramecraft.ru"

def render_base_template(pageName="home.html"):
    return render_template(
        pageName,
        websiteName = websiteName,
        hostName = hostName,
        year = datetime.now().year
    )

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def home():
    return render_base_template("home.html")

@app.route('/home')
def go_home():
    return redirect('/')

# Для доступа к проектам
@app.route('/projects/<path:path>')
def send_project_assets(path):
    return send_from_directory('projects', path)

# Для доступа к проектам
@app.route('/project/<string:project_name>')
def send_project(project_name):
    project = Projects.getProject(project_name)

    if not project:
        print("No such project!")
        return render_template("project_error.html", project_name=project_name)

    return render_template("project.html", project_name=project.name)

@app.route('/contacts')
def contacts():
    return render_base_template("contacts.html")

@app.route('/downloads/list', methods=['GET'])
def downloads_count():

    files_list = list()
    # Заполняем массив ссылок
    for file_name in Download.getFilesList():

        file_data = dict()
        file = Download.DownloadableFile(file_name)

        file_data.update({"name": file.name})
        file_data.update({"extension": file.extension})
        file_data.update({"description": file.description})
        file_data.update({"link": file_name})

        files_list.append(file_data)

    # Формируем границы отображаемого списка загрузок
    files_n = len(files_list)

    return {'list': files_list, 'count': files_n}

@app.route('/downloads')
def downloads():
    files_n = downloads_count()['count']

    return render_template(
        "downloads.html",
        isEmpty=files_n == 0,
        websiteName=websiteName,
        hostName=hostName,
        year=datetime.now().year
    )

@app.route('/projects')
def projects():

    projects = Projects.getProjects(Projects.getProjectsList()) # Объекты проектов, которые содержат всю нужную информацию

    return render_template(
        "projects.html",
        projects = projects,
        websiteName=websiteName,
        hostName=hostName,
        year=datetime.now().year
    )

@app.route('/downloads/<filename>')
def download_file(filename):
    if filename[0:2] == '__':
        return 'Bad request', 400
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/projects/color_combinations')
def colors_combinations(train_color_amount = 3, mode = 0):

    train_color_amount = int(request.args.get('color_amount') or train_color_amount)
    mode = int(request.args.get('mode') or mode)

    colors_set = ColorCombinations.generate_colors(train_color_amount) # Создаём набор цветов

    last_colors_set = list()
    for i in range(train_color_amount):
        last_colors_set.append([i,"#ffffff"])

    prediction_enabled = False
    predicted_color = "#ffffff"
    if 'prediction_enabled' in session:
        prediction_enabled = True if session['prediction_enabled'] == "true" else False
        if 'last_prediction_set_size' in session:
            if int(session['last_prediction_set_size']) == train_color_amount:
                last_prediction_set = ColorCombinations.load_json(session['last_prediction_set'])
                last_colors_set = last_prediction_set['last_colors_set']
                predicted_color = last_prediction_set['predicted_color'] if last_prediction_set[
                                                                                'predicted_color'] != "null" else predicted_color

    return render_template(
        "color_combinations.html",
        websiteName=websiteName,
        hostName=hostName,
        year=datetime.now().year,
        colors_set=colors_set,
        colors_n=train_color_amount,
        mode=mode,
        last_colors_set=last_colors_set,
        predicted_color=predicted_color,
        prediction_enabled=prediction_enabled)

@app.route('/projects/color_combinations/train', methods=['POST'])
def train_system():

    # reCaptcha
    form = ColorCombinations.BaseCaptchaForm()

    color = request.form['color']
    color_amount = request.form['color_amount']

    base_colors_set = list()
    for i in range(int(color_amount)):
        base_colors_set.append(request.form['base-color-'+str(i)])

    if form.validate():
        print("Success: ", base_colors_set, color)
        ColorCombinations.add_colors(color, base_colors_set)

        session['prediction_enabled'] = "true"
        return redirect("/projects/color_combinations?color_amount="+color_amount)
    else:
        print("Fail!")
        session['prediction_enabled'] = "true"
        return redirect("/projects/color_combinations?color_amount="+color_amount)

@app.route('/projects/color_combinations/predict', methods=['POST'])
def predict_color():

    color_amount = request.form['color_amount']

    colors_set = list()
    for i in range(int(color_amount)):
        colors_set.append(request.form['color-'+str(i)])

    prediction_enabled = False
    if 'prediction_enabled' in session:
        if session['prediction_enabled'] == "true":
            prediction_enabled = True

    if prediction_enabled:
        print("Prediction for:", colors_set)
        generated_color = ColorCombinations.get_predicted_color(colors_set)
        print("Prediction:", generated_color)

        session['last_prediction_set'] = ColorCombinations.generate_json(colors_set, generated_color)
        session['last_prediction_set_size'] = color_amount

        return redirect("/projects/color_combinations?mode=1&color_amount="+color_amount)
    else:
        abort(403, description="Access denied!")