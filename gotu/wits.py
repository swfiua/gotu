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

from astropy import coordinates, constants, time

from datetime import datetime

import argparse

from matplotlib import patches, pyplot

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--planets', action='store_true')

    return parser.parse_args()

def get_body(name, at=None):

    if at is None:
        at = datetime.now()

    return coordinates.get_body(name, time.Time(at))

def main(args=None):

    args = args or get_args()

    now = time.Time(datetime.now())

    sun = coordinates.get_sun(now)

    print(f"The time is {now}")
    print("The sun is:")
    print(sun)

    # do some more
    names = 'sun earth moon'.split()

    planets = 'mercury venus mars jupiter saturn'.split()

    if args.planets:
        names += planets

    #ax = pyplot.subplot()
    ax = pyplot.subplot(projection = 'mollweide')

    for name in names:

        body = coordinates.get_body(name, now)
        print(name)
        print(body)
        print()

        ra, dec = body.ra.rad, body.dec.rad
        if ra > math.pi:
           ra = ra - (2 * math.pi)

        label = f'{name} {body.ra.deg:.0f} {body.dec.deg:.0f}'
        pyplot.plot([ra], [dec], 'o', label=label)

    #c = patches.Ellipse((.5, .5), .1, .1)
    #print(c)
    #ax.add_patch(c)
    pyplot.grid(True)
    pyplot.legend(loc=0)
    pyplot.show()



if __name__ == '__main__':

    main()

