"""Spiral Galaxies

Galactic rotation curves without dark matter.

**A new paradigm for the universe.**

https://msp.warwick.ac.uk/~cpr/paradigm

ISBN: 9781973129868

I keep dipping into this book.

Each time with new understanding.  Each time with a new perspective.

It is a wonderful work, with compelling arguments.

Chapter 2, Sciama's principle finishes with:

   Sciama's initiative, to base a dynamical theory on Mach's principle as
   formulated in Sciama's principle, has never been followed up and this
   approach to dynamics remains dormant.  One of the aims of this book is to
   reawaken this approach.

One of the aims of `blume` is to help understanding of such theories.

In particular, help my own understanding with computer simulations.

This project will explore some of the mathematics of the book.

It will require `astropy`.  

Solar system, galactic and local galaxy visualsation and simulation.

Simulation of gravitational waves generated by black hole mergers using the
physics of *the book*.

Simulations of gravitational wave from a new galactic arrival.

2021 update
===========

The Geometry of the Universe

Colin Rourke

https://www.worldscientific.com/worldscibooks/10.1142/12195

ISBN: 978-981-123-386-9 (hardcover)

A new book, with a bold claim.  A stunning story, a revival of some
old ideas and new brilliance too.


Spiral
======

Spiral galaxies?  Why spirals?

The problem noted by observational scientist Vera Rubin was that stars
in the outer reaches of spiral galaxies are moving far too fast.

This observation is what lead to the dark matter assumption: there
must be some matter we can't see that is dragging the stars along.

Colin Rourke, says nonesense, there must be a giant rotating mass at
the centre, dragging things along.


Einstein's general relativity withstands double pulsar's Scrutiny
=================================================================

https://physics.aps.org/articles/v14/173

Strong-Field Gravity Tests with the Double Pulsar

M. Kramer et al.

Phys. Rev. X 11, 041050 (2021)

Published December 13, 2021

Binary pulsars provide strong tests of general relativity.  The idea
is that there are two, rapidly rotating, neutron stars in a close
orbit around each other.

The Hulse-Taylor binary system has long been the best observed system
and the strongest test.

A new system *PSR J0737-3039A/B* has now taken that crown as the best
observed system.  Lets call it Jumb0 737, from the J designate, or
Jumbo for short.

The rotations of the Jumbo are incredibly stable, at the level of an
atomic clock, allowing very precise measurements of the time delays of
the pulses of energy as the system makes each rotation.

In addition, Jumbo is nearer than the Hulse-Taylor system and there is
much less uncertainty in our estimate of its distance from earth.

It all gets complicated, since as although the system is in our own
galaxy, the intervening spacetime modulates the signal we receive.

The new paper explains the precise measurements that can now be made
and how variations on general relativity, can, in some cases, be
tested.

In particular, the paper now mentions that rotation of the faster
rotating body now has to be taken into account in the equations of
state of the entire system.  The other body is rotating around one
hundred times slower so the effect can largely be ignored.

The aproach that is taken is to assume the Lense-Thiring effect.  

This is discussed in some detail in chapter 3 of the book, *the
biggest blunder...*.  Particular attention should be paid to the
discussion around page 60.

There are some quite technical arguments.  The Lense Thiring effect is
intuitively compelling.  General relativity tells us that if
*space-time is a vacuum*, then the Kerr metric is the only solution
that fits Einstein's equations.

This is problematic for the book's arguments as the Kerr metric falls
off as 1/(r**3) whereas the book argues it should fall off as 1/r.

Rourke makes the assumption that linear motion has no inertial effect
and notes that you can change angular momentum by adding a linear
motion, whereas angular velocity cannot be changed in this way.

Is space time a vacuum?
-----------------------

The impasse is resolved if we assume that space is not in fact a
vacuum.

For starters, there is an awful lot of microwave radiation buzzing
around:  the cosmic microwave background.

The nature of this background depends critically on our assumptions
about the geometry of the universe: big bang, or static universe?

What would a static universe look like given the effects of special
relativity, simplifying a universe to the set of galaxies above a
certain size?

This model will instead show how by assuming this 1/r relation for the
effect of a masses rotation on its surroundings, produces galactic
rotation curves very much in line with observations.

What about Jumbo?
=================

So the cool news is that we now get estimates of the angular velocity
of each body and it's moment of inertia.

The latter adds some uncertainty to model fit as there is uncertainty
of the exact distribution of the matter within each neutron star,
which is important to know, as the model being used assumed it is
angular momentum that drives the rotational frame dragging.

As noted above, Rourke argues that it is angular velocity, rather than
angular momentum that matters in the calculation, in short the matter
distribution within the black hole is not required for his model.

Further, that the Lense-Thiring effect drops off as 1/r, not the
1/r**3 that is presumably being used by the new paper.  Unless the
orbits are highly oblique, this difference is not going to be
detectable with a single system.

This should mean that a fit using Rourke's model reduces the
uncertainty in all the parameters that the fitting process estimates,
since the uncertainty in the matter distribution no longer comes into
play, just the uncertainty in angular velocity.

Another project would be to fit the model to the latest Hulse-Taylor
data and see what changes.

I am also curious how Rourke's model affects the long term evolution
of these systems.  My hunch (actually I think I read something along
these lines in the book) is that the feedback from the rotation keeps
these binary systems stable and that it is highly improbable that they
will in-spiral and coalesce.   

Which raises the interesting question of what is the source of the
waves that our gravitational wave detectors are seeing?   

Which reminds me, I need to work on the grb module.


What about the spiral module?
=============================

The idea is to create a visualisation of the formation of spiral
galaxies with a *\omega m / r* model.

It would be good to also be able to model binary systems while we are at it.

"""

