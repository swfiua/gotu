"""Where Is The Sun?

This turns out to be part of this mystery in our story.

Of course, we know where the Sun is, but where is it in relation to
the rest of our galaxy?

Where is the centre of our own galaxy, the Milky Way?

The conventional wisdom is that Sagittarius A* is an impressive sized
black hole, around 4 million times the mass of our sun.

Impressive though this is, it is nowhere near large enough to drive a
good sized spiral galaxy.

A mass of tens if not hundreds of billions times the mass of the sun
is required.

Let's see if astropy can help.

Astropy
=======

It seems astropy can help a great deal.  

It is not long before we encounter coordinate reference frames.

A coordinate or frame in the Geocentric Celestial Reference System (GCRS).

Running help(coordinates.GCRS) lead me to this link:

https://arxiv.org/abs/astro-ph/0602086

It is a wonderful paper discussing the subtleties of celestial frames
of reference.   

Earth based astronomy is very interested in how the earth rotates and
moves, but is also vey interested in the whole solar system as that
has an impact on how the earth moves.

The GCRS reference introduces different ways to measure time: the
earth's rotation versus the vibration of an atomic clock.

If we ignore time, briefly, GCRS introduces a geocentric coordinate
system for space.  There is a related reference system called ICRS, which is centred 

The positions of a catalogue of distant fixed stars is used to define
a fixed frame in space, centered on earth at a point in time.

Our observations are now of such precision that a tiny wobble, or
nutation, of the earth as it spins on its axis, needs to be taken into
account to make observations.  It is possible to predict this nutation
out some considerable time into the future (???).

"""
import math

from collections import deque

from astropy import coordinates, constants, time

from datetime import datetime, timedelta

from matplotlib import pyplot

import argparse

from blume import magic, farm



def get_args():
    """ A parser for command line arguments

    
    Returns an `argparseArgumentParser`
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--planets', action='store_true')
    parser.add_argument('--fontsize', type=int, default=6)
    parser.add_argument('--inc', type=float)
    parser.add_argument('--log', action='store_true')
    parser.add_argument('--rotate', action='store_true')

    return parser.parse_args()

def get_body(name, at=None):
    """ astropy helper function to get a body.

    astropy needs one of its time.Time() objects as a time.

    Here we hope at is something it understands and if None,
    then we just use our current time according to datetime.
    """
    
    if at is None:
        at = datetime.now()

    return coordinates.get_body(name, time.Time(at))

class SolarSystem(magic.Ball):
    """Visualise the solar system 

    `astropy` has all the data

    This magic.Ball just needs to get the data and plot it in various
    frames of reference.

    For now, it trecks through time plotting planets and the moon.

    It is now at least at the point where it can be used to find
    planets in the night sky.

    """

    def __init__(self, args):

        super().__init__()

        
        self.__dict__.update(vars(args or get_args()).items())

        self.now = time.Time(datetime.now())

        self.modes = deque(['icrs', 'gcrs'])
        self.views = deque(['mollweide', 'polar'])

        sun = get_body('sun', self.now)

        print(f"The time is {self.now}")
        print("The sun is:")
        print(sun)

        self.radii.add_filter('N', self.reset)

    async def reset(self):
        """ Reset the time to now """

        self.now = time.Time(datetime.now())

    async def run(self):
        """ Create a plot based on current time """

        names = 'sun earth moon'.split()

        planets = 'mercury venus mars jupiter saturn'.split()

        if self.planets:
            names += planets

        mode = self.modes[0]
        view = self.views[0]
        if self.rotate:
            if  mode == 'gcrs':
                self.views.rotate()
            self.modes.rotate()

        ax = pyplot.subplot(projection=view)

        for name in names:

            body = get_body(name, self.now)

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
                if self.log and dist:
                    dist = math.log(dist)
                pyplot.plot([ra], [dist], 'o', label=label)
            else:
                pyplot.plot([ra], [dec], 'o', label=label)

        pyplot.grid(True)
        pyplot.title(self.now)
        pyplot.legend(loc=0, fontsize=self.fontsize, title=f'{mode} {view}')
        await self.put()
        self.tick()

    def tick(self):
        """ Move the clock by inc """
        if self.inc is None:
            self.now = time.Time(datetime.now())
        else:
            self.now += timedelta(seconds=self.inc or 0)


if __name__ == '__main__':

    ss = SolarSystem(get_args())

    fm = farm.Farm()

    fm.add(ss)
    fm.shep.path.append(ss)
    farm.run(fm)

