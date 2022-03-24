"""
Try to simulate a binary system.
"""

from blume import magic, farm

from astropy import units, constants

class Binary(magic.Ball):

    def __init__(self):
        """ Initialise binary system.

        Assume two roughly equal sized masses orbitting each other.

        
        """

        # initial state
        self.m1 = 0.5 * units.solMass
        self.m2 = 0.5 * units.solMass
        self.r1 = [100000 * units.au, 0 * units.au]
        self.r1 = [-100000 * units.au, 0 * units.au]
        self.v1 = [0 * units.kms, 0.4 * units.kms]
        self.v2 = [0 * units.kms, -0.4 * units.kms]

        # number of days for bodies to rotate.
        n1 = n2 = 27
        self.w1 = (math.pi * 365 / n1) * units.rad / units.year
        self.w1 = (math.pi * 365 / n2) * units.rad / units.year

        self.t = 0
        self.inc = 100

        self.mode = deque('Newton', 'cpr')

    def step(self):

        # Do one step of the system first need Newtonian, then add
        # rotations?  Assume that the rate of precession of the
        # inertial frame matches that of the binary system -- ie there
        # is essentially zero angular momentum when masses are
        # furthest apart, all velocity is rotational.

        # in fact, it is only necessary for the excess velocity
        # the system has to be within the rotational frame dragging

        v = self.v1[1]
        r = self.r1[0] * 2
        
        