import argparse

import random

import math

from collections import deque

import astropy.units as u
import astropy.constants as constants
import astropy.coordinates as coord

from blume import magic
from blume import farm as fm
from blume import taybell

from matplotlib import pyplot as plt
from matplotlib import colors

import numpy as np

from scipy import integrate


class SkyMap(magic.Ball):
    """ Yet another table viewer? 

    parsing csv and figuring out what it means.

    or just give me lists of fields i can pick form for
    any purpose?

    Or yet another universe viewer.

    And so we descend into the world of coordinate systems.

    Something astronomers understand very well.
    
    See :mod:`gotu.wits` for more on this subject.

    Maybe SkyMap allows systems to evolve over time, according to the paradigm.

    """

    def __init__(self, gals):

        super().__init__()

        print('clean galaxy data')
        print(len(gals), type(gals[0]))
        print(gals[0])

        self.balls = gals
        self.sleep=1.0
        self.offset = 0.

        

    def decra2rad(self, dec, ra):

        return math.radians(dec), math.radians(ra)

        ra = (ra - 12) * math.pi / 12.

        while ra > math.pi:
            ra -= 2 * math.pi
        
        return dec * math.pi / 180., ra
        

    def spinra(self, ra):

        ra += self.offset
        while ra > math.pi:
            ra -= 2 * math.pi

        while ra < math.pi * -1:
            ra += 2 * math.pi

        return ra
        
    async def run(self):

                
        #ax = fig.add_axes((0,0,1,1), projection='mollweide')
        ax = await self.get()
        ax.projection('mollweide')

        locs = [self.decra2rad(ball['DEC'], ball['RA'])
                    for ball in self.balls]

        ball_colours = [x['DISTANCE'] for x in self.balls]

        ax.set_facecolor('black')
        ax.scatter([self.spinra(xx[1]) for xx in locs],
                   [xx[0] for xx in locs],
                   c=ball_colours,
                   s=[x['BMAG'] or 1 for x in self.balls])

        ax.axis('off')

        ax.show()


