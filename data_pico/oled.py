
import board
import busio
import adafruit_tca9548a
import adafruit_ssd1306
from time import sleep, time


width = 128
height = 64


class Oled():
    i2c = busio.I2C(board.GP17, board.GP16)
    tca = adafruit_tca9548a.TCA9548A(i2c)
    def __init__(self, index):
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, Oled.tca[index])
        self.oled.fill(0)

    
    def draw_bitmap(self, bitmap):
        self.oled.fill(0)
        r = 0
        for row in bitmap:
            c = 0
            for col in row:

                self.oled.pixel(c, r, col)
                c+=1
            r+=1
        self.oled.show()





