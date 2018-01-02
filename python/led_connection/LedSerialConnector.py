import serial,sys
from time import sleep
import serial.tools.list_ports

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
    BAUD_RATE = 12000
    TIMEOUT = 1 #in seconds

    def __init__(self, serial_port_name):
        self.serial_port_name = serial_port_name

    def __init__(self):
        """
        If no port name is given, try to find it
        """
        (connection, port_name) = self.find_port()
        if connection == None:
            print('No valid device found. Aborting')
            sys.exit(1)
        else:
            self.serial_connection = connection
            self.serial_port_name = port_name
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def get_connection(self):
        if self.serial_connection == None:
            self.serial_connection = self.connect(self.serial_port_name)
            self.serial_connection.readline()
        return self.serial_connection

    def run(self):
        self.get_connection()
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
            elif user_in.startswith('q'): #quit
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
            connection = serial.Serial(serial_port_name, baudrate=self.BAUD_RATE)  # Establish the connection on a specific port
            print('connected')
            print(connection.readline().decode())
            connection.write('o'.encode() + b'\x00\x00\x00\x00\x00')
            return connection
        except serial.serialutil.SerialException:
            failed_attempts = failed_attempts+1
            print('failed to connect')
            if failed_attempts>100:
                print('no connection possible')
                return
            sleep(0.5)
            self.connect(serial_port_name=serial_port_name)

    def disconnect(self, connection=None):
        serial_conn = connection
        if connection == None:
            serial_conn = self.serial_connection
        if serial_conn == None:
            print('Cannot disconnect a connection that is None.')
            return
        msg = 'd'.encode() + b'\x00\x00\x00\x00\x00'
        serial_conn.write(msg)
        answer = serial_conn.readline()
        success = answer.decode().strip() == 'closed'
        if success:
            print('closed connection')
        else:
            print('Could not close connection')
        serial_conn.close()
        if connection == None:
            self.serial_connection = None

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
            print('Found a device on ', port.device)
            (connection, success) = self.try_port(port.device)
            #retry a few times
            for retry in range(2):
                if not connection == None and success:
                    #everything went well
                    found_connection = connection
                    found_port = port.device
                    break
                elif not connection == None:
                    #could connect, but not getting answer, retry
                    #print(connection.readline().decode())
                    print('Connecting to ', port.device, ' failed. Retrying.')
                    self.disconnect(connection=connection)
                    (connection, success) = self.try_port(port_name=port.device)
                else:
                    #all failed
                    continue
        if not found_port == None:
            #set timeout to normal value
            found_connection.timeout = self.TIMEOUT

            print(found_port, 'is a valid LED controller')
        return (found_connection, found_port)

    def try_port(self, port_name):
        try:
            connection = serial.Serial(port_name, baudrate=self.BAUD_RATE, timeout=1, write_timeout=1)
            #print(connection.readline())
            connection.write('o'.encode() + b'\x00\x00\x00\x00\x00')

            # Check if it is a led controller. If it is, it will answer with 'connected'
            answer = connection.readline()
            #print(answer)
            # if the device is not answering correctly, try to disconnect and connect again.
            # If that fails again, try next device
            if answer.decode().strip() == 'open':
                return (connection, True)
            else:
                return (connection, False)
        except serial.serialutil.SerialException as error:
            print(error)
            connection.close()
            return (None, None)

if __name__ == '__main__':
    #server = LedSerialConnector(serial_port_name = 'COM5')

        with LedSerialConnector() as server:
            try:
                server.run()
            except KeyboardInterrupt:
                print('Killing')
                server.disconnect()
