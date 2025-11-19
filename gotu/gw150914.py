"""
Thanks to the Gravitational Wave Open Science Center for event catalogs and data.

https://gwosc.org/eventapi/html/GWTC/
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
        #galaxy.theta = random.gauss(0, math.pi/32)

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

    async def birth(self, tmax=None, samples=None):
        """What does the wave for the current galaxy look like?
        
        What would the gravitational wave from a black hole arriving
        in a de Sitter space universe look like?

        The wavefront, the distortion of space time due to the body's
        angular momentum, will follow the 1/r**3 relationship from the
        Kerr metric.
        
        However, the curvature of space time means we see this through
        curved glasses.

        There's a hyperbolic rotation parameterised by theta and phi.

        """

        galaxy = self.galaxy
        if tmax is None:
            tmax = ((galaxy.cosmo.cosmo.hubble_time << u.s).value) * self.skymap.max_t0

        if samples is None: samples = 1000

        # time of birth
        tstar = galaxy.tstar()
        ttt = np.linspace(tstar, tstar + self.skymap.max_t0, samples+1)
        ttt = ttt[1:]
        uuu = [galaxy.uoft(t) for t in ttt]
        zandx = [galaxy.zandx(t, u) for t, u in zip(ttt, uuu)]

        # zzz and xxx are the redshift (in our case, blueshift) and distance of the newborn
        zzz = [zx[0] for zx in zandx]
        xxx = [zx[1] for zx in zandx]

        # set mass and wavelength
        wavelength = mass = galaxy.schwartzchild().value

        # inspiral -- this isn't quite right yet, but close
        inspiral = []
        u0 = uuu[0]
        for ix, uu in enumerate(uuu):
            umu0 = uu - u0
            value = mass * math.sin(umu0 / wavelength) / (umu0**3)
            inspiral.append(value)
        
        ax = await self.get()

        sniff = 3
        ringdown = []
        ax.set_title("Inspiral")
        clip = max(inspiral[:sniff])
        ax.plot(ttt, np.clip(inspiral, -clip, clip))

        ax.show()
        ax = await self.get()

        ringdown = []
        for ix, uu in enumerate(uuu):
            distance = xxx[ix]
            zz = zzz[ix]
            value = mass * math.sin(umu0 / wavelength) / (distance * (1+zz))
            ringdown.append(value)

        ax.set_title("Ringdown")
        clip = max(ringdown[:sniff])
        ax.plot(ttt, np.clip(ringdown, -clip, clip))

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
        
