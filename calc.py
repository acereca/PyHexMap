import matplotlib.pyplot as plt
import matplotlib.collections
import numpy as np
import pandas as pd
import json
from hexagon import *

settlements = []
hexmap = hexmap()

#hexes
data2 = pd.read_csv('testmap.csv', sep=',')

# paths
data = pd.read_csv('roads.csv', sep=',')

sidelist = ['0','1','2','3','4','5']
for i,e in data.iterrows():
    active_hex = hex(e['q'],e['r'])
    connected_sides = []
    for side in sidelist:
        if e[side] == True:
            connected_sides.append(int(side))

    if len(connected_sides) == 1 or len(connected_sides) >= 3:

        for cs in connected_sides:
            #print(active_hex.hex_side(cs))
            s = data2.loc[(data2['q'] == e['q']) & (data2['r'] == e['r'])]

            if (s.shape[0]) == 1:
                x_mod = (active_hex.get_x_pos() + active_hex.hex_side(cs)[0]) / 2
                y_mod = (active_hex.get_y_pos() + active_hex.hex_side(cs)[1]) / 2

            else:
                x_mod = active_hex.get_x_pos()
                y_mod = active_hex.get_y_pos()

            # plt.plot(
            #     [x_mod, active_hex.hex_side(cs)[0]],
            #     [y_mod, active_hex.hex_side(cs)[1]],
            #     lw = 5,
            #     c = '#777777',
            #     zorder = 1
            # )

    if len(connected_sides) == 2:
        #print(connected_sides)

        side1_pos = active_hex.hex_side(connected_sides[0])
        side2_pos = active_hex.hex_side(connected_sides[1])
        midpoint = [active_hex.get_x_pos(), active_hex.get_y_pos()]

        tripoint = [
            (side1_pos[0]+side2_pos[0]+midpoint[0])/3,
            (side1_pos[1]+side2_pos[1]+midpoint[1])/3
        ]

        # plt.plot(
        #     [side1_pos[0], tripoint[0], side2_pos[0]],
        #     [side1_pos[1], tripoint[1], side2_pos[1]],
        #     lw = 5,
        #     c = '#777777',
        #     zorder = 1
        # )


for i,e in data2.iterrows():
    hgrid = hex(
        e['q'],
        e['r'],
        c=('plains' if e['c'] == '' else e['c']),
        settlement=e['settlement'],
        name=e['name'],
        road=(False if e['road'] != True else True)
    )
    # to be removed in future
    hgrid.plot()
    hexmap.add(hgrid)

xy = np.array(hexmap.get_road_pos()).T
sxy = np.empty(xy.shape)
sxy[0] = xy[0]
sxy[xy.shape[0]-1] = xy[xy.shape[0]-1]
for i in np.arange(1,xy.shape[0]-1):
     sxy[i] = (xy[i-1]+xy[i]+xy[i+1])/3

print(sxy, xy)
plt.plot(sxy[:,0],sxy[:,1], c='r', zorder=1)


plt.axis('equal') # fit to plotted hexes
plt.axis('off')    # then turn off lines

plt.legend(handles=[matplotlib.collections.RegularPolyCollection(
        numsides=6,
        sizes=(100,),
        facecolors=(col,),
        label=coln
    ) for coln,col in terrain_colors.items()]
)

plt.savefig('rendered.png', bbox_inches='tight')
