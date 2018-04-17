#import where_is_berry as wib
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt
import pprint

dao = DAO.UDP_DAO("localhost", 12347) #publish locations
berry = wib.WhereIsBerry(12346)

while True:
    location = berry.whereIsBerry(filtered = True)
    pprint.pprint(location)
    dao.writeData(location)