class Spiral(magic.Ball):
    """  Model a spiral galaxy

    Or any rotating mass?

    Want to convert this to use astropy units.
    """

    def __init__(self):

        super().__init__()

        self.modes = deque(
            ('galaxy', 'sun'))

        # set up an initial mode
        self.mode = None
        self.mode_switch()

        self.details = True

    def galaxy(self):
        """ Set parameters for a galaxy """
        print('Galaxy!' * 6)
        # A = K * \omega_0.  K = M for Sciama principle
        self.A = 0.0005

        # Apparent rate of precession of the roots of the spiral.
        self.B = 0.00000015

        # Central mass.  Mass converted to Schwartzschild radius (in light years)
        # Mass of 1 is approximately 3e12 solar masses.
        self.Mcent = 0.03
        self.Mball = 0.
        self.Mdisc = 0.

        self.K = self.Mcent
        self.omega0 = self.A / self.K   # angular velocity in radians per year

        # magic constant determined by overall energy in the orbit
        self.EE = -0.00000345

        # constant, can be read from tangential velocity for small r
        self.CC = -10

        # range of radius r to consider, in light years
        self.rmin = 5000
        self.rmax = 50000

        self.print_parms()
        print()

    def sun(self):

        print('SUN!' * 10)
        solar_mass = 1
        solar_angular_velocity = 2 * math.pi / 25  # radians per year
        
        # Central mass.  Mass converted to Schwartzschild radius (in light years)
        # Mass of 1 is approximately 3e12 solar masses.
        self.Mcent = solar_mass
        self.Mball = 0.
        self.Mdisc = 0.
        self.omega0 = solar_angular_velocity # radians per year

        # astronomical unit in light years
        # au = 1 / 63241.08  ### can't remember how I calculated this
        auasly = u.au.to(u.lightyear)
        
        self.rmin = 0.1 * auasly
        self.rmax = 50 * auasly

        self.K = self.Mcent

        # solar wind goes from 30 km/s at 3 AU to 500 km/s at 40 AU
        # so set A to 2 * 500 km/s in our units
        # ??

        # A = K * \omega_0.  K = M for Sciama principle
        # want 2 * A to be 
        self.A = self.K * solar_angular_velocity

        # magic constant determined by overall energy in the orbit
        self.EE = 5.6e10


        # constant, can be read from tangential velocity for small r
        self.find_cc(tangential_velocity=self.rmin * self.omega0)
        #self.CC = -0.1

        # Apparent rate of precession of the roots of the spiral.
        self.B = self.A / self.rmin

        self.omega0 = self.A / self.K   # angular velocity in radians per year

        self.print_parms()
        print()

    def print_parms(self):
        
        print('omega0', self.omega0)
        print('CC', self.CC)
        print('A/K', self.A / self.K)
        print('rmin_check', self.rmin_check())
        

    
    def find_cc(self, tangential_velocity):

        # constant, can be read from tangential velocity for small r
        A, K, r = self.A, self.K, self.rmin

        print(r, K, r/K)
        
        tv = (2 * A) - (2 * A *K) * math.log((r/K) + 1)

        self.CC = tangential_velocity - tv
        print('tv', tangential_velocity, self.CC, tv)

        return self.CC

    def rmin_check(self):
        """ The length of the roots of the spirals 

        This can be used to set the B value.

        Assume that the spiral roots end at radius r0

        And assume the roots are moving with the inertial frame at that
        radius.

        The rate of precession will match that of the inertial frame at
        that radius.

        """
        return self.A / self.B


    def v(self, r):
        """ Velocity at radius r 

        A = 0.0005
        K = Mcent
        CC = -10

        ??
        """
        A = self.A
        K = self.K
        CC = self.CC

        return (2 * A) - (2 * K * A * math.log(1 + K) / r) + CC / r


    def vinert(self, r, v):
        """ Inertial part of the velocity

        Part of velocity relative to inertial frame.

        Notes
        -----

        K is central mass.   A = 0.0005
        """
        return v - (self.A * r) / (self.K + r)

    def rdoubledot(self, r, vinert):

        rdd = ((vinert ** 2) / r) - (self.Mcent/(r**2))

        # if we have Mdisc of Mball, adjust as appropriate?
        rdd -= self.Mdisc/(self.rmax ** 2)
        rdd -= self.Mball * r /(self.rmax ** 3)

        return rdd

    def energy(self, r):

        CC = self.CC
        Mcent = self.Mcent
        Mdisc = self.Mdisc
        Mball = self.Mball
        rmax = self.rmax
        EE = self.EE
        K = self.K
        A = self.A
        Log = math.log

        # ok this deserves an explanation!
        energy = (-CC**2/(2*r**2) + (Mcent - 2*A*CC)/r -
                    # adjustment for a uniform disk radius rmax, mass Mdisc
                    Mdisc*r/rmax**2 +
                    # adjustment for a spherical mass
                    Mball*r**2/(2*rmax**3) +
                    # 
                    A**2*K/(K + r) +
                    A**2*Log(K + r) +
                    2 * A*K * (CC + 2*A*r) * Log(1 + r/K)/(r**2)
                    - (2 * A*K*Log(1 + r/K)/r)**2 + EE);
        
        return energy

    def mode_switch(self):

        if self.mode != self.modes[0]:
            self.mode = self.modes[0]
            print('switching mode', self.mode)
            # run the mode
            getattr(self, self.mode)()

    
    async def run(self):

        # switch mode if it is time to do so
        self.mode_switch()

        rr = np.arange(self.rmin, self.rmax, 100)
        #vv = [self.v(r) for r in rr]
        vv = self.v(rr)
        ii = self.vinert(rr, vv)
        rdd = self.rdoubledot(rr, ii)
        energy = np.array([self.energy(r) for r in rr])
        #ii = [self.vinert(r, v) for (r, v) in zip(rr, vv)]
        #rdd = [self.rdoubledot(r, v) for (r, v) in zip(rr, ii)]
        rdot = np.sqrt(2 * energy)
        print('energy', max(energy), min(energy))
        #print('spiral', len(rr), len(rdot))

        if self.details:
            ax = await self.get()
            ax.plot(rr, vv, label='velocity')
            ax.plot(rr, ii, label='vinert')
            ax.plot(rr, rdot, label='rdot')
            #ax.plot(rr, energy, label='energy')
            ax.legend(loc=0)
            ax.show()

            ax = await self.get()
            ax.plot(rr, rdd, label='rdoubledot')
            ax.legend(loc=0)
            ax.show()

        thetadot = vv/rr;

        dthetabydr = thetadot/rdot 
        dtbydr = 1/rdot

        NIntegrate = integrate.cumtrapz

        thetaValues = NIntegrate(dthetabydr, rr, initial=0.)
        tvalues = NIntegrate(dtbydr, rr, initial=0.)


        B = self.B
        ax = await self.get()
        # fixme - want polar projections - wibni this worked?
        ax.projection('polar')
        ax.plot(thetaValues - (B * tvalues), rr)
        ax.plot(thetaValues - (B * tvalues) + math.pi, rr)
        ax.axis('off')
        ax.show()


