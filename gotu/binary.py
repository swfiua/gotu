"""
Try to simulate a binary system.



"""


import math
from collections import deque

from astropy import units, constants

from blume import magic, farm

from .spiral import SkyMap, Spiral

class Binary(magic.Ball):

    def __init__(self):
        """Initialise binary system.

        Assume two roughly equal sized masses orbitting each other.

        FIXME: just inialise a couple of Spiral's and introduce them
        to each other.

        The plan is to turn Spiral into something that will simulate
        and visualise what the induced gravitational field might look like.

        
        """

        # initial state
        kms = units.km / units.second
        
        self.m1 = 0.5 * units.solMass
        self.m2 = 0.5 * units.solMass
        self.r1 = [100000 * units.au, 0 * units.au]
        self.r2 = [-100000 * units.au, 0 * units.au]
        self.v1 = [0 * kms, 0.4 * kms]
        self.v2 = [0 * kms, -0.4 * kms]

        # number of days for bodies to rotate.
        n1 = n2 = 27
        self.w1 = (math.pi * 365 / n1) * units.rad / units.year
        self.w1 = (math.pi * 365 / n2) * units.rad / units.year

        self.t = 0
        self.inc = 100

        self.mode = deque(('Newton', 'cpr'))

    def step(self):

        # Do one step of the system first need Newtonian, then add
        # rotations?  Assume that the rate of precession of the
        # inertial frame matches that of the binary system -- ie there
        # is essentially zero angular momentum when masses are
        # furthest apart, all velocity is rotational.

        # in fact, it is only necessary for the excess velocity
        # the system has to be within the rotational frame dragging

        v = self.v1[1].to(units.m/units.second)
        r = (self.r1[0] * 2).to(units.m)
        
        m = self.m1.to(units.kg)

        print(constants.G)
        newton = constants.G * m * m / (r * r)

        print(newton / m)
        #print(v)
        #print(r)
        print(0.5 * v * v / r)


if __name__ == '__main__':

    bb = Binary()
    bb.step()
