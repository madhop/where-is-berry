import udpy

def run(name):
    udp = udpy.UDP_DAO("localhost",12347)

    while True:
        data = udp.readData()
        #print "******* THREAD ",name
