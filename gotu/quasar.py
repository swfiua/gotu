"""=======================================================================
 What would light emerging at the event horizon of a quasar look like?
=======================================================================

For now that is the goal for this module, what should a quasar look like?

With all fingers crossed for the `JWST`_, I think we are about to be
surprised at how ubiquitous quasars are.

Geometry
========

Oscillations, tidal ejection.  

In a place where the passage of time is close to zero, but not actually, zero.


JWST
====

The model for quasars outlined in `gotu`_ requires just two parameters.

The central mass and the temperature and density of matter around the
Eddington sphere of the quasar's black hole.

There is a huge range of possible redshifts, depending on these two
parameters.  

"""
from astropy import constants, coordinates, time, table

M = 4e6
n = 1
T = 1

bondi = 2 * constants.G * M * constants.m_p / (3 * constants.k_B * T)
