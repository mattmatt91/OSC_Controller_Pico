import uselect
import time
import gc
from sys import stdin, exit

# size of each letter in pixels
CHARACTER_SIZE = 8

# how serial lines are ended
TERMINATOR = "\n"


class Pico:

    def __init__(self):

        self.run_loop = True

        self.buffered_input = []

        self.input_line_this_tick = ""
        
        self.output = ""

    def main(self):

        latest_input_line = ""

        
        while self.run_loop: 
            self.read_serial_input()
            if len(self.input_line_this_tick)>0:
                latest_input_line = self.input_line_this_tick
                # print(latest_input_line+ ' from pico')
    

       

           
         
            time.sleep(0.001)



    def read_serial_input(self):
        """
        Buffers serial input.
        Writes it to input_line_this_tick when we have a full line.
        Clears input_line_this_tick otherwise.
        """
        # stdin.read() is blocking which means we hang here if we use it. Instead use select to tell us if there's anything available
        # note: select() is deprecated. Replace with Poll() to follow best practises
        select_result = uselect.select([stdin], [], [], 0)
        while select_result[0]:
            # there's no easy micropython way to get all the bytes.
            # instead get the minimum there could be and keep checking with select and a while loop
            input_character = stdin.read(1)
            # add to the buffer
            self.buffered_input.append(input_character)
            # check if there's any input remaining to buffer
            select_result = uselect.select([stdin], [], [], 0)
        # if a full line has been submitted
        if TERMINATOR in self.buffered_input:
            line_ending_index = self.buffered_input.index(TERMINATOR)
            # make it available
            self.input_line_this_tick = "".join(self.buffered_input[:line_ending_index])
            # remove it from the buffer.
            # If there's remaining data, leave that part. This removes the earliest line so should allow multiple lines buffered in a tick to work.
            # however if there are multiple lines each tick, the buffer will continue to grow.
            if line_ending_index < len(self.buffered_input):
                self.buffered_input = self.buffered_input[line_ending_index + 1 :]
            else:
                self.buffered_input = []
        # otherwise clear the last full line so subsequent ticks can infer the same input is new input (not cached)
        else:
            self.input_line_this_tick = ""

    
    def exit(self):
        self.run_loop = False

    def get_msg_enc(self):
        msg = str(self.input_line_this_tick)
        if len(msg)>0:
            msg_enc = dict(subString.split("=") for subString in msg.split(";"))
            return msg_enc
        else:
            return None



# start the code
if __name__ == "__main__":
    pico = Pico()
    pico.main()
    # when the above exits, clean up
    gc.collect()