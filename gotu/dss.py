"""de Sitter Space

It's a ball, expanding and contracting, like an Escher drawing.

Are gamma-ray bursts optical illusions?

Robert S Mackay, Colin Rourke.

https://pjm.ppu.edu/paper/247

The paper describes the relationships between pairs of geodesics in de
Sitter Space.

One geodesic corresponds to the path of a distant galaxy and the other
a receiver geodesic.

Each emitter arrives in our visible universe highly blue shifted, then
becomes increasingly red-shifted as time goes by.

The actual blue shift period and full details depend on two
parameters, phi and theta.

phi corresponds to the minimum distance between the receiver and
emitter, in other words, the emitter's closest point of approach.

theta measures the angle of approach.



"""

# we are going to need this
import random
import math
import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate
from traceback import print_exc

import curio

from blume import magic
from blume import magic
from blume import farm as fm

class Dss(magic.Ball):

    def __init__(self):
        """ initialise """
        super().__init__()

        self.theta = 0.1
        self.phi = 5
        self.size = 50
        self.aaa = magic.modes
        
        self.alpha, self.beta, self.gamma, self.delta = (1,1,1,1)

    def set_abcd(self):

        self.a = (self.alpha + self.beta - self.gamma - self.delta) / 2
        self.b = (self.alpha - self.beta - self.gamma + self.delta) / 2
        self.c = (self.alpha + self.beta + self.gamma + self.delta) / 2
        self.d = (self.alpha - self.beta + self.gamma - self.delta) / 2
        

    def constraints(self):

        print(self.alpha**2 - self.gamma**2 >= 1.)

        print(self.alpha > 0)

        a, b, c, d = self.alpha, self.beta, self.gamma, self.delta

        print((a * b - c * d) <= (a*a - c*c - 1) * (b*b - d*d -1))

        print((a*d - b*c) <= (a*a - c*c - b*b + d*d -1))

    def blue_shift_time(self, alpha=None, delta=None):
        """ """
        a = alpha or self.alpha
        d = delta or self.delta

        sqrt = math.sqrt
        etb = sqrt((1+a)/(a+d)) + sqrt((1-d)/(a-d))
        
        return math.log(etb)

    def time_until_red_shift_matches_expected_for_distance(self, error=0):
        """ Curious how this value varies with phi and theta """
        raise NotImplemented        

    def time_until_red_shift_turns_light_into_microwaves(self, error=0):
        """ Curious how this value varies with phi and theta """
        raise NotImplemented        


    def deSitter(self):

        pass


    async def run(self):

        size = self.size
        epsilon = 1e-3

        img = np.zeros((size, size))

        for row in range(1, size+1):

            delta = math.cos(math.pi * row/(size+1))
            for col in range(1, size+1):
                alpha = math.cosh(self.phi * col/(size+1))

                try:
                    img[row-1][col-1] = self.blue_shift_time(
                        alpha or epsilon, delta or epsilon)
                except:
                    print_exc()
                    print(alpha, delta)
                    raise
 
            #print(img[row-1])

            await curio.sleep(0)

        ax = await self.get()
        
        aximg = ax.imshow(img, cmap=magic.random_colour())
        ax.figure.colorbar(aximg)

        ax.show()


async def run():

    dss = Dss()

    dss.set_abcd()
    dss.constraints()

    farm = fm.Farm()
    
    farm.add(dss)
    
    await farm.start()

    print(dss.deSitter())

    farm.shep.path.append(dss)

    await farm.run()
        

if __name__ == '__main__':

    # theta distributed as cos(theta) * delta_theta
    theta = math.cos(random.random() * math.pi) * math.pi
    # phi distributed as sinh ** 2 * delta_phi
    phi = None

    thetas = np.array([math.cos(theta * math.pi * xx) for xx in range(1, 1000)])

    shines = np.array([math.sinh(x/100) ** 2 for x in range(1,1000)])

    weights = integrate.cumulative_trapezoid(shines, initial=0)
    plt(weights)
    plt.show()
    0/1

    wm = False
    curio.run(run(), with_monitor=wm)
