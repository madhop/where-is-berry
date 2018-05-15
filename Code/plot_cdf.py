from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import numpy as np

techniques = ['localization_trilateration_kalman',
                'localization_trilateration_unfiltered',
                'localization_fingerprinting_kalman',
                'localization_fingerprinting_unfiltered'
                ]

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
errors_mongo = db['errors_mongo'] #errors_mongo

for t in techniques:
        print t
        errors = np.asarray(list(errors_mongo.find(projection=[t]))[0][t])
        print(np.mean(errors))
        values, base = np.histogram(errors)
        cumulative = np.cumsum(values)
        cumulative = cumulative/float(len(errors))
        plt.plot(base[:-1], cumulative)

'''# unfiltered
errors = np.asarray([3.2023463632565305, 2.1628601560424245, 1.027460582206667, 0.6308177763968214, 1.5810900744568686,
        4.466374130612163, 1.1592874497800696, 1.2631839743391506, 1.4202043298795168, 1.216591793618466,
        1.341051447365456, 2.963741353538781, 2.132081683224721, 2.0925278179792004])#, 1.78417591941049])
values, base = np.histogram(errors)
cumulative = np.cumsum(values)
cumulative = cumulative/14.0
plt.plot(base[:-1], cumulative)

# kalman
errors = np.asarray([2.801846258135186, 2.320959355398024, 1.3608746914842589, 0.8430509621214368, 0.8110864804155035,
        1.08252843883038, 1.5212490494000745, 1.5510306422816258, 1.4093806722154187, 1.3375855928995217,
        1.715989403882959, 2.10124394488345, 2.157826339406514, 1.8925836486684133])
values, base = np.histogram(errors)
cumulative = np.cumsum(values)
cumulative = cumulative/14.0
plt.plot(base[:-1], cumulative)

#fingerprinting
errors = np.asarray([1.8193652263793376, 0.8958893170197145, 0.6900659500063883, 0.788905149208018, 0.9454671571835516,
        0.6153606913830285, 0.9055574237137313, 1.0492851781180579, 1.0692242401310053, 0.6540494603688626,
        1.095126311794344, 1.454458496897059, 1.1882162611080136, 1.0513458489134622])#, 1.094403067880318]
values, base = np.histogram(errors)
cumulative = np.cumsum(values)
cumulative = cumulative/14.0
plt.plot(base[:-1], cumulative)'''


plt.legend(['trilateration_kalman',
            'trilateration_unfiltered',
            'fingerprinting_kalman',
            'fingerprinting_unfiltered'],
            loc=4, borderaxespad=0.)
#plt.show()
