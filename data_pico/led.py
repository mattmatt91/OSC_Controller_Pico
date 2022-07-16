import neopixel
import board



class Pixels():
        def __init__(self,num_pixels=8):
                self.pixels = neopixel.NeoPixel(board.GP0, num_pixels)
                self.pixels.brightness = 0.1
                self.pixels.fill((255, 0, 0))
                self.pixels.show()
        
        def color_pixels(self, pixel, color):
                self.pixels.fill((0, 0, 0))
                self.pixels[pixel] = color
                self.pixels.show()
            
        def fill_all_white(self):
            self.pixels.fill((0,0,0))
                
        def color_all_pixel(self, colors): # remove keyarg
            for color, pixel in zip(colors, range(len(self.pixels))):
                self.pixels[pixel] = color