from LedSerialConnector import LedSerialConnector
from utils.Color import Color
from time import sleep
from collections import UserList
import numpy as np

class WS2811(UserList):
    DefaultColor = Color.Black()
    editing = False
    dirty_leds = set()
    leds = None
    def __init__(self, led_connector):
        self.led_connector = led_connector
        led_count = led_connector.get_led_count()
        #init leds and make it change color
        self.set_leds(np.zeros((led_count, 3)))

    def __getitem__(self, index):
        return self.leds[index]

    def __setitem__(self, key, value):
        if isinstance(value, Color):
            value = value.rgb_components()
        if not (self.leds[key] == value).all():
            self.leds[key] = value

            if self.editing:
                self.dirty_leds.add(key)
            else:
                self.set_one(address=key, color=Color(rgb_components=value) )

    def __len__(self):
        return len(self.leds)

    def __add__(self, other):
        if not np.shape(other) == self.shape():
            return
        new_leds = self.leds + other
        #cap addition
        new_leds[new_leds > 255] = 255
        new_leds[new_leds < 0] = 0

        self.set_leds(new_leds)
        return self

    def shape(self):
        return np.shape(self.leds)

    def set_leds(self, leds):
        #force into valid interval
        leds[leds > 255] = 255
        leds[leds < 0] = 0

        #initial case is different. just set it
        if self.leds is None:
            self.leds = leds
            change_leds = {i: Color(rgb_components=leds[i]) for i in range(len(leds))}
            self.set_burst(change_leds)
            return

        if not np.size(leds) == np.size(self.leds):
            print('invalid dimension when setting leds. was ',np.size(leds), ' instead of ',np.size(self.leds))
            return

        abs_diff = np.abs(leds - self.leds)
        changed_rows,_ = np.nonzero(abs_diff)
        change_leds = {i:Color(rgb_components=leds[i]) for i in changed_rows}
        self.set_burst(change_leds)

        self.leds = leds

    def set_all(self, color):
        self.led_connector.set_all(red=color.red, green=color.green, blue=color.blue)

    def set_one(self, address, color):
        self.led_connector.set_one(address=address, red=color.red, green=color.green, blue=color.blue)

    def set_burst(self, address_color_dict):
        self.led_connector.set_burst(address_color_dict)

    def begin(self):
        self.editing = True

    def end(self):
        changed_leds = {key:Color(rgb_components=self.leds[key]) for key in self.dirty_leds }
        self.dirty_leds = set()
        self.set_burst(changed_leds)
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

    def random(self, scale=2, wait=0.05, red_variation=1, green_variation=1, blue_variation=1 ):
        for i in range(300):
            red_rand = np.random.uniform(low=-scale*red_variation, high=scale*red_variation, size=(len(self),1))
            green_rand = np.random.uniform(low=-scale * green_variation, high=scale * green_variation, size=(len(self), 1))
            blue_rand = np.random.uniform(low=-scale * blue_variation, high=scale * blue_variation, size=(len(self), 1))
            rand = np.column_stack((red_rand, green_rand, blue_rand))
            #other = np.random.normal(loc=0, scale=scale, size=ws.shape())
            ws + rand
            sleep(wait)

    def ocean(self):
        green_rand = np.random.uniform(low=100, high=200, size=(len(self)))
        blue_rand = np.random.uniform(low=100, high=200, size=(len(self)))
        start_values = np.zeros(self.shape())
        start_values[:,1] = green_rand
        start_values[:,2] = blue_rand
        ws.set_leds(start_values)
        self.random(scale=1, wait=0.1, red_variation=0, green_variation=0.1,blue_variation=0.2)

if __name__ == '__main__':
    with LedSerialConnector() as connector:
        ws = WS2811(led_connector=connector)
        # ws.begin()
        # for i in range(0,len(ws),2):
        #     ws[i] = Color.Ocean()
        # ws.end()
        leng = len(ws)
        ws.ocean()

        #ws.ping_pong()
        sleep(1000)