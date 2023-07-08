"""Pulsar timing array detects ultra-low frequency gravitational waves


The news on 29 June 2023 very much lived up to the hype.

Observational astronomy is going through an incredible period.

An observatory tracking the timing of 68 pulsars over 15 years has
detected gravitational waves with wavelenths of years -- that's the
distance light travels in a year.

Since the waves travel at the speed of light, it's also the time it
takes for one wavelength, hence the frequency is in nanohertz.

They have detected a wobble in space time of the order of 10m per
light year.

It is an incredible collaboration.  It was even necessary to improve
our estimates of the movement of Jupiter, using observations from a
Jupiter space-probe, in order to know the position of the earth
relative to the solar system's centre of mass.

Very interestingly the wave detected is approximately twice the amplitude they were expecting to find, given their models.

These models assume we are seeing waves from the mergers of black
holes at the centre of galaxies.

This observation comes at a time when astrophysicists are struggling
to explain how galaxies got so large, so soon after the big bang.

Professor Colin Rourke suggests that the Big Bang never happened. He
proposes *de Sitter Space* as a natural model for the universe.

*de Sitter Space* is much misunderstood.

The big bang model has precisely half the matter in a full de Sitter
universe.

The expanding universe we see is balanced by a contracting flow.

When this matter is added back in, bingo the amplitude of the wave
will be twice what the teams modelling predicted!

The observations will also be able to build a map over time showing
how the amplitude of waves differs in different parts of the sky.

I predict that this map will match the Cosmic Microwave Background.

I expect teams are already looking at this.  If it is found it would
indicate that both the waves and the CMB have the same source.

This will be taken as confirmation of the big bang theory and a
fantasy period of merging galaxies, that we do not see.

What we are seeing is the sum of the rotations of all black holes in
our visible universe.

As Professor Rourke suggests, these black holes drag the surrounding
spacetime by::

         w m / r

Where m is the black hole mass, w (or omega) is the hole's angular
velocity and r is the distance from the hole.

This is known as the *Sciama Principle*, by Dennis Sciama, who proposed
a theory of gravity based on the principle.

The factor of 1/r is controversial, as the unique solution to
Einstein's general relativity, in as vacuum gives the Kerr metric,
which drops off by 1 / r^3.

The solution to this conundrum, is that space is not a vacuum and so
the Kerr metric does not apply.

Now returning to nano-gravity.  The models that are being used assume
the waves are from inspirals of super massive black holes, rather than
just the direct rotations of the black holes themselves (see above re
Kerr metric).

Nonetheless, the waves are commensurate with the Schwartzchild radius
of the black holes, with magnitude proportional to the mass and
presumably dropping off with distance by a factor of 1/r.

For a radius in years, we need 10^11 solar masses.

Note also that the effect is dominated by distant galaxies, as is the
CMB, since the number of galaxies at a given distance goes up with
r^2.

What about the high frequency waves LIGO is detecting?
------------------------------------------------------

These are the analogue of gamma-ray-bursts as describing in `gotu`.

Are there other implications?
-----------------------------

We know pulsar positions and timings in unprecedented detail.

This should allow further tests on variations of general relativity
that take account of a body's rotation.

We have more precise estimates for objects in the solar system,
including jupiter and earth.

Can we now detect the effects of these rotations on the system?


The waves we see are the sum of the waves from all the galaxies that
have entered our visible universe.

But what does that look like?

The converging binary model calculates a chirp mass, which is the
energy emitted by the inspiral.

The Sciama Principle model presumably generates similar energy over a
longer time scale?

Ramling thoughts
----------------

We are now able to track the motion of some objects with incredible
precision. There are lots of opportunities to test the Sciama
Principle. Pulsar models now have factors for rotation in binary
systems.

I'm pretty sure that the binary mergers we see are really small
quasars arriving in our galaxy.

Say 10^5 suns with a 2 second or so wavelength, the time for the black
hole surface to make one rotation at the speed of light.

This gets boosted (due to de Sitter geometry) to say z = 0..01 at
peak, giving a signal in the audible range around 440 Hz

Small quasars, radio sources, not powerful enough to create a
gamma-ray burst.

The larger ones have less gravitational redshift and we get a GRB.

The one definitive case I know about the GRB peak was some 2 seconds
behind the gravity wave peak.

It was assumed the merger included a neutron star, hence the GRB. I
am pretty sure the masses were also at the higher end.

I assume the models all stop at the event horizon, so the spectrum of
the wave should peak around that wavelength, hence there is a natural
mapping from two binaries of the same mass merging as there is to that
rotating mass arriving at the edge of our galaxy.

I think it is reasonable to assume that the gravity wave will peak at
1/2 the wavelength from the centre and hence the delay between the two
events.'

When a galaxy arrives, the wave we see will be much lower
frequency, due to the lower angular velocity: years rather than
seconds.  Now, given a nice collection of GRB, preferably a
comprehensive catalogue for the last few years, look for correlations
with the pulsar array timing and the predicted waves.

The GRB allows us to estimate theta, phi and mass of the arrival.

It should then be possible to go and look for the waves in the pulsar
data (possibly LIGO data too) for matching waves.  I expect the best
to hope for is to get a significant correlation with the wave we see
over a large number of observations.

I suspect someone is doing this work anyway. Multi-messenger astronomy
has been waiting for this and it is natural for someone to do the same
thing for their neutron star merger model.

More Ramblings
--------------

https://nanograv.org/news/15yrRelease

has links to the key papers behind the release.

The NANOGrav 15-year Data Set::

   Constraints on Supermassive Black Hole Binaries from the
   Gravitational Wave Background.


   https://arxiv.org/abs/2306.16220

This has a lot of fascinating information.  Figure A1 is particularly
interesting, showing how models in the literature compare to the
observed waves.

These models are all based on binary mergers of supermassive black
holes.

It is my belief that this is not how black holes behave.

Mergers involve a "chirp" mass: the amount of mass (and hence energy)
released as gravitational waves as a result of the merger.

Intriguingly, this is based on General Relativity calculations that
largely ignore the effects the two body's rotations have on each
other, the energy released is the size of the error in that modelling.

If you take that into account, they don't merge and there is no
gravitational wave, according to GR.

But this same inertial drag that stops them merging drags the
surrounding space time round in a circle.  These giant black holes
drag space time around with them all the time.

It's this that we are seeing, a weaker wave, it happens all the time.

The models all agree that the wavelengths we are seeing are dominated
by a period of supermassive black hole merging.

By a happy coincidence, the chirp mass happens to closely match the
amount of energy the galaxy gives off over half of the time it is
visible to us.


"""
import math
import numpy as np
from astropy import units, constants, coordinates
from matplotlib import pyplot as plt

