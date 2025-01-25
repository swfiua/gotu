"""===================================================
Is the green valley a rainbow mountain in disguise?
===================================================

There's a hill with a green chair, lined by birch, a green valley, if
you will.

It's a place I have spent much time musing about space and time.

This module is about a new mountain, where the jackets are all colours
of the rainbow.

It asks if there is in fact no valley at all, but an illusion of such
due to the assumption that redshift and distance follow an exact
Hubble law.

::

   The *green valley* is a wide region separating the blue and red
   peaks in the ultraviolet optical color magnitude diagram, first
   revealed using GALEX UV photometry.

This is how the green valley galaxies are described by the 2014 paper
of Samir Salim: https://arxiv.org/pdf/1501.01963

Here is an image and caption from the paper:

.. image:: images/samir.png

It is based on observations of distant galaxies in the ultra-violet
spectrum, specifically what is referred to as the NUV-r range.

NUV stands for Near Ultraviolet and -r, I presume, is an indication that
the frequencies have been shifted to make it look like the familiar
red to blue range in light.

In effect, the telescopes making the observations are taking the
temperature of the galaxy being observed, the hotter it is, the bluer
the result.  

It is also possible to measure the red-shift, with good precision, of
each galaxy that is observed.

Assuming an exact Hubble law, we can translate redshift into distance.

Once we have the distance, we can translate the apparent magnitude into
an absolute magnitude.

The curious observation is that across a wide range of magnitudes we
see many red galaxies and many blue galaxies, but far fewer in the
green region, a green valley if you will.

The conclusion is that there are two classes of galaxies.  Ones that
are actively forming stars and ones that are less active in forming
stars.  It is also assumed the transition from active to quiescent
galaxies happens rapidly, hence we see fewer galaxies in this stage.

Explaining the Green Valley
---------------------------

What if the relationship between redshift and distance is not in fact
exact?

There is good evidence for this from the Dark Energy Survey, based on
observations of supernovae.

In de Sitter Space the relationship only holds asymptotically.

There are galaxies both sides of the asymptote.  Here is an image that
attempts to show the relationship:

.. image:: images/zvr.png

Let us also assume that younger, smaller galaxies have a higher star
forming rate than larger, mature galaxies.

At any particular redshift we see galaxies over a wide range of
distances.  For galaxies with no redshift (z=0) it turns out that they
are most likely to be at 2/3 of the Hubble distance.

de Sitter Space is a space-time which has the Perfect Copernican
Principle: there are no special places or times in the universe.

In such a universe, there is no overall expansion.  It exhibits red
shift, but also blue shift in the form of gamma-ray bursts.

There is an asymptotic relationship between z and d.

Closer to home, there are galaxies bursting on the scene, at z=1.
Half imediately recede, the other half zoom closer.  All eventually
converge to the Hubble-law asymptote.

The Green Mountain
------------------

Now imagine what happens if this is what we are observing, but we
assume an exact Hubble law to gauge distance and size.

If a galaxy turns out to be nearer than the Hubble law would imply, we
end up over-estimating it's magnitude, since the object we are seeing is
nearer than we think.

If a galaxy is further away than the Hubble law implies, we
under-estimate it's size.

The set of galaxies that are observed varies over 7 magnitudes,
with z < 0.22.  

Our sample of galaxies that are further away than we are assuming will
be a sample of large galaxies, that we mistakenly assume are small.

The sample of galaxies that are nearer than we are assuming, will
be a sample of small galaxies that we are assuming to be large.

The galaxy model in the Geometry of the Universe proposes a
quasar-galaxy spectrum, in which small quasars grow into large
galaxies over a long period of time suggests there is a general
evolution as the central black hole grows in size.

Younger galaxies tend to be more vigorous in star formation.

In the image of the green valley, the passive sequence includes
galaxies whose size has been underestimated, they will move to the
left in the image.

The star forming sequence includes galaxies who's size has been
over-estimated.  Correcting this will move them to the right in the
picture.

The end result?  A slope of a large rainbow mountain.

I should add there is a good way to test this theory.  The supernovae
data, from the dark energy feature a growing set of galaxies for which
we have good evidence their true distance: supernovae have very
consistent brightness.

I wonder what the colour-magnitude diagram for this set of galaxies
looks like?

And how to show this in code?

Update 2025/1/25
================

To get a better feel for the redshift distance relationship in de
Sitter Space, I made a modification to the :ref:`spiral` module,
specifically to the code that creates plots of z v r, redshift against
distance, for a random sample of galaxies in de Sitter space.

The modification maps z to zdash = z / (1+z), if z < 0, zdash = z if z>=0

The idea here is that z=-1 corresponds to an infinite blue shift, so
this modification stretches the values less than zero out in the same
way that it stretches out in the same way redshift tends to infinity.

I have been experimenting with different windows of zdash.

Here is what a -10,10 zdash window looks like:

.. image:: images/trex.png

I am calling this a t-rex plot.

Zooming in to a smaller range of redshift, such as mod(zdash) < 0.22,
we see that the picture can look very different.

It then becomes very apparent why there is Hubble tension.

One bit remaining to be modelled is the visibility, or apparent
magnitude of each source.  In particular, there needs to be a factor
of 1/(z*z) applied to the magnitude to account for reduction in power
resulting from redshift.  The energy of each photon is proportional to
its frequency, as are the number arriving per unit time, resulting in
a reduction of 1/(z*z) in the magnitude of a source.

"""
# never import *, except ...
from math import *

