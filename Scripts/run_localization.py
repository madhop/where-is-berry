import thread
import localization
import udpy
import kalman

localization = localization.Localization()

udp_writer = udpy.UDP_DAO("localhost", 12347)

kalman = kalman.Kalman()
while True:
    udp_writer.writeData(localization.getLocation(True))
    udp_writer.writeData(localization.getLocation(False))
