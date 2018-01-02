import serial,sys
from time import sleep
import serial.tools.list_ports
from ClosableSerialConnection import ClosableSerialConnection

class LedSerialConnector:
    """
    Protocol:
    All messages consist of 5 bytes.
    ControllByte AddressByte1 AddressByte2 RedByte GreenByte BlueByte
    ControllByte: Can have to following values
        0: set the color of a single led
        'n': return number of LEDs connected
        'a': set all LEDs to same color
        'd': disconnects the arduino
    AddressByte 1 and 2: contain the LEDs address incase a single LED is manipulated
    Red/Green/BlueByte: contain an integer 0-255 specifying each color channels intensity (RGB)
    """
    led_count = -1
    serial_connection = None
    BAUD_RATE = 9600
    TIMEOUT = 1 #in seconds

    def __init__(self, serial_port_name):
        self.serial_port_name = serial_port_name

    def __init__(self):
        """
        If no port name is given, try to find it
        """
        (connection, port_name) = self.find_port()
        if connection == None:
            print('No valid devise found. Aborting')
            sys.exit(1)
        else:
            self.serial_connection = connection
            self.serial_port_name = port_name

    def get_connection(self):
        if self.serial_connection == None:
            self.serial_connection = self.connect(self.serial_port_name)
            self.serial_connection.readline()
        return self.serial_connection

    def run(self):
        with self.get_connection() as ser:
            #ser.readline()
            #print(ser.readline())  # Read the newest output from the Arduin
            #b = bytearray()
            #b.append(0xFF0000)
            #sleep(1)  # Delay for one tenth of a second
            #ser.write(b'\x00\x00\x00\xff\x00')
            #ser.write(str.encode("test"))
            #sleep(10) # Delay for one tenth of a second
            #print(ser.readline())

            while True:
                user_in = input().strip()
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
                elif user_in.startswith('d'): #disconnect
                    self.disconnect()
                    break
                elif user_in[0].isdigit():
                    split_input = user_in.split(' ')
                    if not len(split_input) == 4:
                        continue
                    address = int(split_input[0])
                    red = split_input[1]
                    green = int(split_input[2])
                    blue = int(split_input[3])
                    answ = self.set_one(address=address, red=red, green=green, blue=blue)
                    print(answ)
                else:
                    print('invalid command')
        #      counter +=1
        #      chara = chr(counter)
        #      ser.write(str.encode(chara))
        #      #ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
              #print(ser.readline()) # Read the newest output from the Arduino
          #  sleep(.1) # Delay for one tenth of a second
        #      if counter == 255:
        #         counter = 32

    def connect(self, serial_port_name):
        failed_attempts = 0
        try:
            connection = ClosableSerialConnection(serial_port_name, baudrate=self.BAUD_RATE)  # Establish the connection on a specific port

            print('connected')
            return connection
        except serial.serialutil.SerialException:
            failed_attempts = failed_attempts+1
            print('failed to connect')
            if failed_attempts>100:
                print('no connection possible')
                return
            sleep(0.5)
            self.connect(serial_port_name=serial_port_name)

    def disconnect(self):
        msg = 'd'.encode() + b'\x00\x00\x00\x00\x00'
        self.serial_connection.write(msg)
        answer = self.serial_connection.readline()
        success = answer.decode().strip() == 'closed'
        if success:
            print('closed connection')
            self.serial_connection.close()
            self.serial_connection = None
        else:
            print('Could not close connection')
        return success

    def get_led_count(self, connection=None):
        if connection == None:
            connection = self.serial_connection
        msg = 'n'.encode() + b'\x00\x00\x00\x00\x00'
        connection.write(msg)
        number_leds = ord(connection.read())
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
        #check color values for valid range
        if not (0 <= int(red) <= 255 and 0<=int(green)<=255 and 0<=blue<=255):
            print('color intensity out of range. all values must be from 0 to 255')
            return 'color intensity out of range. all values must be from 0 to 255'
        red = bytes([int(red)])
        green = bytes([int(green)])
        blue = bytes([int(blue)])
        msg = 'a'.encode() + b'\x00\x00' + red + green + blue
        self.serial_connection.write(msg)
        answer = self.serial_connection.readline()
        return answer


    def find_port(self):
        ports = serial.tools.list_ports.comports()
        found_port = None
        found_connection = None
        for port in ports:
            try:
                connection = serial.Serial(port.device, baudrate=self.BAUD_RATE, timeout=self.TIMEOUT)
                print('Found a device on ',port.device)

                connection.write('o'.encode())

                #Check if it is a led controller. If it is, it will answer with 'connected'
                answer = connection.readline()
                if not answer.decode().strip() == 'open':
                    continue

                found_connection = connection
                found_port = port.device
            except serial.serialutil.SerialException:
                continue
        #close port again
        if not found_port == None:
            #set timeout to normal value
            found_connection.timeout = self.TIMEOUT

            print(found_port, 'is a valid LED controller')
        return (found_connection, found_port)

if __name__ == '__main__':
    #server = LedSerialConnector(serial_port_name = 'COM5')
    server = LedSerialConnector()
    server.run()
