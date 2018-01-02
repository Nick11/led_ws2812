class Color:

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return 'color rgb: '+str(self.red)+','+str(self.green)+','+str(self.blue)

    @classmethod
    def Red(cls):
        return Color(255, 0, 0)

    @classmethod
    def Black(cls):
        return Color(0, 0, 0)