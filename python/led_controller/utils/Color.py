import numpy as np

class Color:

    def __init__(self, red=None, green=None, blue=None,rgb_components=None):
        self.red = 0
        self.green = 0
        self.blue = 0
        if not rgb_components is None:
            self.red = int(rgb_components[0])
            self.green = int(rgb_components[1])
            self.blue = int(rgb_components[2])
        if not red == None:
            self.red = int(red)
        if not green == None:
            self.green = int(green)
        if not blue == None:
            self.blue = int(blue)

    def __str__(self):
        return 'color rgb: '+str(self.red)+','+str(self.green)+','+str(self.blue)

    def rgb_components(self):
        return np.array([self.red, self.green, self.blue], dtype=int)

    @classmethod
    def Red(cls):
        return Color(255, 0, 0)

    @classmethod
    def Black(cls):
        return Color(0, 0, 0)

    @classmethod
    def Ocean(cls):
        return Color(0, 150, 255)