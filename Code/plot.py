import DAO
import matplotlib.pyplot as plt
import ast


dao = DAO.UDP_DAO("localhost", 12347) #retrieve locations
unfiltered = []
filtered = []

ax = plt.gca()
color1 = next(ax._get_lines.prop_cycler)['color']
color2 = next(ax._get_lines.prop_cycler)['color']
while True:
    location =  ast.literal_eval(dao.readData())
    unfiltered.append(location['distances']['unfiltered'])
    filtered.append(location['distances']['filtered'])
    plt.legend(['filtered','unfiltered'])
    plt.plot(range(0, len(filtered)), filtered, marker='o', color = color1)
    plt.plot(range(0, len(filtered)), unfiltered, marker='o', color = color2)
    plt.pause(0.05)
