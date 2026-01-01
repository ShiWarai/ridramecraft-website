from keras import models
from keras import layers
from keras.models import load_model

import numpy as np

from Website.DatabaseClasses import database, ColorCombination
from Website.Repository import fileExist, model_path, removeModel

model = None
history_dict = None

def add_colors_db(new_color, colors_set):

    database.session.add(
       ColorCombination(
            color_1 = new_color,
            color_2 = colors_set[0],
            color_3 = colors_set[1] if len(colors_set) > 1 else None,
            color_4 = colors_set[2] if len(colors_set) > 2 else None,
            color_5 = colors_set[3] if len(colors_set) > 3 else None,
            size = len(colors_set) + 1
        )
    )
    database.session.commit()

    # Удаляем модель (что приведёт к обновлению базы при следующем запуске)
    # print("Модель удалена: ", removeModel())

def get_colors(sets_size):
    return ColorCombination.query.filter_by(size = sets_size).all()

# Функции для чтения данных

def hex_to_rgb(h):
    h = h[1:]
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (r, g, b)


def build_model_shade():
    model = models.Sequential()
    model.add(layers.Dense(1028, activation='relu',input_shape = [3,]))
    model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    model.add(layers.Dense(3, activation='relu'))
    model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae'])
    return model

def build_model():
    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu',input_shape = [3,]))
    model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.4, noise_shape=None, seed=None))
    model.add(layers.Dense(3, activation='relu'))
    model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae'])
    return model

def shuffle_in_unison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)


def build_and_fit():

    input_dataset_train = list()
    output_dataset_train = list()

    color_combination_objects = get_colors(2)
    for color_comb_obj in color_combination_objects:
        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))
        # Меняем цвета местами, так как "цвет_1" <=> "цвет_2"
        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

    color_combination_objects = get_colors(3)
    for color_comb_obj in color_combination_objects:
        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

    color_combination_objects = get_colors(4)
    for color_comb_obj in color_combination_objects:
        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_4))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_4))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

    color_combination_objects = get_colors(5)
    for color_comb_obj in color_combination_objects:
        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_2))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_3))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_4))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_4))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_5))

        input_dataset_train.append(hex_to_rgb(color_comb_obj.color_5))
        output_dataset_train.append(hex_to_rgb(color_comb_obj.color_1))

    train_size = round(3 / 4 * len(input_dataset_train))
    train_data = np.array([input_dataset_train[:train_size], output_dataset_train[:train_size]], dtype="int")
    validation_data = np.array([input_dataset_train[train_size:], output_dataset_train[train_size:]], dtype="int")

    print("Размер тренировочного набора:", train_size)
    print("Размер проверочного набора:", len(input_dataset_train) - train_size)


    shuffle_in_unison(train_data[0], train_data[1])
    shuffle_in_unison(validation_data[0], validation_data[1])
    model = build_model()
    return [model, model.fit(train_data[0],train_data[1],epochs = 50, batch_size = 16, validation_data = (validation_data[0],validation_data[1])).history]


if not fileExist(model_path):
    print("Train the model...")
    generated_model = build_and_fit()
    model = generated_model[0]
    history_dict = generated_model[1]
    del generated_model

    model.save(model_path)
    print("Model has been saved")
else:
    model = load_model(model_path)
    print("Model has been loaded")


def post_processing(colors):
    '''
    for i in range(len(colors)):
        colors[i] = hsv_to_rgb(colors[i])
    '''

    processed_colors = list()
    for color in colors:
        red = color[0]
        green = color[1]
        blue = color[2]

        # Увеличим доминирующий цвет
        dominant_color = colors.argmax()
        passive_color = colors.argmax()

        if dominant_color == 0:
            red *= 1.2
        elif dominant_color == 1:
            green *= 1.2
        elif dominant_color == 2:
            blue *= 1.2

        if passive_color == 0:
            red *= 0.8
        elif passive_color == 1:
            green *= 0.8
        elif passive_color == 2:
            blue *= 0.8

        red = min(round(red), 255)
        green = min(round(green), 255)
        blue = min(round(blue), 255)

        processed_colors.append([red, green, blue])

    return processed_colors

def predict(hex_colors_set):
    rgb_colors_set = list()
    for color in hex_colors_set:
        rgb_colors_set.append(hex_to_rgb(color))

    prediction = post_processing(model.predict(rgb_colors_set))

    return prediction