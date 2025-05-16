#program to contain more logic for the wavelength game

import random, string

rooms = {}

def create_room():
    code = get_code()
    while code in rooms:
        code = get_code()
    rooms[code] = {
        "players": [],
        "answers": []
    }
    return code

def get_code(length=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))