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

What we are seeing is the sum of the rotations of all matter in our
visible universe.  Giant black holes at the heart of galaxies account
for much of the matter.

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
presumably dropping off with distance by a factor of 1/r. [1]

For a radius in years, we need 10^11 solar masses.

Note also that the effect is dominated by distant galaxies, as is the
CMB, since the number of galaxies at a given distance goes up with
r^2.

[1] see Compton radius.

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

Rambling thoughts
-----------------

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

By a happy coincidence(?), the chirp mass happens to closely match the
amount of energy the galaxy gives off over half of the time it is
visible to us.

Update
======



"""
import math
import argparse

import numpy as np
from astropy import units, constants, coordinates
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-n', default=1e11, type=float,
                    help='number of galaxies in the universe')
parser.add_argument('-m', default=5e12, type=float,
                    help='mass of typical galaxy')
parser.add_argument('-r', default=1.37e10,
                    help='radius of the visible universe')


args = parser.parse_args()

# Number of galaxies in the universe
N = args.n

# mass we are interested in, in solar masses
M = args.m

# Suns mass as a distance in meters
msun = 3000 * units.meter

# radius of the visible universe
R = args.r * units.lightyear

# how big is the wave from all these masses
amplitude = N * M * msun / R.to(units.meter)

print(f'{N:e} galaxies of mass {M:e}')

print('Amplitude:', amplitude)

# was hoping for 10 meters, how bad is the guestimate?
print('factor out:', 10 / amplitude)

print('Schwartzchild radius in light years:',
      (msun * M).to(units.lightyear))

surface_area_of_universe = 4 * math.pi * R.to(units.meter)**2
print('surface area of universe:', surface_area_of_universe)

cmb_photon_density = 4e8 / (units.meter**3)

print('photons emitted:', cmb_photon_density * surface_area_of_universe)

# how about R * 1.33?
V = 1.33
print('surface_area_of_universe * V *V:', V)

print('photons emitted at V',
      cmb_photon_density * surface_area_of_universe * V * V)

# it does not matter where you are, the cmb_photon_density is the same

# the question is, why is it so hot?
# there is about 45 times the microwave energy
# than that which all the galaxies are emitting as energy

T = 2.73 * units.K

E = constants.k_B * T**4 

print(f'Radiant heat per unit area at {T}: {E}')

# planck's law  B_v(v, T) = (2hv^3/c^2) / (e(hv/kT) - 1)


def planck_radiance_law(v, T=T):
    """ Energy emitted in frequency v at temperature T """
    h = constants.h
    c = constants.c
    e = math.exp

    v = v / units.second
    hv = h * v
    kT = constants.k_B * T
    lam = c / v

    # in terms of frequency v
    bv = (2*h*v**3/(c*c)) / (e(hv/kT) - 1)

    return bv.value

def planck_radiance_law_wavelength(wavelength, T=T):
    """ Energy emitted in wavelength at temperature T """
    h = constants.h
    c = constants.c
    e = math.exp
    kT = constants.k_B * T
    lam = wavelength * units.meter
    #print(lam)
    #print(h*c/lam*kT)
    # in terms of frequency v
    blam = (2*h*c**2/(lam**5)) / (e(h*c/(lam*kT)) - 1)

    return blam.value


def plots():

    xx = np.logspace(7, 12., 100)

    yy = [planck_radiance_law(x / units.second).value for x in xx]

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(xx, yy)

    yy = [
        planck_radiance_law_wavelength(
            constants.c / (x / units.second)).value
        for x in xx]

    ax2.plot(xx, yy)
    plt.show()


def velocity_of_hydrogen_gas(T=2.73):

    value = 3 *constants.k_B * T * units.K / (2 * constants.m_p)
    print(value)
    v_rms = math.sqrt(value.value)

    return v_rms

# how much matter is hydrogen gas?
mass_of_galaxies = M * N * constants.M_sun

dust_ratio = 1

hydrogen_atoms = mass_of_galaxies / (constants.m_p * 2)

# ratio of surface area of a galaxy to surface area if split into
# hydrogen molecules
ratio = M * constants.M_sun / (2 * constants.m_p)
print(ratio) 

sc_radius_of_galaxy = 3 * units.kilometer * M
c = constants.c
sc_radius_of_proton = 2 * constants.G * constants.m_p / (c*c)

# surface area
print(sc_radius_of_galaxy ** 3 /
      ((sc_radius_of_proton ** 3) * ratio))

# hydrogen_atomes per m3
def mass_of_universe_given_hpm(hpm = 10):

    h2 = (hpm/units.meter)**3

    # calculate mass of universe at this density
    total_h2 = 4 * math.pi * h2 * (R.to(units.meter))**3 / 3
    mass = (2 * constants.m_p) * total_h2

    # in solar masses
    print(f'With {hpm} hydrogen molecules per meter')
    print(f"Mass of universe density {h2:e} {mass/constants.M_sun:e} solar masses")
    print(f"Or {mass/(M*constants.M_sun):e} galaxies of {M:e} suns")
    print(f"total_h2 {total_h2:e}")
    # what is the surface area of a proton compared to galaxy mass M?
    ratio = (M * 3 * units.kilometer) ** 2 / (
        total_h2 * (2*constants.m_p/constants.M_sun))
    ratio = (M * constants.M_sun / constants.m_p)
    
    
    print(ratio, ratio / total_h2)
    
    protons_per_galaxy = M * constants.M_sun / constants.m_p
    print(f'protons per galaxy: {protons_per_galaxy:e}')

    # galaxy surface area
    sa_of_galaxy = (protons_per_galaxy**(1/3))**2

    print(f'surface area of galaxy in proton area {sa_of_galaxy:e}')

    gas_area = protons_per_galaxy / sa_of_galaxy
    print(f'one galaxy of protons has area of {gas_area:e}')

# eg compare these
mass_of_universe_given_hpm(1)
mass_of_universe_given_hpm(10)
mass_of_universe_given_hpm(100)

