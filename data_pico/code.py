from oled import Oled
from encoder import Encoders
from led import Pixels
from time import time, sleep
from serial_2_pico import Pico
import gc
import board

num_tracks = 9
track = 0
num_fx = 3 # all encoders -1

pins_encoders = [[board.GP20, board.GP19, board.GP18], #len should fit to num_fx
                [board.GP13, board.GP12, board.GP11],
                [board.GP3, board.GP2, board.GP4],
                [board.GP9, board.GP8, board.GP7]]


test_msg_led =  {'type': 'LED', 'data':[(0,i*10,0) for i in range(num_tracks)]}
test_msg_oled = {'type': 'OLED', 'data':[[(i+n)%2 for n in range(20)]for i in range(20)], 'reset':'1'}


print(test_msg_led)
print(test_msg_oled)
class Controller():
    def __init__(self):
        # print('starting controller')
        self.num_tracks = num_tracks
        Encoders.init_encoders(pins_encoders)
        self.pico = Pico()
        
        self.oleds = [Oled(i) for i in range(num_fx)]

        self.led = Pixels(num_tracks)

       
  
        

        # msg = {'track':self.track,'cmd':'fx', 'enc':enc_id, 'type':'btn', 'value':value}
      
        
        # msg = {'track':self.track, 'enc':enc_id,'cmd':'fx', 'type':'enc', 'value':value}
      

        
    
    def encoder_handler(self, buffer):
        for msg in buffer:
            print(str(msg))
                    
    
    def serial_handler(self, msg):
        # print('pico returns: ', buffer_serial)
        if msg['type'] == 'LED':
            data = msg['data'] 
            self.led.color_all_pixel(data)
            
        elif msg['type'] == 'OLED':
            index = msg['index']
            data = msg['data']
            if reset:
                self.oled.fill_all_white()
            self.oleds[index].draw_bitmap(data) 
            

    def loop(self):
        try:
            Encoders.read_all()
            buffer_encoders = Encoders.read_buffer()
            if len(buffer_encoders) > 0:
                self.encoder_handler(buffer_encoders)
        except Exception as e:
            print(f'error while reading encoders: {e}')
            
        """try:"""
        if True:
            self.pico.read_serial_input()
            # msg = self.pico.get_msg_enc()
            msg = test_msg_led
            if msg != None:
                self.serial_handler(msg)
                # print(latest_input_line+ 'returned from pico')
        """except Exception as e:
            print(f'error while reading serial: {e}')"""
        
        
if __name__ =='__main__':
        controller = Controller()
        start = time()
        _time = time()
        while True:      
        # while _time <= start+100:
            try:
                controller.loop()
            except KeyboardInterrupt:
                gc.collect()
            _time = time()
        print('connection_closed')
        
        







