import udpy

udp = udpy.UDP_DAO("localhost",12347)

while True:
    data = udp.readData()
    print data
