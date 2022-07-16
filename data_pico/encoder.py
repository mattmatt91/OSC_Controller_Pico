import digitalio
import board
import rotaryio

pins_encoders = [[board.GP20, board.GP19, board.GP18],
                [board.GP13, board.GP12, board.GP11],
                [board.GP3, board.GP2, board.GP4],
                [board.GP9, board.GP8, board.GP7]]

class Encoders():
        encoders = {}
        msg_buffer = []
        def __init__(self, id,  pin_e1, pin_e2, pin_btn):
                self.id = id
                self.enc = rotaryio.IncrementalEncoder(pin_e1, pin_e2)
                self.last_position = None
                self.btn = digitalio.DigitalInOut(pin_btn)
                self.btn.direction = digitalio.Direction.INPUT
                self.btn.pull = digitalio.Pull.UP
                self.btn_state = None
                self.last_position = self.enc.position
                # print(f'created encoder {self.id}: {pin_e1, pin_e2, pin_btn}')
                Encoders.encoders[self.id] = self
        
        def read_enc(self):
                current_position = self.enc.position
                position_change = current_position - self.last_position
                if position_change != 0:
                        # print(position_change, self.id)
                        Encoders.msg_buffer.append({'id':self.id, 'element':'rot', 'val':position_change})
                self.last_position = current_position
                if not self.btn.value and self.btn_state is None:
                        self.btn_state = "pressed"
                if self.btn.value and self.btn_state == "pressed":
                        # print("Button pressed.", self.id)
                        Encoders.msg_buffer.append({'id':self.id, 'element':'btn', 'val':True})
                        self.btn_state = None

        
        @classmethod
        def read_all(cls):
                for encoder in cls.encoders:
                        cls.encoders[encoder].read_enc()
                        
        @classmethod
        def read_buffer(cls):
                buf = cls.msg_buffer
                cls.msg_buffer = []
                return buf
                        
        @classmethod
        def init_encoders(cls, pins_encoders):
            i = 0
            for pins in pins_encoders:
                cls.encoders[i] = Encoders(i, pins[0], pins[1], pins[2])
                i += 1