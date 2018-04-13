import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import numpy as np


errors = np.asarray([3.2023463632565305, 2.1628601560424245, 1.027460582206667, 0.6308177763968214, 1.5810900744568686,
        4.466374130612163, 1.1592874497800696, 1.2631839743391506, 1.4202043298795168, 1.216591793618466,
        1.341051447365456, 2.963741353538781, 2.132081683224721, 2.0925278179792004, 1.78417591941049])

#errors = np.sort(errors)
values, base = np.histogram(errors)
cumulative = np.cumsum(values)
cumulative = cumulative/15.0
#plt.plot(errors ,mlab.normpdf(errors, np.mean(errors), np.std(errors)))
plt.plot(base[:-1], cumulative)

plt.show()