def pick(x, v, vmin, vmax):

    n = len(v)
    loc = n * (x - vmin) / vmax

    return v[loc]


def cpr():
    """  Started as Mathematica code from the new paradigm.
    
    adapted to python over time.

    See spiral class for more information over time.
    """

    Plot = plt.plot
    Log = np.log
    Sqrt = np.sqrt
    NIntegrate = integrate.cumtrapz
    
    A = 0.0005; Mcent = .03; EE = -.00000345; CC = -10;
    B = .00000015; Mball = 0; Mdisc = 0; K = Mcent;
    rmin = 5000; rmax = 50000; iterate = 1000;
    
    step = (rmax - rmin)/(iterate - 1)

    r = np.arange(rmin, rmax)

    ax = plt.subplot(121)

    v = 2*A - 2*K*A*Log(1 + r/K)/r + CC/r
    inert = v - A*r/(K + r);
    ax.plot(r, v, label='velocity')
    ax.plot(r, inert, label='vinert')
    
    rdoubledot = inert**2/r - Mcent/r**2 - Mdisc/rmax**2 - Mball*r/rmax**3
    ax.plot(r, rdoubledot, label='rdoubledot')

    energy = (-CC**2/(2*r**2) + (Mcent - 2*A*CC)/r -
                  Mdisc*r/rmax**2 +
                  Mball*r**2/(2*rmax**3) +
                  A**2*K/(K + r) +
                  A**2*Log(K + r) +
                  2 * A*K * (CC + 2*A*r) * Log(1 + r/K)/(r**2)
                  - (2 * A*K*Log(1 + r/K)/r)**2 + EE);
    #Plot(energy, r, label='energy')
    rdot = Sqrt(2*energy)

    ax.plot(r, rdot, label='rdot')

    ax.legend(loc=0)
    
    thetadot = v/r;
    dthetabydr = thetadot/rdot 
    dtbydr = 1/rdot

    
    thetaValues = NIntegrate(dthetabydr, r, initial=0.)
    print(thetaValues)
    print(len(thetaValues))

    tvalues = NIntegrate(dtbydr, r, initial=0.)

    #thetavalues = Table(
    #    NIntegrate(dthetabydr, rmin, rmax), ivalue, i, iterate))
    #tvalues = Table(
    #    NIntegrate(dtbydr, r, ivalue, i, iterate))
    
    #ListPolarPlot[{ Table[{thetavalues[[i]] - B*tvalues[[i]], ivalue},
    #{i, iterate}] ,
    #Table[{thetavalues[[i]] - B*tvalues[[i]] + Pi, ivalue},
    #{i, iterate}] }]

    print('theta', thetaValues[:5])
    ax = plt.subplot(122, projection='polar')
    ax.plot(thetaValues - (B * tvalues), r)
    ax.plot(thetaValues - (B * tvalues) + math.pi, r)

    values = (thetaValues - (B * tvalues))
    print(min(values), max(values))
    return rdot, inert, v, values


