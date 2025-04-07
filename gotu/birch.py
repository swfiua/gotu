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

NUV stands for Near Ultraviolet and -r, I presume, is an indication
that the frequencies have been shifted to make it look like the
familiar red to blue frequency range in light.  update: it appears in
the literature that NUV-r is taken as a good indicator of star
formation rate.

In effect, the telescopes making the observations are taking the
temperature of the galaxy being observed, the hotter it is, the bluer
the result.

It is also possible to measure the red-shift, with good precision, of
each galaxy that is observed.

Assuming an exact Hubble law, we can translate redshift into distance.

If it is also assumed that there was a big bang, redshift is used to
estimate the age of the galaxy.  

Once we have the distance, we can translate the apparent magnitude into
an absolute magnitude.

Combining this with the age of the galaxy we get an estimate of star
formation rate.

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
observations of supernovae, that the relation is not exact.

.. image:: images/supernovae.png

This is a central theme of :ref:`gotu`.  de Sitter Space, a uniformly,
negatively curved space-time, is suggested as a good model for what we see.

In de Sitter Space, the Hubble law only holds asymptotically.

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
Half immediately recede, the other half zoom closer.  All eventually
converge to the Hubble-law asymptote.

.. image:: images/blueshift.png

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

It then becomes very apparent why there is Hubble tension, the image
can look very different based on which range of redshifts and
distances you look at.

Here is the image for abs(zdash) < 1.

.. image:: images/zdash.png

One bit remaining to be modelled is the visibility, or apparent
magnitude of each source.  In particular, there needs to be a factor
of 1/(z*z) applied to the magnitude to account for reduction in power
resulting from redshift.  The energy of each photon is proportional to
its frequency, as are the number arriving per unit time, resulting in
a reduction of 1/(z*z) in the magnitude of a source.

The pieces are coming together to model the green valley.

2025/2/1
========

The Fortune object here is now at the point of creating interesting pictures.

It is also at the point of showing that things are of course a little
more complicated.

There is other factors that needs a model: gravitational redshift and
cosmological blueshift too.

As always all this is covered in :ref:`The Geometry of the Universe`.

There is a quasar-galaxy spectrum, defined by the size of the object's
central black hole.

These black holes, grow slowly acreting matter over time, so larger
black holes may well be much older.  The :ref:`gotu.spiral.Spiral`
module has all the key pieces, it is just necessary to put the puzzle
together.

Quasars typically exhibit gravitational redshift.  

The Eddington sphere, is the place where the outward radiation
pressure matches the inward gravitational pull.
:ref:`gotu.Spiral.eddington`.  The radius of this sphere can be
calculated, given the redshift.

If we know the mass of the black hole and the temperature and density
of the medium then we can calculate z, and hence the Eddington radius.

The density must lie somewhere between the density of the black hole
and the density of the universe.  The latter is between 100/cm3 and
1e12/cm3.  Reasonable to assume it is lower than the density of the
black hole.

What is needed here is a full model for quasars evolving into galaxies.

Some general observations:

* Small quasars have gravitational redshift, the Eddington sphere is
  close to the Schwartzchild radius.

* Stars typically form further out from the Eddington sphere and hence
  are subject to reduced redshift.

* de Sitter Space exhibits blue shift as well as redshift.  We may be
  seeing the dust of some galaxies and mistaking it for stars.

If we assume that all redshift is cosmological, then the result is
that the stars around small quasars will appear blue-shifted.

.. image:: images/blueshift

6/3/2025
========

Simulations of de Sitter Space show that redshift is only a weak
indicator of distance, or rather asymptotically an indicator of
distance.

This applies to blueshift too, where, the higher the blueshift, the
closer the source is to the Hubble radius. As with redshift, this
is only an asymptotic relationship.

The glowing dust of a high blueshift source may be mistaken for a
redshifted view of the stars in a galaxy.

Perhaps the green valley is in part due to whether we are seeing the
dust or the stars of a galaxy.

This is one area the JWST can contribute significantly.  Observations
of nearby galaxies at different wavelengths should help us refine our
classifications of galaxies.

24/3/2025
=========

There is a new release of data from the Dark Energy Spectrographic Instrument (DESI).

Observations are classified in various categories.

ELG, LRG, BGS, QSO

Emission Line Galaxy

Luminous Red Galaxy

Bright Galaxy Survey

Quasar Stellar Objects

DESI data release 2

It is going to be very interesting to explore the DESI data sets with
the perspective of the Geometry of the Universe.

The central idea is that as the size of the central black hole grows,
so does the ratio of the radius of the Eddington sphere to the
Schwartzchild radius.

So small quasars exhibit significant redshift.  Some of the luminous
red galaxies are likely nearby quasars.

When the light comes from the acretion disk it is harder to extract a
detailed spectrum, in short spectral lines are blurred.

See :ref:`gotu.desi` for tools to download DESI data.


