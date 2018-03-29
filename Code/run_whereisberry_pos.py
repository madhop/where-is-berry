#import where_is_berry as wib
import where_is_berry_pos as wib
import DAO
import matplotlib.pyplot as plt
import pprint

dao = DAO.UDP_DAO("localhost", 12347) #publish locations
berry = wib.WhereIsBerry()

while True:
    location = berry.whereIsBerry(True)
    pprint.pprint(location)
    dao.writeData(location)
