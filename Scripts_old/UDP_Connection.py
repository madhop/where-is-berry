import socket
import json

def getData(address, port):

    UDP_IP = address
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    return json.loads(data)
