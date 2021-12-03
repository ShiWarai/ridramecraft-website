from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS
from secrets import token_hex
import argparse

from Website import Repository  # Константы расположения проекта

# Аргументы
parser = argparse.ArgumentParser(description='Server launcher')
parser.add_argument('-m', '--mode', metavar='mode', type=str,
                    help="mode of running server (debug/release)", default='release')
parser.add_argument('-k', '--api-key', required=True, metavar='api_key', type=str,
                    help="api-key for Yandex Cloud translation")

args = parser.parse_args()

# App
app = Flask(__name__, static_folder='assets')
app.config['UPLOAD_FOLDER'] = Repository.downloads_directory
app.config['SQLALCHEMY_BINDS'] = {'main' : "sqlite:///main.db", 'color_combinations' : "sqlite:///colors-sets.db" }
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ["ru", "en"]  # First language - source
app.config['DEBUG'] = (args.mode == "debug")
app.secret_key = token_hex(16)
app.api_key = args.api_key

babel = Babel(app)
babel_js = BabelJS(app, view_path="/assets/js/_lang.js")

from Website import DatabaseClasses
from Website import Translator

import Website.Views
