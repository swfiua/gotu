"""Milli-second pulsar edition

https://www.astro.umd.edu/~eferrara/pulsars/GalacticMSPs.txt


2026 TODO
=========

Build a model for the wobbles in the Milky Way based on the Sciama Principle.

There is a common component to every observation and that is the
movement of the Sun relative to the centre of the galaxy.

The mass and distance of the galactic centre are the two key
parameters, under the prior assumption that the centre may be as much
as 50 thousand light years distant, with a mass of 100s or thousands
of billions of suns.

Where pulsars are members of globular pulsars we can add the mass of
the cluster's centre to our variables, and model it's movement
releative to the galactic centre.

The key test would be whether a Bayesian approach yields a
signficantly higher posterior probability of the observations than
other models.

The model will also be able to make predictions of the amplitude we
can expect to find as we move into longer and longer time periods.

"""

from blume import magic

from astropy import table

import csv

def get_rows(infile=None):

    infile = infile or open('GalacticMSPs.txt')
    tab = csv.reader(infile,
                     skipinitialspace=True,
                     delimiter=' ')

    for row in tab:
        if not row: continue
        if row[0].startswith('#'): continue
        if row[2] == 'unk': continue
        name = row[0]
        period, dm, l, b = [float(x) for x in row[1:5]]

        yield dict(name=name, period=period, dm=dm, l=l, b=b)


class PTA(magic.Ball):

    def __init__(self):

        super().__init__()
        self.table = table.Table(list(get_rows()))

    async def run(self):

        ax = await self.get()

        ax.projection('polar')

        dm = self.table['dm']
        b = self.table['b']
        ax.scatter(self.table['l'], dm, s=dm, c=b)

        await ax.show()
        
if __name__ == '__main__':

    from blume import farm
    land = farm.Farm()
    land.add(PTA())
    farm.run(land)
    
