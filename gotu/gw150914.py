"""Thanks to the Gravitational Wave Open Science Center for event catalogs and data.

https://gwosc.org/eventapi/html/GWTC/

The first gravitational wave detection.

I heard about this event during a Python conference in Februeary 2016
at the time of the announcement.

Brandon Rhodes gave a keynote where he mentioned the recent
announcement by the LIGO team and how python was used at key parts of
the the entire process.

The detection of these ripples in space time was a stunning
achievement, after decates of hunting.

Two black holes, 35.6 and 30.6 solar masses merge to form a final mass
of just 63.1 solar masses.

Energy emitted as gravitational waves: 3.1 solar masses.

There was a lot of interest at the conference and a number of
attendees with good knowledge of the discovery.

It was not until :ref:`GW170817` that I started to wonder whether the
signals being detected might have another explanation other than the
merging black holes.

By that time I had read Rourke's book.

How to reconcile the Sciama Principle with the Kerr metric?

And how does the Perfect Copernican Principle change priors?

What if everything is much, much older than 13 billion years?

Rourke uses the Sciama Principle as an addition to General Relativity,
to explain galactic rotation curves, without need for dark matter.

The problem for gravitational wave physics that with the Sciama
Principle binary systems are highly stable and there is a limit to how
far they can inspiral.

Fortunately, Rourke also proposes the hypothesis that gamma-ray bursts
may be the arrivals of new galaxies in our visible universe.

Along with Robert MacKay he shows how in a de Sitter universe, new
arrivals burst on the scene highly blue shifted.

It is due to the curvature of space time, each galaxy arrives highly
blue shifted, the blue shift reduces over time, until the galaxy then
starts to accelerate away and converge to a Hubble law.

Now any gravitational waves the galaxy is emitting will be modulated
in the same way.  Perhaps that is what we are detecting?

In a 2018 discussion on black holes there is this fascinating comment
from Colin Rourke::


   There is another possible more important problem that I have with
   black holes.  The fundamental inertial drag hypothesis that explains
   the dynamics of galaxies needs every mass in the universe to have a
   well-defined rotation (or a well-defined inertial frame in which it is
   static).  But the current fiction is that a BH is a POINT SINGULARITY
   and therefore it has nothing to define its rotation.  I mention this
   problem in passing in the book, but I did not stress it because I did
   not want to murder yet another sacred cow.

   
In the merging black hole models it is assumed that the angular
momentum that the two black holes have around each other is lost to
the surrounding universe, in a very brief amount of time.

In the arriving galaxy model, it is the wave from new angular
momentum, in the form of a rotating galaxy or quasar, arriving in our
visible universe.

So instead of masses in the stellar graveyard, we could be seeing
masses in our cosmic birth registry?

The black hole model also has to take account of space-time curvature:
close to black holes, time slows, exponentially.

Interestingly, the wave front will be shaped by the Kerr metric.  It
is the Kerr metric based frame dragging that creates a wave in space
time.

The key to resolving the Kerr/Sciama paradox is to understand that
both effects apply.

If you know the angular momentum of a body, you can calculate how it
will drag the surrounding space time round with it using the Kerr
metric.

This also gives the angular momentum that will be lost by the body,
and leads to the conclusion that bodies will eventually inspiral.

Now this will create a wave in the surrounding space time, with it's
amplitude dropping off inversely with distance, as assumed in
gravitaitonal wave physics.

In short, the detection of gravitational waves is direct confirmation
of the Sciama Principle, which in terms of the fabric of space-time
can be phrased::

  an oscillation w in space time induces an oscillation of amplitude
  w/r in the space time at distance r.



chirp redshift degenerecy
=========================

Chirp mass 28.6 Suns and at a distance of 430 Mpc.

The wave we observed depends on both the redshift and the source mass.

Suppose we have a chirp mass m, at distance z, then the wave we
observe will be the same as a mass m_0 = m * (1 + z).

inspiral
========

I have now spent a while trying to match the sort of curves we see.

The idea is that the whole curve will be determined by two parameters, theta and phi.

theta is the angle of approach.

theta is distributed as cos(theta), but there is a relationship
between theta and the brightness of the wave, so that needs to be taken into account.

phi is distribute as sinh(phi) squared, but again there are some complications.

My belief is that in observations, theta is biassed to small theta and
phi is arccosh(m1/m2).

Now the wave we see is not the entire history of the new arrival,
since there are two horizons a body needs to cross, in order for it to be visible to us.

Due to the low level waves throughout the universe, there is a limit
to how far waves can travel before they are thoroughly diverted from
their original direction.

This distance is likely a few hubble distances.

Now the hypothesis is that we are seeing new objects arriving in our
visible universe.  How old might those objects be?

My guess is that for an isolated quasar the actual acretion rate is
very low indeed.  [TODO problem is T and n to pass to acretion formulae]

For now, my approach is to go with the 3-6 hubble distance range
(which is in line with the cosmic microwave background).

This and the acretion rate can be tuned to create any magnitude wave
that we might detect.

From Rourke::

    For a short time after the first appearance we have the asymptotic relation:

       1 + z ~ t - t*

We are in the small t regime for both the ringdown and the inspiral.

ringdown
========

I was wrong about the cosmic birth registry!  It is not a births, it is weddings!.

It is our cosmic wedding registry.

The ringdown phase will presumably also depend on the two parameters,
theta and phi.

It feels like it might depend on the local conditions, would a space
based detector behave differently further from the earth's influence?

I think the answer is no.   The 

phi is the hyperbolic rotation for the arrival, distributed as
sinh(phi) squared.

The same parameters will characterise any accompanying gamma-ray burst
and other observations in the electromagnetic spectrum.

In the gamma-ray burst situation the decay in intensity would
presumably be identical and definitely be determined by theta and phi?

Now since we are seeing 


The first multi-messenger event?
--------------------------------

There was a weak burst of gamma-ray energy.

"""

