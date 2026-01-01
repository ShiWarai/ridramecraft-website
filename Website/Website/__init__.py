from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS
from secrets import token_hex
from os import environ

from Website import Repository  # Константы расположения проекта

# Получение аргументов из переменных окружения или аргументов командной строки
import sys
mode = environ.get('MODE', 'release')
api_key = environ.get('API_KEY', None)

# Поддержка аргументов командной строки для обратной совместимости
if '--mode' in sys.argv or '-m' in sys.argv:
    import argparse
    parser = argparse.ArgumentParser(description='Server launcher')
    parser.add_argument('-m', '--mode', metavar='mode', type=str,
                        help="mode of running server (debug/release)", default=mode)
    parser.add_argument('-k', '--api-key', metavar='api_key', type=str,
                        help="api-key for Yandex Cloud translation", default=api_key)
    args = parser.parse_args()
    mode = args.mode
    if args.api_key:
        api_key = args.api_key

if not api_key:
    raise ValueError("API_KEY must be provided either as environment variable or --api-key argument")

# App
app = Flask(__name__, static_folder='assets')
app.config['UPLOAD_FOLDER'] = Repository.downloads_directory
app.config['SQLALCHEMY_BINDS'] = {
    'projects': f"sqlite:///{Repository.databases_directory}/projects.db",
    'color_combinations': f"sqlite:///{Repository.databases_directory}/colors-sets.db"
}
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ["ru", "en"]  # First language - source
app.config['DEBUG'] = (mode == "debug")
app.secret_key = token_hex(16)
app.api_key = api_key

babel = Babel(app)
babel_js = BabelJS(app, view_path="/assets/js/_lang.js")

from Website import DatabaseClasses
from Website import Translator

import Website.Views
