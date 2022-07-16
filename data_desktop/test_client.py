from pythonosc.udp_client import SimpleUDPClient
from time import sleep
ip = "127.0.0.1"
port = 1337

client = SimpleUDPClient(ip, port)  # Create client
while True:
    add = "/track/3/volume" 
    data = 0.3
    client.send_message(add, data) 
    print('ip: ', ip, 'port: ', port, 'add: ',add, 'data: ', data)
    sleep(1)