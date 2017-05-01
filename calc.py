import matplotlib.pyplot as plt
import matplotlib.collections
import numpy as np
import pandas as pd
import json
from hexagon import *

settlements = []

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

    if len(connected_sides) == 1:
        corner_pos_1 = active_hex.hex_corner(connected_sides[0])
        corner_pos_2 = active_hex.hex_corner(connected_sides[0]+1)
        s = data2.loc[(data2['q'] == e['q']) & (data2['r'] == e['r'])]
        if (s.shape[0]) == 1:
            x_mod = (active_hex.get_x_pos() + (corner_pos_1[0]+corner_pos_2[0])/2)/2
            y_mod = (active_hex.get_y_pos() + (corner_pos_1[1]+corner_pos_2[1])/2)/2

        else:
            x_mod = active_hex.get_x_pos()
            y_mod = active_hex.get_y_pos()

        plt.plot(
            [x_mod, active_hex.hex_side(connected_sides[0])[0]],
            [y_mod, active_hex.hex_side(connected_sides[0])[1]],
            lw = 5,
            c = '#777777',
            zorder = 1
        )
    if len(connected_sides) == 2:
        print(connected_sides)

        side1_pos = active_hex.hex_side(connected_sides[0])
        side2_pos = active_hex.hex_side(connected_sides[1])
        midpoint = [active_hex.get_x_pos(), active_hex.get_y_pos()]

        tripoint = [
            (side1_pos[0]+side2_pos[0]+midpoint[0])/3,
            (side1_pos[1]+side2_pos[1]+midpoint[1])/3
        ]

        plt.plot(
            [side1_pos[0], tripoint[0], side2_pos[0]],
            [side1_pos[1], tripoint[1], side2_pos[1]],
            lw = 5,
            c = '#777777',
            zorder = 1
        )


qlim = [0,0]
rlim = [0,0]
for i,e in data2.iterrows():
    hgrid = hex(e['q'],e['r'], c=('plains' if e['c'] == '' else e['c']))
    #print(e)
    plt.gca().add_patch(hgrid.to_poly())


    # settlements
    if isinstance(e['settlement'], str):
        t = e['settlement']
        print(t)
        plt.gca().add_patch(
            plt.Circle(
                (hgrid.get_x_pos(), hgrid.get_y_pos()),
                settlement_types[t]['size']/2,
                fc=settlement_types[t]['fc'],
                lw=4,
                aa=True,
                fill = True,
                ec=settlement_types[t]['ec'],
                zorder = 2
            )
        )
        plt.annotate(
            e['name'],
            xy = (hgrid.get_x_pos(), hgrid.get_y_pos()),
            fontsize = 14,
            xytext=(0,1),
            ha = 'center',
            va = 'center',
            bbox=dict(boxstyle="round", fc="#ffffff55", ec='#ffffff00')
        )
        settlements.append(hgrid)




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
