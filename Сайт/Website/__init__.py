from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS
from secrets import token_hex
from sys import argv

from Website import Repository # Константы расположения проекта

app = Flask(__name__, static_folder='assets')
app.config['UPLOAD_FOLDER'] = Repository.downloads_directory
app.config['SQLALCHEMY_BINDS'] = {'main' : "sqlite:///main.db", 'color_combinations' : "sqlite:///colors-sets.db" }
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ["en", "ru"] # First language - source
app.config['DEBUG'] = argv[1].split('--')[1] == "release" if False else True
app.secret_key = token_hex(16)

babel = Babel(app)
babel_js = BabelJS(app, view_path="/assets/js/_lang.js")

from Website import DatabaseClasses
from Website import Translator

import Website.Views
