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

        # chirp and z
        chirp = ((m1 * m2)**0.6)/((m1 + m2)**0.2)

        bluechirp = (chirp/(1+redshift))/(1+blueshift)

        # How big does a mass at the Hubble distance have to be to
        # create a strain like the one detected?
        # strain is proportional to mass**(3/5) and inversely proportional
        # to distance.  
        mass35 = ((chirp**(3/5) / (distance * u.Mpc)) * galaxy.cosmo.hubble_distance).decompose()

        mass = mass35**(5/3)
        
        
        print(f'chirp {chirp} bluechirp {bluechirp} phi {galaxy.phi}phi mass {mass}')

        

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
                #thetas=[self.galaxy.theta],
                thetas=[epsilon + (x * math.pi/12) for x in range(4)],
                phis=[self.galaxy.phi])
            
            await magic.sleep(self.sleep)



            
if __name__ == '__main__':

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--events', default='events.csv')

    args = parser.parse_args()
    
    data = list(read_csv(open(args.events)))

    data = transdict(data)
    
    data = table.Table(data)


    land = farm.Farm()
    land.add(View(table=data))
    farm.run(land)
        
