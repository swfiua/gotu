"""
================
The Green Valley
================

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

Now it is also possible to measure the red-shift of each galaxy that
is observed.

Assuming an exact Hubble law, we can translate redshift into distance.

Once we have the distance, we can translate the aparent magnitude into
an absolute magnitude.

The curious observation is that across a wide range of magnitudes we
see many  red galaxies and many blue galaxies, but far fewer in the
green region, a green valley if you will.

The conclusion is that there are two classes of galaxies.  Ones that
are actively forming stars and one which is less active in forming
stars.

Explaining the Green Valley
---------------------------

What if the relationship between redshift and distance is not in fact
exact?

In de Sitter Space the relationship only holds asymptotically.

There are galaxies both sides of the asymptote.  Here is an image that
attempts to show the relationship:


.. image:: images/zvr.png


At any particular redshift we see galaxies over a wide range of
distances.  At z=0, the most likely distance is actually at 2/3 of the
distance to the edge of the universe.

We now see the problem.

If a galaxy turns out to be nearer than the Hubble law would imply, we
end up over-estimating it's size.

Likewise, if a galaxy is further away than the Hubble law implies, we
under-estimate it's size.

The more distant a galaxy is, the larger it has to be for us to
observe it.

Our sample of galaxies that are further away than we are assuming will
be a sample of large galaxies, that we mistakenly assume are small.
Note that there are many more such galaxies to observe, than there are
ones closer to home.

The sample of galaxies that are nearer that we are assuming, will
include small galaxies that we are assuming to be large.  There will
be far fewer of these galaxies, but because they are closer to us we
observe many.

Hence our sample is dominated by the many small, hot galaxies and the
large, cooler galaxies that are more distant.


Now how to show this in code?  

"""
