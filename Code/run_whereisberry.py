#import where_is_berry as wib
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt
import pprint

dao = DAO.UDP_DAO("localhost", 12347) #publish locations
berry = wib.WhereIsBerry(12348) #(from nodered 12346, from simulation 12348)

while True:
    location = berry.whereIsBerry(filtered = True)
    print '***** tel chi la location'
    pprint.pprint(location)
    dao.writeData(location)
