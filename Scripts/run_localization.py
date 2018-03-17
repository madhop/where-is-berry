import thread
import localization
import udpy

localization = localization.Localization()

udp_writer = udpy.UDP_DAO("localhost", 12347)

while True:
   udp_writer.writeData(localization.getLocation())