# Number of galaxies in the universe
N = 1e11

# mass we are interested in, in solar masses
M = 1e11

# Suns mass as a distance in meters
msun = 3000 * units.meter

R = 1.37e10 * units.lightyear

amplitude = N * M * msun / R.to(units.meter)

print('Amplitude:', amplitude)

print('factor out;', 10 / amplitude)

1/0

hubble = 68 * units.kilometer / units.second / units.megaparsec

N = 1e11  # total number of galaxies in our visible universe

# proportion of mass emitting wavelengths of a few years
# things are complicated by z,
# I should really sum over a range of z's adjusting the mass at each z 
# to keep the effective wavelength constant.
# I also need better information on galaxy mass distributions.
k = 5e-6   

# mass of each galaxy, in years   1 = 3e12 solar masses
Msun = (3 * units.kilometer).to(units.lightyear)

# mean mass of galaxies emiting wavelength of interest
# my guess is that this wave is coming from smaller objects
M = 1 * units.lightyear

# hubble  distance in light years
R = 1.37e10 * units.lightyear
z = 1000

rmin = 1e9 * units.lightyear
rmax = 13.5e9 * units.lightyear

wavelength = 1.0 * units.lightyear

results = None

def main():


    print("mass in lightyears:", M)
    print("mass in suns:", M / Msun)
    

    print("redshift adjusted wave length:", z * M)

    amplitude = k * N * M / R
    amplitude *= units.lightyear

    print(amplitude.to(units.meter) / z**2)

    # loop over distance
    r = rmin + 0
    global results
    results = []
    c = constants.c
    print('rRRRRRR', r, rmin, rmax, rmin<rmax, r<rmax)
    print('r is rmin', r is rmin)
    rr = np.linspace(rmin, rmax, 20)

    for r in rr:
        print('xxxxxxx', r, rmin, rmax, rmin<rmax, r<rmax)
        v = (r * hubble).to(units.meter/units.second)
        zz = v / c


        # alternative zz calc based on v
        zz2 = -1 + 1 / (math.sqrt((1-(v**2/c**2))))
        print('zzzz', zz, zz2, zz/zz2)

        # use z = (wobs - wemit)/wemit to calculate
        # wemit necessary for given wobs.
        # rearrange to ge wemit = wobs/(1+z)
        # and note that wobs is M

        # we want a wavelength equal to M
        # but we're redshifted by z, so our wave will be
        # m = M / (1+ z)
        
        m = M / (1 + zz)

        print("distance:", r, zz)
        print("mass in lightyears:", m)
        print(f"mass in suns:  {m / Msun:e}")
        print("redshift adjusted wave length:", m)

        # need to modify N according to r
        n = N * (r / R) ** 2 
        
        amplitude = k * n * m / r * units.lightyear
        
        print(r/R, v, zz, m, amplitude.to(units.meter))

        results.append(
            dict(r=r, z=zz, m=m, roverhubble=r/R, v=v,
                 amp=amplitude.to(units.meter)))

        
        
        print('rrrrrr', len(results), r, rmin)

        r += 1e9 * units.lightyear

    print(results)
    fig, ax = plt.subplots()
    from astropy.table import Table
    tab = Table(results)
    print(tab)
    ax.plot(tab['r'],  tab['amp'])
    #ax.show()
    print()
    print('rrrrrr', len(results))

    plt.show()

if __name__ == '__main__':

    main()