from astropy import table, io, units as u, constants as c

from pycbc import waveform

import csv

import random
import math

from blume import magic, farm

from . import spiral

np = magic.np

m1 = 35.6 * u.M_sun
m2 = 30.6 * u.M_sun

mfinal = 63.1 * u.M_sun

mwave = 3.1 * u.M_sun

chirp =  28.6 * u.M_sun

distance = 430 * u.Mpc


def read_csv(infile):

    line = infile.readline()
    
    fields = [x.strip() for x in line.split(',')]

    reader = csv.DictReader(infile, fieldnames=fields)

    # skip first line
    reader.__next__()

    data = [x for x in reader]
    
    spell = magic.Spell(keys=fields)

    spell.find_casts(data, sniff=218)
    print(spell.casts)
    print(len(data))
    yield from spell.spell(data)
    
def transdict(data):

    result = {}

    for row in data:
        for k, v in row.items():
            result.setdefault(k, []).append(v)

    return result


class View(magic.Ball):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.skymap = spiral.SkyMap()
        self.skymap.tborigin = False
        self.skymap.max_t0 = 1e-12
        self.minz = -0.999
        self.tmax = 10


    def select(self, name='150914'):
        """ Really need the carpet to handle tables """
        if not hasattr(self, 'xtable'):
            self.xtable = self.table
        self.table = self.xtable[[name in x for x in self.xtable['name']]]
    

    async def zerochirp(self):

        data = self.table
        
        m1 = data['mass_1_source']
        m2 = data['mass_2_source']

        chirp = ((m1 * m2)**0.6)/((m1 + m2)**0.2)
        
        redshift = data['redshift']

        zzerochirp = chirp / (1 + redshift)

        ax = await self.get()
        bins = 25
        ax.hist(zzerochirp, bins)
        ax.set_title('z-zero chirp')
        #ax.plot(sorted(zzerochirp))

        ax.show()
        ax = await self.get()
        ax.hist(chirp, bins)
        ax.show()
        ax = await self.get()
        ax.plot(redshift)
        ax.show()


    def to_spiral(self, m1, m2, redshift, blueshift, distance):
        """Create a Spiral object with mass based on this observation

        Also want to estimate phi and theta.

        Although the wavefront all arrives at the same time, the waves
        that departed the source earlier have travelled further and so
        will be weaker.

        Rourke also notes that there is a limit to how far light (and
        hence gravitational waves) can travel before being thoroughly
        diverted from its original direction.

        Using the magnitude of the CMB he suggests that this is
        probably of the order of 3-6 Hubble distances.

        There is also the acretion of matter over time to consider.

        """
        self.galaxy = galaxy = spiral.Spiral()


        # 1 <= m1/m2 < infinity
        # looks like this is in fact cosh(phi)
        galaxy.phi = math.acosh(m1/m2)

        # galaxy.theta -- need to figure this one out too - 
        # NB theta could be related to spin alignment of black holes, or spin
        # of final black hole, where 0<=spin<=1, so theta = acos(spin)?
        # for now go withtheta distributed sin(theta) 
        # Note that the strength of the signal also depends on theta, I think
        # the stronger signals likely have small theta.

        
        galaxy.theta = math.acos((2*random.random()-1))

        # assume theta is small
        galaxy.theta = random.gauss(0, math.pi/32)

        # chirp and z
        chirp = ((m1 * m2)**0.6)/((m1 + m2)**0.2)

        bluechirp = (chirp/(1+redshift))/(1+blueshift)

        # How big does a mass at the Hubble distance have to be to
        # create a strain like the one detected?
        # strain is proportional to mass**(3/5) and inversely proportional
        # to distance.
        mass35 = ((chirp**(3/5) / (distance * u.Mpc)) * galaxy.cosmo.hubble_distance).decompose()

        mass = mass35**(5/3)

        # This what you would need if a black hole merger happened at that blueshift.
        # But that is not what is happening.
        # We are in a universe where galaxys grow slowly over time as they acrete matter
        # There is plenty of time and everything is older than you might think.

        # There is, however, a limit to how far light can travel
        # before being thoroughly diverted from it's original direction.

        # The ripples in space time reduce how far you can go from
        # your origin, before being turned back on yourself.
        
        print(f'chirp {chirp} bluechirp {bluechirp} phi {galaxy.phi}phi mass {mass}')

        # assume masses are normally distributed about the frequency of the detector
        mass = (3 * u.km)* random.gauss(10e6, 1e6)

        galaxy.Mcent = (mass << u.lightyear).value


    async def birth(self, samples=None):
        """What does the wave for the current galaxy look like?
        
        What would the gravitational wave from a black hole arriving
        in a de Sitter space universe look like?

        The wavefront, the distortion of space time due to the body's
        angular momentum, will follow the 1/r**3 relationship from the
        Kerr metric.
        
        However, the curvature of space time means we see this through
        curved glasses.

        There's a hyperbolic rotation parameterised by theta and phi.

        We do not actually see all the waves the body has ever emitted.

        The universe is full of low level gravitational waves and so waves can only go so far before being 

        """

        galaxy = self.galaxy
        hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value

        tmax = self.tmax / hubble_time

        if samples is None: samples = 1000

        # time of birth
        epsilon = 1/hubble_time
        tstar = galaxy.tstar()
        ttt = np.linspace(tstar+epsilon, tstar +epsilon+ tmax, samples)
        uuu = [galaxy.uoft(t) for t in ttt]
        zandx = [galaxy.zandx(t, u) for t, u in zip(ttt, uuu)]

        # zzz and xxx are the redshift (in our case, blueshift) and distance of the newborn
        zzz = [zx[0] for zx in zandx]
        xxx = [zx[1] * hubble_time for zx in zandx]

        zfilter = [z > self.minz for z in zzz]
        print(magic.Counter(zfilter))
        self.subtable = table.Table(dict(uuu=uuu, ttt=ttt, zzz=zzz, xxx=xxx, zfilter=zfilter))
        #uuu = np.array(uuu)[zfilter]
        #ttt = np.array(ttt)[zfilter]
        #zzz = np.array(zzz)[zfilter]
        #xxx = np.array(xxx)[zfilter]


        # set mass and wavelength
        wavelength = mass = (galaxy.schwartzchild() << u.lightsecond).value

        # inspiral -- this isn't quite right yet, but close
        inspiral = []
        u0 = uuu[0]
        for ix, uu in enumerate(uuu):
            umu0 = (uu - u0) * hubble_time
            try:
                value = mass * math.sin(umu0 / wavelength) / (umu0**3)
                value = math.log(mass / (umu0**3))
            except ValueError:
                value = mass

            inspiral.append(value)
        
        ax = await self.get()

        sniff = 3
        ax.set_title(f"Inspiral tstar={tstar}")
        clip = max(inspiral[:sniff])
        #ax.plot(ttt, np.clip(inspiral, -clip, clip))
        ax.plot(ttt, inspiral)

        ax.show()
        ax = await self.get()

        ringdown = []
        for ix, uu in enumerate(uuu):
            umu0 = (uu - u0) * hubble_time
            distance = xxx[ix]
            zz = zzz[ix]
            try:
                value = mass * math.sin(umu0 / wavelength) / (distance * ((1+zz)**2))
                value = math.log(mass / (distance * ((1+zz)**2)))
                #value = mass * math.sin(umu0 / wavelength) / distance
            except ValueError:
                value = mass
                
            ringdown.append(value)

        ax.set_title("Ringdown")
        clip = max(ringdown)
        #ax.plot(ttt, np.clip(ringdown, -clip, clip))
        ax.plot(ttt, ringdown)

        ax.show()

        ax = await self.get()
        ax.set_title("full")

        times = np.concat(((-1. * (ttt - tstar))[::-1], ttt-tstar))
        print('JJJJJJJJJ', len(times), len(inspiral[::-1] + ringdown))
        ax.plot(times, np.clip(inspiral[::-1] + ringdown, -clip, clip))

        ax.show()
        

    async def run(self):

        fields = ['mass_1_source', 'mass_2_source', 'redshift', 'luminosity_distance']
        blueshift = -0.999

        epsilon = 1e-6
        for row in self.table.iterrows(*fields):

            m1, m2, redshift, distance = row

            delta_t = 0.001
            
            try:
                wf = waveform.get_td_waveform(
                    mass1=m1,
                    mass2=m2,
                    approximant='TaylorF2', delta_t=delta_t, f_lower=20)
            except:
                print(m1, m2, 'bad')
                continue

            ts = wf[0]
            nn = len(ts)


            ax = await self.get()
            ax.plot(magic.np.arange(len(ts)) * delta_t, ts)
        
            ax.set_title(f"Solar Masses: {m1:.1f} {m2:.1f}")
            ax.show()

            self.to_spiral(m1, m2, redshift, blueshift, distance)

            await self.skymap.explore(
                thetas=[self.galaxy.theta],
                #thetas=[self.galaxy.theta] + [epsilon + (x * math.pi/12) for x in range(4)],
                phis=[self.galaxy.phi])

            await self.birth()
            
            await magic.sleep(self.sleep)

            

            
if __name__ == '__main__':

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--events', default='events.csv')
    parser.add_argument('--name', default=None)

    args = parser.parse_args()
    
    data = list(read_csv(open(args.events)))

    data = transdict(data)
    
    data = table.Table(data)

    view = View(table=data)

    if args.name:
        view.select(args.name)

    land = farm.Farm()
    land.add(view)
    farm.run(land)
        
