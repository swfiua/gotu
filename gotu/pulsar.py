"""
Milli-second pulsar edition

https://www.astro.umd.edu/~eferrara/pulsars/GalacticMSPs.txt
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
    
