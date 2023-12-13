""" Analysis of the evidence for dark energy

http://cdsarc.u-strasbg.fr/viz-bin/ReadMe/J/MNRAS/475/193

https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/475/193/table6.dat


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
        self.tasks.add(self.plot, zfield='zCMB')
        self.tasks.add(self.plot2)


    async def plot1(self):

        ax = await self.get()

        bmag = self.tab['Bmag']
        e_bmag = self.tab['e_Bmag']
        lz = np.array([log(x) for x in self.tab['zCMB']])

        ax.errorbar(lz, bmag, yerr=e_bmag, fmt='o')

        line = statistics.linear_regression(lz, bmag)

        xx = np.linspace(min(lz), max(lz), 100)
        yy = line.intercept + line.slope * xx

        ax.plot(xx, yy)
        ax.show()
        
        res = bmag - (line.intercept + line.slope * lz)

        hist = await self.get()
        hist.hist(res, 12)

        hist.show()
        
    async def plot(self, zfield='zCMB'):

        ax = await self.get()

        bmag = self.tab['Bmag']
        e_bmag = self.tab['e_Bmag']
        lz = np.array([log(x) for x in self.tab[zfield]])

        ax.errorbar(lz, bmag, yerr=e_bmag, fmt='o')

        line = statistics.linear_regression(lz, bmag)

        xx = np.linspace(min(lz), max(lz), 100)
        yy = line.intercept + line.slope * xx

        ax.plot(xx, yy)
        ax.show()
        
        res = bmag - (line.intercept + line.slope * lz)

        hist = await self.get()
        hist.hist(res, 12)

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
