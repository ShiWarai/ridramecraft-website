#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ

from Website import app
from waitress import serve

if __name__ == '__main__':
    if not app.debug:
        HOST = '0.0.0.0'  # Слушаем на всех интерфейсах для Docker
        PORT = int(environ.get('SERVER_PORT', '80'))
        print(f"Starting server on {HOST}:{PORT}")
        serve(app, host=HOST, port=PORT, threads=8)
    else:
        HOST = '0.0.0.0'  # Слушаем на всех интерфейсах для Docker
        PORT = int(environ.get('SERVER_PORT', '8000'))
        print(f"Starting server in debug mode on {HOST}:{PORT}")
        app.run(HOST, PORT, debug=True)
