import numpy as np
import matplotlib.pyplot as plt

terrain_colors = {
    'none':'#000000a0',
    'snow':'#ece7f2a0',
    'ice':'#e5f5f9a0',
    'plains':'#a8ddb5a0',
    'forest':'#669973a0',
    'mountain':'#8d8d8da0',
    'desert':'#ffffcca0',
    'fields':'#8c9966a0',
    'swamp':'#998066a0'
}

settlement_types = {
    'city':{
        'size': 1,
        'ec': '#00000070',
        'fc': '#8d8d8d'
    },
    'village':{
        'size': .3,
        'fc': '#777777',
        'ec': '#00000055'
    }
}

class hex(object):
    def __init__(self, x1, x2, s=1, c='plains', settlement=None, name=None, road=False):
        self.x1 = x1
        self.x2 = x2
        self.s = s
        self.c = c
        self.settlement = settlement
        self.name = name
        self.road = road

    def get_x_pos(self):
        return (self.x1+self.x2/2) * np.sqrt(3) * self.s

    def get_y_pos(self):
        return self.x2 * 3 / 2 * self.s

    def get_pos(self):
        return (self.get_x_pos(), self.get_y_pos())

    def get_coord(self):
        return (self.x1, self.x2)

    def hex_corner(self, i):
        angle_deg = 60 * i + 30
        angle_rad = np.pi / 180 * angle_deg
        return [
            self.get_x_pos() + self.s * np.cos(angle_rad),
            self.get_y_pos() + self.s * np.sin(angle_rad)
        ]

    def hex_side(self, i):
        s1 = self.hex_corner(i)
        s2 = self.hex_corner(i + 1)
        return [
            (s1[0]+s2[0])/2,
            (s1[1]+s2[1])/2
        ]

    def to_poly_list(self):
        pts = [self.hex_corner(i) for i in range(0,6)]
        return pts

    def to_poly(self):
        return plt.Polygon(
            self.to_poly_list(),
            edgecolor='#aaaaaa',
            closed=True,
            fill=True,
            fc=terrain_colors[self.c]
        )

    def distance_to(hex):
        ac = hex_to_cube(a)
        bc = hex_to_cube(b)
        return (abs(self.x1 - hex.x1)
                    +abs(self.x2 - self.x2)
                    +abs(-self.x1-self.x2+hex.x1+hex.x2)
                )/2

    def plot(self):
        plt.gca().add_patch(self.to_poly())
        plt.annotate(
            "{:2},{:2}".format(self.x1,self.x2),
            xy = (self.get_x_pos(), self.get_y_pos()),
            ha = 'center',
            va = 'center',
            color = '#00000020'
        )

        # settlements
        if isinstance(self.settlement, str):
            plt.gca().add_patch(
                plt.Circle(
                    (self.get_x_pos(), self.get_y_pos()),
                    settlement_types[self.settlement]['size']/2,
                    fc=settlement_types[self.settlement]['fc'],
                    lw=4,
                    aa=True,
                    fill = True,
                    ec=settlement_types[self.settlement]['ec'],
                    zorder = 2
                )
            )
            plt.annotate(
                self.name,
                xy = (self.get_x_pos(), self.get_y_pos()),
                fontsize = 14,
                xytext=(0,1),
                ha = 'center',
                va = 'center',
                bbox=dict(boxstyle="round", fc="#ffffff55", ec='#ffffff00')
            )


class hexmap(object):
    def __init__(self, hlist=[]):
        self.hexlist = hlist
        self.roadlist = []

    def add(self, gridpoint: hex):
        self.hexlist.append(gridpoint)
        if gridpoint.road:
            pos = gridpoint.get_pos()
            coord = gridpoint.get_coord()
            self.roadlist.append([coord, pos])
            #print("added road at pos {}, with coordinates {}".format(pos,coord))

    def get_road_pos(self):
        x = []
        y = []
        for e in self.roadlist:
            x.append(e[1][0])
            y.append(e[1][1])

        return (x,y)
