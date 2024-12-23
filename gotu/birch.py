"""================
The Green Valley
================

There's a hill with a green chair, lined by birch, a green valley, if
you will.

It's a place I have spent much time musing about space and time.

This module is about a new mountain, where the jackets are green.

It asks if there is in fact no valley at all, but an illusion of such
due to the assumption that redshift and distance follow an exact
Hubble law.

::

The *green valley* is a wide region separating the blue and red peaks
in the ultraviolet optical color magnitude diagram, first revealed
using GALEX UV photometry.

This is how the green valley galaxies are described by the 2014 paper
of Samir Salim: https://arxiv.org/pdf/1501.01963

Here is an image and caption from that paper:

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
see many  red galaxies and many blue galaxies, but far fewer in the
green region, a green valley if you will.

The conclusion is that there are two classes of galaxies.  Ones that
are actively forming stars and ones that are less active in forming
stars.

Explaining the Green Valley
---------------------------

What if the relationship between redshift and distance is not in fact
exact?

In de Sitter Space the relationship only holds asymptotically.

There are galaxies both sides of the asymptote.  Here is an image that
attempts to show the relationship:

Let us also assume that star forming rate has a linear relation with
galaxy size.

.. image:: images/zvr.png

At any particular redshift we see galaxies over a wide range of
distances.  At z=0, the most likely distance is actually at z=2, in a
Universe with an exact Hubble law.

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

The end result?  A slope of a large green mountain.

Now how to show this in code?

"""

from . import spiral

def mtod(m, M):
    """ Relationship between magnitude and distance.

    m - M = -5 + 5 * log(d)

    m apparent magnitude
    d distance
    """
    pass


