"""Where Is The Sun?

This turns out to be part of this mystery.

We know where the sun is, but where is it in relation to the centre of
our galaxy?

Specifically, the centre of our own galaxy, the milky way?

The conventional wisdom is that Sagittarius A* is an impressive sized
black hole, around 4 million times the mass of our sun.

Impressive though this is, it is nowhere near large enough to drive a
good sized spiral galaxy.

A mass of tens if not hundreds of billions times the mass of the sun
is required.

Let's see if astropy can help.

"""
import math

from collections import deque

from astropy import coordinates, constants, time

from datetime import datetime, timedelta

from matplotlib import pyplot

import argparse

from blume import magic, farm



def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--planets', action='store_true')
    parser.add_argument('--fontsize', type=int, default=6)

    return parser.parse_args()

def get_body(name, at=None):

    if at is None:
        at = datetime.now()

    return coordinates.get_body(name, time.Time(at))

class SolarSystem(magic.Ball):

    def __init__(self, args):

        super().__init__()

        
        self.__dict__.update(vars(args or get_args()).items())

        self.inc = 3600
        self.now = time.Time(datetime.now())

        self.modes = deque(['icrs', 'gcrs'])
        self.views = deque(['mollweide', 'polar'])

        sun = get_body('sun', self.now)

        print(f"The time is {self.now}")
        print("The sun is:")
        print(sun)

        self.radii.add_filter('N', self.reset)

    async def reset(self):

        self.now = time.Time(datetime.now())

    async def run(self):
        

        # do some more
        names = 'sun earth moon'.split()

        planets = 'mercury venus mars jupiter saturn'.split()

        if self.planets:
            names += planets

        #ax = pyplot.subplot()
        mode = self.modes[0]
        view = self.views[0]
        if view == 'polar':
            ax = pyplot.subplot()
        else:
            ax = pyplot.subplot(projection = view)
            

        for name in names:

            body = get_body(name, self.now)
            #print(name)
            #print(body)
            #print()

            if mode == 'gcrs':
                bod = body.gcrs
            else:
                bod = body.icrs

            ra, dec = bod.ra.rad, bod.dec.rad
            if ra > math.pi:
               ra = ra - (2 * math.pi)

            dra, ddec, dist = bod.ra.deg, bod.dec.deg, bod.distance.au
            label = f'{name} {dra:.0f} {ddec:.0f} {dist:0.2f}'

            if view == 'polar':
                pyplot.polar([ra], [dist], 'o', label=label)
            else:
                pyplot.plot([ra], [dec], 'o', label=label)

        #c = patches.Ellipse((.5, .5), .1, .1)
        #print(c)
        #ax.add_patch(c)
        pyplot.grid(True)
        pyplot.title(self.now)
        pyplot.legend(loc=0, fontsize=self.fontsize)
        await self.put()
        self.tick()

    def tick(self):

        self.now += timedelta(seconds=self.inc)



if __name__ == '__main__':

    ss = SolarSystem(get_args())

    fm = farm.Farm()

    fm.add(ss)
    fm.shep.path.append(ss)
    farm.run(fm)

