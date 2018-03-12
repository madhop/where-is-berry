#Colors
colors = {1 : 'pink', 2 : 'purple', 3 : 'green', 4 : 'yellow', 5 : 'white'}

#Ids
uuid = "b9407f30f5f8466eaff925556b57fe6d"
b_id = {}
b_id[colors[1]] = {}
b_id[colors[1]]['uuid'] = uuid
b_id[colors[1]]['major'] = 30085
b_id[colors[1]]['minor'] = 60205
b_id[colors[2]] = {}
b_id[colors[2]]['uuid'] = uuid
b_id[colors[2]]['major'] = 56653
b_id[colors[2]]['minor'] = 61150
b_id[colors[3]] = {}
b_id[colors[3]]['uuid'] = uuid
b_id[colors[3]]['major'] = 42622
b_id[colors[3]]['minor'] = 48183
b_id[colors[4]] = {}
b_id[colors[4]]['uuid'] = uuid
b_id[colors[4]]['major'] = 534
b_id[colors[4]]['minor'] = 21618
b_id[colors[5]] = {}
b_id[colors[5]]['uuid'] = uuid
b_id[colors[5]]['major'] = 49242
b_id[colors[5]]['minor'] = 41078

#Location
places = {}
places[1] = {'where' : 'Luca Bedroom', 'when' : '12 mar 2018'}

b_positions = {}
b_positions[1] = {}
b_positions[1][colors[1]] = {}
b_positions[1][colors[1]]['place'] = places[1]
b_positions[1][colors[1]]['x'] = 160
b_positions[1][colors[1]]['y'] = 398
b_positions[1][colors[1]]['z'] = 110
b_positions[1][colors[2]] = {}
b_positions[1][colors[2]]['place'] = places[1]
b_positions[1][colors[2]]['x'] = 320
b_positions[1][colors[2]]['y'] = 265
b_positions[1][colors[2]]['z'] = 52
b_positions[1][colors[3]] = {}
b_positions[1][colors[3]]['place'] = places[1]
b_positions[1][colors[3]]['x'] = 5
b_positions[1][colors[3]]['y'] = 198
b_positions[1][colors[3]]['z'] = 54
b_positions[1][colors[4]] = {}
b_positions[1][colors[4]]['place'] = places[1]
b_positions[1][colors[4]]['x'] = 272
b_positions[1][colors[4]]['y'] = 5
b_positions[1][colors[4]]['z'] = 73
b_positions[1][colors[5]] = {}
b_positions[1][colors[5]]['place'] = places[1]
b_positions[1][colors[5]]['x'] = 438
b_positions[1][colors[5]]['y'] = 137
b_positions[1][colors[5]]['z'] = 55




def getColors():
    return colors

def getId():
    return b_id

def getPos(place):
    return b_positions[place]

def getPlace(n):
    return places[n]
