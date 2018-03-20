#import where_is_berry as wib
import where_is_berry as wib
import DAO

dao = DAO.UDP_DAO("localhost", 12347)

berry = wib.WhereIsBerry()

while True:
    location = berry.whereIsBerry(True)
    #print "*******BERRY:", location
    dao.writeData(location)
    #dao.writeData()
