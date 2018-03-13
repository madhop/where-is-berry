import socket
#import ast


class UDP_DAO(object):
    """docstring for UDP_DAO."""
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print 'UDP_DAO: ' + self.UDP_IP + " - " + str(self.UDP_PORT)

    def read_data(self):
        data, addr = self.sock.recvfrom(1024)
        return data
