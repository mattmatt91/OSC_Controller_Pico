import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend


class MIDI_device():
        def __init__(self):
        
                self.buffer = []
                print(usb_midi.ports)
                self.midi = adafruit_midi.MIDI(
                        midi_in=usb_midi.ports[0], in_channel=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), midi_out=usb_midi.ports[1], out_channel=0,
                        debug=False,in_buf_size=100)
                # Convert channel numbers at the presentation layer to the ones musicians use
                print("Default output channel:", self.midi.out_channel )
                print("Listening on input channel:", self.midi.in_channel )
        
        def send_cc(self, num, value, channel):
                self.midi.send(ControlChange(num, value), channel=channel)

        
        def read_cc(self):
                msg = self.midi.receive()
                if msg is not None:
                    self.buffer.append(msg)
                    # midi_message.from_bytes(msg)
                    # print("Received:", msg) #msg.value
        
        def read_buffer(self):
            buff = self.buffer
            self.buffer = []
            return buff