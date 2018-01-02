from LedSerialConnector import LedSerialConnector
from utils.Color import Color
from time import sleep
from collections import UserList

class WS2811(UserList):
    DefaultColor = Color.Black()
    editing = False

    def __init__(self, led_connector):
        self.led_connector = led_connector
        led_count = led_connector.get_led_count()
        self.set_leds( {i:self.DefaultColor for i in range(led_count)})

    def __getitem__(self, index):
        return self.leds[index]

    def __setitem__(self, key, value):
        if not self.leds[key] == value:
            self.leds[key] = value

            if not self.editing:
                self.set_one(address=key, color=value)

    def __len__(self):
        return len(self.leds)

    def set_leds(self, leds):
        self.leds = leds
        self.set_burst(self.leds)

    def set_all(self, color):
        self.led_connector.set_all(red=color.red, green=color.green, blue=color.blue)

    def set_one(self, address, color):
        self.led_connector.set_one(address=address, red=color.red, green=color.green, blue=color.blue)

    def set_burst(self, address_color_dict):
        self.led_connector.set_burst(address_color_dict)

    def begin(self):
        self.editing = True

    def end(self):
        self.set_burst(self.leds)
        self.editing = False

    def move_single_led(self, step=1, color=Color.Red()):
        old_state = self.leds.copy()

        domain = range(0, len(self), step)
        if step < 0:
            domain = range(len(self)-1, 0, step)

        for domain_index in range(1, len(domain)):
            index = domain[domain_index]
            last_index = domain[domain_index-1]
            ws[last_index] = old_state[last_index]
            ws[index] = color
            #sleep(0.02)

    def ping_pong(self):
        direction = -1
        while True:
            self.move_single_led(step=direction)
            direction = direction * (-1)

if __name__ == '__main__':
    with LedSerialConnector() as connector:
        ws = WS2811(led_connector=connector)
        ws.ping_pong()
        sleep(1000)