"""
# never import *, except ...
from math import *

import random
import time

from astropy import table, units as u, constants as c

from blume import magic, farm, train
np = magic.np

from . import spiral

def mdtoM(m, d):
    """ Relationship between magnitude and distance.

    m - M = -5 + 5 * log(d)

    m apparent magnitude
    d distance in parsecs
    """
    M = m + 5 - (5 * log10(d))
    return M

def apparent_magnitude(absmag, distance):
    """ Give apparent magnitude give absolute magnitude and distance

    NB need distance in mega-parsecs.
    """
    return absmag - 5 + (5 * log10(distance))

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

def magnitude(self):
    """ Return estimate of magnitude based on mass """
    suns = (self.lightyear_to_kg() << u.M_sun).value

    mag = (5 * log10(1 / suns) / 2.)
    return mag

def gravitational_redshift(self):

    # density based on Schwartzchild radius
    dens = (self.density() / c.m_p) << 1/(u.m**3)

    # density in protons per m*3
    n = self.n

    print(dens, n)

    return dens


class Fortune(spiral.SkyMap):

    def __init__(self):

        super().__init__()

        self.sky = spiral.SkyMap()
        self.green = magic.TableCounts(
            xname='magnitude', yname='NUV-r',
            minx=-24, maxx=-18, maxy=10.)
        self.tablecounts.maxx = 0.22
        self.tablecounts.minx = -0.75
        self.tablecounts.maxy = 1.
        self.tborigin = False


    def nuvr(self, mag):
        """ return nuv-r value for given magnitude

        Assume a straight line relationship.
        """
        minmag = -24.
        magrange = 6.
        wavelength = 6.3 - ((mag-minmag) * 5.3/magrange)
        return wavelength
        
    async def run(self):

        self.create_sample()

        # reset Mstellar values, using our own favourite distribution
        self.set_mstellar(self.balls)

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
                x = x/(1+x)

                gz = gravitational_redshift(ball)
                await self.green_valley(ball, z, x, gz)

                #weight = 1/(x*x)
                weight = 1
                self.tablecounts.update([z], [x], weight)
                t += self.delta_t

            #print(f'{t:8.2f} {ball.theta:6.3f} {ball.phi:6.2f} {z:6.2f} {x:6.2f}')
            t2 = time.time()
            tt += t2-t1
            if tt > self.sleep:
                await self.tablecounts.show(xname=xname, yname=yname)
                await self.green.show()
                tt = 0.

        # one last show
        await self.tablecounts.show(xname=xname, yname=yname)
        await self.green.show()

    def set_mstellar(self, balls=None):

        balls = balls or self.balls

        for ball in balls:
            ball.Mstellar = self.random_mstellar()

    def random_mstellar(self):
        """Want distribution of galaxies by stellar mass

        There should be good values from local data.

        The gotu.spiral module uses a lognormal distribution.

        This models things well for high stellar masses, but it feels
        like it very much underestimates the numbers of smaller
        objects, below 10^9 stellar masses.

        The problem here is that biggest surveys are affected by the
        very same problem, the assumption of an exact Hubble law.

        There should however be a large enough sample of local galaxies to
        get a better estimate of the distribution.

        """
        return magic.random.expovariate(1/1e6)
        

    async def green_valley(self, ball, z, x, gz=0.):
        """ Create colour magnitude diagram

        Each ball is a galaxy, redshift z and distance x.

        Use self.nuvr() to calculate colour given magnitude
        and use self.green to make some counts.
        """
        mag = magnitude(ball)
        col = self.nuvr(mag)

        # add some random noise to col
        rcol = magic.random.gauss(col, col/10.)

        # distance in mega-parsec
        scale = (self.cosmo.hubble_distance << u.parsec).value

        dist = x * scale

        # calculate the apparent magnitude
        amag = apparent_magnitude(mag, dist)

        # skip stuff too small to see
        if amag > 25.:
            print(amag, dist, mag)
            return

        zsum = z + gz
        # use this amag to calculate the magnitude assuming distance is zsum
        # FIXME, should divide by 1/(z*z), but magnitude is log, so maybe -2z?


        try:
            magz = mdtoM(amag, zsum * scale)
        except ValueError:
            print("negative distance ie z", zsum)
            return

        print(rcol, mag, magz, z-x)
        self.green.update([magz], [rcol])


def flux2mag(flux):

    return 22.5 - (2.5 * log10(flux))
        
class View(train.Train):

    def __init__(self):

        super().__init__()
        self.tablecounts = magic.TableCounts(
            minx=-0.1, maxx=2.5,
            miny=15, maxy=30,
            width=200, height=200,
            xname='redshift',
            yname='flux magnitude'
        )


    def get_parser(self):

        parser = super().get_parser()

        parser.add_argument('--glob', default='**/*')

        return parser

    async def start(self):

        self.runs = 0
        
        if not self.paths:
            if self.path.is_file():
                self.paths = [self.path]
            else:
                path = Path(self.path)
                self.paths = list(path.glob(self.glob))
        else:
            self.paths = [magic.Path(path) for path in self.paths]
        self.paths = magic.deque(sorted(self.paths))

    def next_table(self):

        self.table = table.Table.read(self.paths[0])
        self.paths.rotate()

        return self.table

    def filter_table(self, table=None):

        table = table or self.table

        mask = table.field('ZWARN') == 0
        mask = mask & (table.field('SPECTYPE') == 'GALAXY')
        mask = mask & (table.field('FLUX_Z') > 0)
        mask = mask & (table.field('elg') != 0)

        return table[mask]

    async def run(self):

        tot = 0.0
        while True:
            self.runs += 1
            t1 = time.time()
        
            table = self.next_table()

            table = self.filter_table(table)

            # filter table and update tablecounts
            
            mag = [flux2mag(x) for x in table.field('FLUX_Z')]
        
            self.tablecounts.update(
                table.field('Z'),
                mag)

            tot += time.time() - t1
            if tot > self.sleep:
                await self.tablecounts.show()
                tot = 0.0
        
        
if __name__ == '__main__':

    
    land = farm.Farm()
    land.add(Fortune())
    land.add(View())
    farm.run(land)
