import serial

class ClosableSerialConnection(serial.Serial):
    def __init__(self, close_action):
        self.close_action = close_action

    def __enter__(self):
        super.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_action()
        super.__exit__()