def near_galaxies():
    """ parse galaxy.txt from 

    https://heasarc.gsfc.nasa.gov/w3browse/all/neargalcat.html

    """
    from astroquery import heasarc
    from astropy import coordinates

    heas = heasarc.Heasarc()

    coord = coordinates.SkyCoord('12h00m00 + 0d0m0s', frame='gcrs')
    table = heas.query_region(
        mission='heasarc_neargalcat',
        position=coord,
        radius='360 deg')

    for item in table:
        yield item

    print(item.keys())


def parse_radec(value):

    d, m, s = [float(s) for s in value.split()]

    scale = 1
    if d < 0:
        d *= -1
        scale = -1

    d += m / 60.
    d += s / 3600.

    return d * scale
    
def cleanse(data):

    clean = {}

    for key in data.keys():
        value = data[key]
        try:
            value = float(value)
        except:
            pass

        if key.lower() in ('ra', 'dec'):
            print(key, value)
            value = parse_radec(value)
            
        clean[key] = value

    return clean

async def run(**args):

    farm = fm.Farm()

    if args['skymap']:
        gals = list(near_galaxies())
        skymap = SkyMap(gals)
        farm.add(skymap)
    
    spiral = Spiral()
    farm.add(spiral)
    farm.shep.path.append(spiral)
    await farm.start()
    print('about to run farm')
    await farm.run()


def main(args=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--skymap', action='store_true')

    args = parser.parse_args(args)

    magic.run(run(**args.__dict__))



if __name__ == '__main__':

    
 
    #cpr()
    #plt.show()
    main()
