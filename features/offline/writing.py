from pynput.keyboard import Controller

################################################

class Writing():
    def __init__(self, output):
        self.keyboard = Controller()   
        self.keyboard.type(output)