from re import search as re_search

led_color = "#000000"

class WrongLedData(BaseException):
    pass

def set_led_data(color):
    global led_color
    if re_search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
        led_color = color
    else:
        raise WrongLedData("Wrong led color")


def get_led_data():
    global led_color
    return {'color': led_color}
