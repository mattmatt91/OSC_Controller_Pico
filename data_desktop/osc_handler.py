import argparse
from audioop import add
import random
import time
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
from pythonosc import udp_client
from serial_pico import SerialOSC


port_pcio = '/dev/ttyACM0'

class OSC_Handler():
    def __init__(self, ip, port_in, port_out) -> None:
        self.track = 1 
        self.num_tracks = 8
        self.ip = ip
        self.port_in = port_in
        self.port_out = port_out
        self.flag_osc = True
        self.serial_osc = SerialOSC(port_pcio)

        # client
        self.parser_client = argparse.ArgumentParser()
        self.parser_client.add_argument("--ip", default=self.ip,
            help="The ip of the OSC server")
        self.parser_client.add_argument("--port", type=int, default=self.port_out,
            help="The port the OSC server is listening on")
        self.args_client = self.parser_client.parse_args()
        self.client = udp_client.SimpleUDPClient(self.args_client.ip, self.args_client.port)

        # server
        self.dispatcher_server = Dispatcher()
        self.dispatcher_server.set_default_handler(self.default_handler)
        asyncio.run(self.init_server())

    


    def send_msg(self, add, msg):
        self.client.send_message(add, msg)
        # print(f'sending to {add} -> {str(msg)} -> ip: {self.ip}, port: {self.port_out}')


    def default_handler(self, address, *args):
        if address.find('/vu') < 0:
            print(f"handler: {address}: {args}")
        
    def set_track(self, val):
        track_old = self.track
        self.track = self.track+ val
        if self.track > self.num_tracks:
            self.track = self.num_tracks
        elif self.track < 0:
            self.track = 0
        else:
            print(f'selected track: {self.track}')
            add_osc = f"b/track/{track_old}/select"
            self.client.send_message(add_osc, 0)
            add_osc = f"b/track/{self.track}/select"
            self.client.send_message(add_osc, 1)
            add_osc = f"s/track/recv/{self.track}/name"
            self.client.send_message(add_osc, 'test')
            # self.serial_osc.send(b'data=[255,10,20,30,40,50,60,70,80],type=LED')



    def arm_track(self):
        print(f'armed track: {self.track}')
        add_osc = f"t/track/{self.track}/recarm/toggle"
        self.client.send_message(add_osc, 1)

    # adds = f't/track/{i%5}/volume' <-- for setting volume track
    # adds = f'b/track/{i%5}/fx/1/openui' <-- open ui

    def send_fx_enc(self, enc, val):
        add_osc = f"t/track/{self.track}/enc/{enc}/toggle"
        self.client.send_message(add_osc, val)

    def send_fx_btn(self, enc):
        add_osc = f"t/track/{self.track}/btn/t{enc}/toggle"
        self.client.send_message(add_osc, 'test')

    def serial_handler(self, msg_list):
        for msg in msg_list:
            if msg['id'] == 0: # menu stuff
                if msg['element'] == 'rot':
                    val = msg['val']
                    # print('track - rot - ', val)
                    self.set_track(val)
                elif msg['element'] == 'btn':
                    # print('track - btn')
                    self.arm_track()

            elif msg['id'] > 0:
                if msg['element'] == 'rot':
                    val = msg['val']
                    self.send_fx_enc(msg['id'], val)
                    print('fx - rot - ', val)
                elif msg['element'] == 'btn':
                    self.send_fx_btn(msg['id'])
                    print('fx - btn')


    async def loop(self):
        i = 1
        test = False
        while self.flag_osc:  
            if not test:
                    await asyncio.sleep(0.01)
                    msg_ser = self.serial_osc.read()  
                    if msg_ser != None:
                        self.serial_handler(msg_ser)
            else:
                await asyncio.sleep(1)
                vals = f'track{i}'
                adds = f's/track/{i%5}/fx/{1}/name'
                self.client.send_message(adds, vals)
                print(adds, vals)
                print('\n')
                i+=1

    def stop_osc(self):
        self.flag_osc = False


    async def init_server(self):
        server = AsyncIOOSCUDPServer((self.ip, self.port_in), self.dispatcher_server, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
        await self.loop()  # Enter main loop of program
        transport.close()  # Clean up serve endpoint



if __name__ == '__main__':
    osc_handler = OSC_Handler("192.168.1.9",1338,1337)

