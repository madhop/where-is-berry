import socket

class UDP_DAO:
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port

    def readData(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.UDP_IP, self.UDP_PORT))
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        return data

    def writeData(self,message):
        MESSAGE = str(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT))
