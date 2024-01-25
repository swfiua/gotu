"""Analysis of the evidence for dark energy

http://cdsarc.u-strasbg.fr/viz-bin/ReadMe/J/MNRAS/475/193

https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/475/193/table6.dat

The Supernovae class just digests a table of data.

It is looking for a magnitude (Bmag) and a redshift value (z), as well
as the error in the magnitude.

It does a scatter plot of the data and does a linear regression to
plot a least squares fit.

Residuals are calculated as the difference between the observed
magnitude and the magnitude expected assuming we lie on the best fit
line.

A histogram of the residuals is plotted.

These are asymetric and consistent with a de Sitter Universe where
each galaxy we observe has the Hubble line as an asymptote.

To put another way, some galaxies are relatively new arrivals that
have not yet accelerated away fast enough to give the redshift we
would expect, given how far away they are.

There seems good evidence in the data for the de Sitter Model.

TODO: work on details based on arrival rate of new galaxies.

Here's a try.  there are N=10**11 galaxies in the visible universe
which is 10**10 years wide.

there are pi * 10**2 days in a year, so pi * 10**13 days in the
universe.

We are getting about one gamma ray per day, so how small can a galaxy
be and give a detectable gamma ray?

Can we estimate where the cut-off is and get a better handle on
distribution of gravitational waves un-accompanied by GRB?

"""

import requests
import statistics
from math import *
from collections import defaultdict
    
from pathlib import Path
from astropy.io import fits, ascii
from astropy import table, cosmology, units as u, constants as c
from astropy.io import fits

import numpy as np

from blume import magic, farm

DATA_URL='https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/475/193/table6.dat'
COLUMNS = ['sn', 'zhelio', 'e_zhelio', 'zCMB', 'e_zCMB',
           'MJDPeak', 'e_MJDPeak', 'x1', 'e_x1', 'c', 'e_c', 'Bmag', 'e_Bmag']

def get_data():
    """ Just get the data for table 6.

    https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/475/193/ReadMe

    Saves file as table6.dat in current working directory.

    Checks for file and uses that rather than request a new copy.
    """

    filename = Path('table6.dat')
    if filename.exists():
        data = filename.open().read()
    else:
        resp = requests.get(DATA_URL)
        data = resp.content.decode()
        filename.open('w').write(data)
    
    rows = data.split('\n')

    data = defaultdict(list)
    for row in rows:
        name = row[:29].strip().replace(' ', '_')
        fields = [float(x.strip()) for x in row[29:].split()]

        if not fields: continue
        for col, value in zip(COLUMNS, [name] + fields):
            data[col].append(value)

    for k, value in data.items(): print(k, len(value))
    tab = table.Table(data)
    return tab


class Supernovae(magic.Ball):


    def __init__(self, tab=None):

        super().__init__()

        if tab is None:
            tab = get_data()

        self.tab = tab

        self.tasks.add(self.plot)
        self.tasks.add(self.plot, zfield='zhelio')
        #self.tasks.add(self.plot2)


    async def plot(self, zfield='zCMB'):

        ax = await self.get()

        bmag = self.tab['Bmag']
        e_bmag = self.tab['e_Bmag']
        lz = np.array([log(x) for x in self.tab[zfield]])

        ax.errorbar(lz, bmag, yerr=e_bmag, fmt='o')

        ax.set_ylabel('Bmag')
        ax.set_xlabel('log(%s)' % zfield)

        line = statistics.linear_regression(lz, bmag)

        xx = np.linspace(min(lz), max(lz), 100)
        yy = line.intercept + line.slope * xx

        ax.plot(xx, yy)
        ax.show()
        
        res = bmag - (line.intercept + line.slope * lz)

        hist = await self.get()
        hist.hist(res, 12)
        hist.set_title('Residuals: Observed Bmag-expected|%s' % zfield)
        hist.show()

    async def plot2(self):

        ax = await self.get()

        lhz = np.array([log(x) for x in self.tab['zhelio']])
        lcz = np.array([log(x) for x in self.tab['zCMB']])

        ax.scatter(lhz, lcz)
        ax.set_ylabel('zCMB')
        ax.set_xlabel('zhelio')

        ax.show()
        
if __name__ == '__main__':

    land = farm.Farm()

    land.add(Supernovae())

    farm.run(land)
