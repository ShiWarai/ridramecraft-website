from flask import request
import json
import requests

from math import sqrt

from Website import NeuralNetwork

def generate_json(last_colors, predicted_color):

    # Подготовим данные
    last_colors_set = list()
    for i in range(len(last_colors)):
        last_colors_set.append([i, last_colors[i]])

    message = json.dumps({"last_colors_set": last_colors_set, "predicted_color": predicted_color})
    return message

def load_json(json_dump):
    return json.loads(json_dump)

def check_recapcha(response, remoteip):
    return json.loads(requests.post('https://www.google.com/recaptcha/api/siteverify', data=dict(
        secret="6Lc8_o4bAAAAAK0ki07kq82mxAEOTosPX8e15Oa_",
        response=response.get('g-recaptcha-response'),
        remoteip=remoteip
    )).text)['success']

# Для случайного цвета
from random import randint, seed
from datetime import datetime

seed(datetime.now())

def get_random_color():

    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)

    return [red, green, blue]

def rgb_to_hex(color):
    return '#%02x%02x%02x' % (color[0], color[1], color[2])

def get_predicted_color(colors_set):

    colors = NeuralNetwork.predict(colors_set)
    colors_n = len(colors)

    # Получаем средне квадратичное значение
    final_color = [0, 0 ,0]
    for rgb_color in colors:
        for i in range(3):
            final_color[i] += (rgb_color[i]*rgb_color[i])

    for i in range(3):
        final_color[i] = round(sqrt(final_color[i]/colors_n))

    final_color = rgb_to_hex(final_color)

    return final_color

def generate_colors(n = 3):
    '''
    n - кол-во цветов, которое требуется сгенерировать
    '''
    colors = list()
    colors_set = list()

    # Первый цвет - случайный
    colors.append(rgb_to_hex(get_random_color()))
    for i in range(n-1):
        colors.append(get_predicted_color(colors))

    for i in range(n):
        colors_set.append([i, colors[i]])

    return colors_set

def add_colors(new_color, colors_set):
    NeuralNetwork.add_colors_db(new_color, colors_set)

def validate_hash(hash):
    if hash != "":
        return True
    else:
        return False

class BaseCaptchaForm():

    def validate(self):
        success = False
        try:
            if 'g-recaptcha-response' in request.form:
                success = check_recapcha(
                    request.form,
                    request.remote_addr
                )
        except:
            pass
        return success
