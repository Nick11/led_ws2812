import serial
from time import sleep
class LedServer:
    """
    Protocol:
    All messages consist of 5 bytes.
    ControllByte AddressByte1 AddressByte2 RedByte GreenByte BlueByte
    ControllByte: Can have to following values
        0: set the color of a single led
        'n': return number of LEDs connected
        'a': set all LEDs to same color
    AddressByte 1 and 2: contain the LEDs address incase a single LED is manipulated
    Red/Green/BlueByte: contain an integer 0-255 specifying each color channels intensity (RGB)
    """
    led_count = -1
    serial_connection = None
    serial_port_name = None

    def __init__(self, serial_port_name):
        self.serial_port_name = serial_port_name
    def run(self):
        with self.connect() as ser:
            #ser.readline()
            print(ser.readline())  # Read the newest output from the Arduin
            #b = bytearray()
            #b.append(0xFF0000)
            #sleep(1)  # Delay for one tenth of a second
            #ser.write(b'\x00\x00\x00\xff\x00')
            #ser.write(str.encode("test"))
            #sleep(10) # Delay for one tenth of a second
            #print(ser.readline())

            while True:
                user_in = input()
                if user_in == 'n':
                    self.get_led_count()
                elif user_in.startswith('a'):
                    split_input = user_in.split(' ')
                    if not len(split_input) == 4:
                        continue
                    red = int(split_input[1])
                    green = int(split_input[2])
                    blue = int(split_input[3])
                    self.set_all(red, green, blue)

                else:
                    split_input = user_in.split(' ')
                    if not len(split_input) == 4:
                        continue
                    address = int(split_input[0])
                    red = split_input[1]
                    green = int(split_input[2])
                    blue = int(split_input[3])
                    answ = self.set_one(address=address, red=red, green=green, blue=blue)
                    print(answ)
        #      counter +=1
        #      chara = chr(counter)
        #      ser.write(str.encode(chara))
        #      #ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
              #print(ser.readline()) # Read the newest output from the Arduino
          #  sleep(.1) # Delay for one tenth of a second
        #      if counter == 255:
        #         counter = 32

    def connect(self):
        failed_attempts = 0
        try:
            self.serial_connection = serial.Serial(self.serial_port_name, 9600)  # Establish the connection on a specific port
            print('connected')
            return self.serial_connection
        except serial.serialutil.SerialException:
            failed_attempts = failed_attempts+1
            print('failed to connect')
            if failed_attempts>100:
                print('no connection possible')
                return
            sleep(0.5)
            self.connect()

    def get_led_count(self):
        msg = 'n'.encode() + b'\x00\x00\x00\x00\x00'
        self.serial_connection.write(msg)
        number_leds = ord(self.serial_connection.read())
        self.led_count = number_leds
        print(number_leds)
        return number_leds

    def set_one(self, address, red, green, blue):
        address = (int(address)).to_bytes(2, byteorder='big')
        red = bytes([int(red)])
        green = bytes([int(green)])
        blue = bytes([int(blue)])
        msg = b'\x00' + address + red + green + blue
        self.serial_connection.write(msg)
        answer = self.serial_connection.readline()
        return answer

    def set_all(self, red, green, blue):
        red = bytes([int(red)])
        green = bytes([int(green)])
        blue = bytes([int(blue)])
        msg = 'a'.encode() + b'\x00\x00' + red + green + blue
        self.serial_connection.write(msg)
        answer = self.serial_connection.readline()
        return answer


if __name__ == '__main__':
    server = LedServer(serial_port_name = '/dev/cu.usbmodem1411')
    server.run()
