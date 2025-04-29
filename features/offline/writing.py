from pynput.keyboard import Controller

################################################

def type(input):
    keyboard = Controller()   
    keyboard.type(input)