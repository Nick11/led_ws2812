import serial
from time import sleep

serial_port_name = '/dev/cu.usbserial-DA00SVW5'

def main():
    with connect() as ser:
        ser.readline()
        #print(ser.readline())  # Read the newest output from the Arduin
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
                msg = b'\x01\x00\x00\x00\x00'+'n'.encode()
                ser.write(msg)
                number_leds = ord(ser.read())
                print(number_leds)
            else:
                split_input = user_in.split(',')
                if not len(split_input) == 4:
                    continue
                address = (int(split_input[0])).to_bytes(2, byteorder='big')
                red = bytes([int(split_input[1])])
                green = bytes([int(split_input[2])])
                blue = bytes([int(split_input[3])])
                msg = b'\x00'+address+red+green+blue
                ser.write(msg)
                ser.readline().decode()
    #      counter +=1
    #      chara = chr(counter)
    #      ser.write(str.encode(chara))
    #      #ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
          #print(ser.readline()) # Read the newest output from the Arduino
      #  sleep(.1) # Delay for one tenth of a second
    #      if counter == 255:
    #         counter = 32

def connect():
    failed_attempts = 0
    try:
        ser = serial.Serial(serial_port_name, 9600)  # Establish the connection on a specific port
        print('connected')
        return ser
    except serial.serialutil.SerialException:
        failed_attempts = failed_attempts+1
        print('failed to connect')
        if failed_attempts>100:
            print('no connection possible')
            return
        sleep(0.5)
        connect()

main()