import random

from blume import magic, farm
np = magic.np

from . import spiral

def mtod(m, M):
    """ Relationship between magnitude and distance.

    m - M = -5 + 5 * log(d)

    m apparent magnitude
    d distance in parsecs
    """
    M = m + 5 - (5 * log10(d))

def apparent_magnitude(absmag, distance):
    """ Give apparent magnitude give absolute magnitude and distance

    NB need distance in mega-parsecs.
    """
    return absmag - 5 + (5 * log10(dist))

def is_visible(magnitude, distance, zmax=0.22, minmag=-24, maxmag=-17):
    """ Can we see this magnitude at this distance?

    The Salim paper was up to z = 0.22 and
    magnitude in the range -24 to -17

    Assume magnitude -24 is just visible at z=0.22
    magnitude -17 visible at small z.
    """

    slope = zmax / (minmag - maxmag)

    visible = magnitude < maxmag + (distance * slope)
    
    return visible


class RandomSize:
    """ Return magnitude of galaxy chosen at random
    """
    def __init__(self, mins=-24, maxs=-17, bins=1000):
        self.mins = mins
        self.maxs = maxs
        self.bins = np.zeros(bins)
        
        
    def __call__(self):
        """ Return a random galaxy from our distribution """
        random(choice(list(range(len(self.bins))), weights=self.bins))



class Fortune(spiral.SkyMap):

    def __init__(self):

        super().__init__()

        self.sky = spiral.SkyMap()
        self.random_magnitude = RandomSize()

    async def xrun(self):

        # get a new sample
        self.sky.create_sample()

        for ball in self.sky.balls:
            ball.magnitude = self.random_magnitude()

            # get redshift and distance for ball
            zz, xx = ball.zandx()

            if not is_visible(ball.magnitude, xx): continue

            wavelength = self.nuvr(ball.magnitude)

            # now calculate magnitude assuming zz is distance
            

    def nuvr(self, mag):
        """ return nuv-r value for given magnitude

        Assume a straight line relationship
        """
        minmag = -24
        wavelength = 6.3 - ((mag-minmag) * 5.3/magrange)
        return wavelength
        
    async def run(self):

        self.create_sample()
        maxtheta = self.maxtheta
        mintheta = self.mintheta

        tt = 0.

        xname, yname = 'z', 'r'
        for ball in self.balls:
            t1 = time.time()
            if maxtheta or mintheta:
                maxcos, mincos = cos(maxtheta), cos(mintheta)
                # need uniform numbers in range [maxcos, mincos]
                if maxcos < mincos:
                    maxcos, mincos = mincos, maxcos
                rand = (random.random() * (maxcos-mincos)) + mincos
                ball.theta = math.acos(rand)
        
            t = ball.tstar() + self.toff

            if self.tborigin:
                t += ball.tb()

            while True:
                z, x = ball.zandx(t)

                # adjust distance for scale factor, adjust z too...
                # ie repace x by x/1+x, ditto z.
                if self.scale_for_curvature:
                    xname, yname = 'z/(1+z)', 'r/(1+r)'
                    x *= self.cosmo.scale_factor(x)
                    z *= self.cosmo.scale_factor(z)

                if z > self.tablecounts.maxx:
                    break
                if z > 0 and x > self.tablecounts.maxy:
                    break

                if z < 0:
                    z = z/(1+z)
                    #x = x/(1+x)

                #weight = 1/(x*x)
                weight = 1
                self.tablecounts.update([z], [x], weight)
                t += self.delta_t

            #print(f'{t:8.2f} {ball.theta:6.3f} {ball.phi:6.2f} {z:6.2f} {x:6.2f}')
            t2 = time.time()
            tt += t2-t1
            if tt > self.sleep:
                await self.tablecounts.show(xname=xname, yname=yname)
                tt = 0.

        # one last show
        await self.tablecounts.show(xname=xname, yname=yname)

if __name__ == '__main__':

    
    land = farm.Farm()
    land.add(Fortune())
    farm.run(land)
