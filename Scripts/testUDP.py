import udpy

udp = udpy.UDP_DAO("localhost",12346)

while True:
    data = udp.readData()
    print data
