import DAO
import matplotlib.pyplot as plt
import ast


dao = DAO.UDP_DAO("localhost", 12347) #retrieve locations
unfiltered = []
filtered = []
time = []
x = []
y = []

ax = plt.gca()
color1 = next(ax._get_lines.prop_cycler)['color']
color2 = next(ax._get_lines.prop_cycler)['color']
while True:
    location =  ast.literal_eval(dao.readData())

    print location
    if len(filtered) > 30:
        filtered.pop(0)
        unfiltered.pop(0)
        time.pop(0)


    ''' 2D
    x.append(location['estimates']['location']['x'])
    y.append(location['estimates']['location']['y'])
    #plt.legend(['x','y'])
    plt.plot(x, y, marker='o', color = color1)
    plt.pause(0.05)'''

    '''1D'''
    filtered.append(location['localization_kalman']['measures'][0]['dist'])
    unfiltered.append(location['localization_unfiltered']['measures'][0]['dist'])
    time.append(location['localization_kalman']['measures'][0]['elapsed_time'])

    plt.plot(time, filtered, color = color1)
    plt.plot(time, unfiltered, color = color2)
    plt.legend(['filtered','unfiltered'])
    plt.pause(0.05)
