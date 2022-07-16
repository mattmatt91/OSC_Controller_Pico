from serial import Serial
from time import sleep
import ast


port = '/dev/ttyACM0'

class SerialOSC():
    def __init__(self, port) -> None:
        self.ser = Serial(port, 115200, timeout=0)

    def read(self):
        try:
            msg = self.ser.readlines()
            if len(msg) > 0:
                msg = [ast.literal_eval(i.decode('utf-8')) for i in msg]
                return msg
        except:
            pass

    def send(self, msg):
        self.ser.write(b'hello')   

    def close(self):
        self.ser.close()  


if __name__ == '__main__':
    serial_osc = SerialOSC(port)
    serial_osc.send('est')
    serial_osc.read()
    serial_osc.close()

    # str = " Jan = January; Feb = February; Mar = March"