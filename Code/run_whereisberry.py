#import where_is_berry as wib
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt

dao = DAO.UDP_DAO("localhost", 12347)

berry = wib.WhereIsBerry()

filtered = []
unfiltered = []
while True:
    location = berry.whereIsBerry(True)
    filtered.append(location['filtered'])
    unfiltered.append(location['unfiltered'])
    print location
    plt.plot(range(0, len(filtered)), filtered, marker='o')
    plt.plot(range(0, len(filtered)), unfiltered, marker='o')
    plt.legend(['filtered','unfiltered'])
    plt.show()
    #print "*******BERRY:", location
    dao.writeData(location)
    #dao.writeData()
