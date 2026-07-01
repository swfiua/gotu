"""
The James Webb Space Telescope has revealed large numbers of so-called Little Red Dots (LRD).

Spectra.

Central black holes.

Intriguing possibility: these are what are causing gravitational waves.

References
==========

[1] classic lrd spectra: v-shape emission lines

[2] estimate of mass of central black holes, surrounded by dust

[3] quasar-like features

"""

from blume import magic, farm

from astropy import table, io, units as u, constants as c

from .gw150914 import View, read_csv, transdict

class MassView(View):
    """ The black hole merger theory gives us masses merging at a particular redshift

    The arriving object theory gives us the masses arriving at a particular blueshift.

    Because of mass/redshift degeneracy we can calculate the masses of an arrival.

    frequency = mass * (1 + redshift)
    mass_arrival = mass * 

    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    async def run(self):

        fields = ['mass_1_source', 'mass_2_source', 'redshift', 'luminosity_distance']

        cosmo = self.skymap.cosmo.cosmo

        blueshift = self.blueshift
        hubble_distance = cosmo.hubble_distance

        m1s = []
        m2s = []
        rvs = []
        for row in self.table.iterrows(*fields):

            m1, m2, redshift, distance = row

            if not m1: continue

            print(row)

            freq = m1 * (1+redshift)

            m1_arrival = freq / (1 + blueshift)
            
            m1s.append(m1_arrival)
            m2s.append(m2*m1_arrival/m2)

            relative_distance = hubble_distance/distance

            relative_z = (1+blueshift)/(1+redshift)

            relative_visibility = ((m1_arrival * (((1+redshift)*distance)**2)) / m1) / (((1+blueshift)*hubble_distance)**2.)

            rvs.append(relative_z)

            # amplitude of wave at merger is
            amp = self.strain * (distance * u.mpc << u.m)

            # amplitude to get same wave for new arrival
            amp_arrival = amp / relative_visibility.value
            print('amplitudes', amp, amp_arrival)
            
        ax = await self.get()
        ax.hist(m1s, bins=20)
        ax.show()
        
        ax = await self.get()
        ax.hist(m2s, bins=20)
        ax.show()

        ax = await self.get()
        ax.set_title('relative z')
        ax.hist(rvs, bins=30)
        ax.show()

        ax = await self.get()
        ax.scatter(m1s, m2s)
        ax.show()

if __name__ == '__main__':

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--events', default='events.csv')
    parser.add_argument('--blueshift', type=float, default=-1+(1/8000.))
    parser.add_argument('--strain', type=float, default=1e-21)
    parser.add_argument('--name', default=None)

    args = parser.parse_args()
    
    data = list(read_csv(open(args.events)))

    data = transdict(data)
    
    data = table.Table(data)

    view = MassView(table=data, blueshift=args.blueshift, strain=args.strain)

    if args.name:
        view.select(args.name)

    land = farm.Farm()
    land.add(view)
    farm.run(land)
