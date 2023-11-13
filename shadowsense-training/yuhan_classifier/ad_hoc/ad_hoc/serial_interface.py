import serial

class LED_Interface:
    def __init__(self, name, baudrate=9600):
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = name
        self.ser.open()

    def action(self,act):
        if act=='blink':
            self.ser.write(b'1\n')
        elif act=='scan':
            self.ser.write(b'2\n')
        elif act=='dscan':
            self.ser.write(b'3\n')
        
    def color(self, color):
        if color=='red':
            self.ser.write(b'0\n');
        elif color=='orange':
            self.ser.write(b'1\n');
        elif color=='yellow':
            self.ser.write(b'2\n');
        elif color=='green':
            self.ser.write(b'3\n');
        elif color=='blue':
            self.ser.write(b'4\n');
        elif color=='purple':
            self.ser.write(b'5\n');
        elif color=='white':
            self.ser.write(b'6\n');
        elif color=='dark':
            self.ser.write(b'7\n');
    def close(self):
        self.ser.close()

