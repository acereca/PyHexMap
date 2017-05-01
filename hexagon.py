import numpy as np
import matplotlib.pyplot as plt

terrain_colors = {
    'snow':'#ece7f2',
    'ice':'#e5f5f9',
    'plains':'#a8ddb5',
    'forest':'#669973',
    'mountain':'#8d8d8d',
    'desert':'#ffffcc',
    'fields':'#8c9966',
    'swamp':'#998066'
}

settlement_types = {
    'city':{
        'size': 1,
        'ec': '#000000ff',
        'fc': '#8d8d8d'
    },
    'village':{
        'size': .3,
        'fc': '#777777',
        'ec': '#00000055'
    }
}

class hex(object):
    def __init__(self, x1=0, x2=0, s=1, c='plains'):
        self.x1, self.x2, self.s, self.c = x1,x2,s,c

    def get_x_pos(self):
        return (self.x1+self.x2/2) * np.sqrt(3) * self.s

    def get_y_pos(self):
        return self.x2 * 3 / 2 * self.s

    def hex_corner(self, i):
        angle_deg = 60 * i +30
        angle_rad = np.pi / 180 * angle_deg
        return [
            self.get_x_pos() + self.s * np.cos(angle_rad),
            self.get_y_pos() + self.s * np.sin(angle_rad)
        ]

    def hex_side(self, i):
        s1 = self.hex_corner(i)
        s2 = self.hex_corner(i+1)
        return [(s1[0]+s2[0])/2, (s1[1]+s2[1])/2]

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
