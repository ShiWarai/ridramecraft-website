#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ

from Website import app
from waitress import serve

if __name__ == '__main__':
    if not app.debug:
        HOST = "185.253.217.111"
        try:
            PORT = 80
        except ValueError:
            PORT = int(environ.get('SERVER_PORT', '80'))

        serve(app, host=HOST, port=PORT, threads=8)
    else:
        from subprocess import check_output as cmd

        HOST = cmd("hostname -I", shell=True).decode().strip()  # IP-адрес в локальной сети
        try:
            PORT = 8000
        except ValueError:
            PORT = int(environ.get('SERVER_PORT', '8000'))

        app.run(HOST, PORT, debug=True)
