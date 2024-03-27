"""
Display data from Gaia

All thanks to the European Space Agency for data and images such as this.

https://gea.esac.esa.int/archive/documentation/GDR2/large/cu9/cu9gat_skydensity_healpix_logcount_gal_large.png

This module uses the `astroquery.gaia` submodule to query the Gaia database.

I am still finding my way around the data (almost June 2020).

It is a record of over a billion observations.

Many variables, along with error estimates too.

The plan for now is to download a bunch of random samples, asynchronously.

Save each sample in `fits` format.

And then explore the data.

Data downloaded is cached in the current directory.

The same is checked for data from a previous run and that will be read in
before loading any further data.

Would be good to be able to be able to share bunches of data, that is part of
the more general problem of distributed data.

See `-bunch` and `-topn` command line options for how to control how many
bunches are downloaded and how big each bunch is.

The idea here is to look into the question, of just where is the sun?

Specifically, where is it relative to the galactic centre?

Recognising that the galactic centre is a bit of a puzzle itself.

"""
import argparse
from collections import deque

from astropy.table import Table, vstack
from astropy import coordinates
from astropy import units as u

from astroquery.gaia import Gaia

import healpy as hp

from blume.magic import Ball

import numpy as np
import math
import random
from pathlib import Path

from blume import magic

from blume import farm as fm

TABLE = 'gaiadr3.gaia_source'
TABLE_SIZE=1811709771

COLUMNS = ('source_id', 'random_index', 'b', 'l', 'ra', 'dec',
           'parallax',
           'pmra', 'pmdec', 'radial_velocity')

FILENAME = 'radial_velocity2.fits'

def get_squeal(bunch, nbunch):

    columns = (', ').join(COLUMNS)

    bunch_size = int(TABLE_SIZE / nbunch)
    start = bunch * bunch_size
    end = start + bunch_size

    squeal = (f'SELECT {columns} ' +
        f'FROM {TABLE} ' +
        f'WHERE radial_velocity is not null ' +
        f'AND random_index BETWEEN {start} AND {end}')


    #squeal = f'select top 100000 {columns} from {table} where radial_velocity IS NOT NULL'
    #squeal = f'select top 1000 {coumns} from {table} where mod(random_index, 1000000) = 0'
    print(squeal)
    return squeal

def get_sample(squeal):

    if len(squeal) > 1000:
        print(f'squeal: {squeal[:360]} .. {squeal[-180:]}')
    else:
        print(squeal)

    job = Gaia.launch_job(
        squeal,
        output_file=str(filename),
        dump_to_file=filename)

    print('*' * 49)
    print(job)
    
    return job.get_results()


def get_samples(n=1000):

    for bid in range(n):

        path = Path(f'bunch_{bid}.fits.gz')

        if path.exists():
            print('already exists:', path)
            continue
        
        squeal = get_squeal(bid, n)
        
        print('launching gaia async job for:', path)
        job = Gaia.launch_job_async(
            squeal,
            output_file=str(path),
            dump_to_file=True)


class Milky(Ball):

    def __init__(self, bunch=1, topn=1): 

        super().__init__()

        self.bunches = deque()
        self.nbunch = bunch
        self.bix = 0
        self.topn = topn
        self.runs = 0
        self.clip = 25  # either side
        self.fudge = 2.
        self.keys = deque(('parallax', 'radial_velocity'))


    async def start(self):
        """ start async task to read/download data """

        # load any bunches there are
        # for now, keep them separate
        self.nbins = 200
        self.vrcounts = np.zeros((self.nbins, self.nbins))
        self.buckets = np.zeros(self.nbins)
        self.counts = np.zeros(self.nbins)
        path = Path()
        for bunch in path.glob('bunch*.fits.gz'):
            if bunch.exists():
                self.bunches.append(bunch)

            if len(self.bunches) == self.nbunch:
                break

            await magic.sleep(0)

    def build_table(self):
        
        #print(hpxmap)
        # Sag A*

        table = vstack(list(self.bunches))

        self.table = table

    async def run(self):

        self.runs += 1
        print("number of runs", self.runs)
        for x in range(1):
            self.calculate()

        await self.plots()
        
    def calculate(self):
        
        self.table = Table.read(self.bunches[0])
        self.bunches.rotate()
        if not hasattr(self, 'table'):
            self.build_table()

        table = self.table
        ra = table['ra']
        dec = table['dec']
        pmra = table['pmra']
        pmdec = table['pmdec']
        radial_velocity = table['radial_velocity']
        dist = table['parallax'].to(u.parsec, equivalencies=u.parallax())

        coords = coordinates.ICRS(
            ra = ra, 
            dec = dec, 
            distance = dist, 
            pm_ra_cosdec = pmra, 
            pm_dec = pmdec, 
            radial_velocity = radial_velocity)            

        fudge = self.fudge

        X_GC_sun_kpc = fudge * 8.    #[kpc]
        Z_GC_sun_kpc = 0.025 #[kpc] (e.g. Juric et al. 2008)

        #circular velocity of the Galactic potential at the radius of the Sun:
        vcirc_kms = 220. #[km/s] (e.g. Bovy 2015)

        #Velocity of the Sun w.r.t. the Local Standard of Rest (e.g. Schoenrich et al. 2009):
        U_LSR_kms = 11.1  # [km/s]
        V_LSR_kms = 12.24 # [km/s]
        W_LSR_kms = 7.25  # [km/s]

        #Galactocentric velocity of the Sun:
        vX_GC_sun_kms = -U_LSR_kms           # = -U              [km/s]
        vY_GC_sun_kms =  V_LSR_kms+vcirc_kms # = V+v_circ(R_Sun) [km/s]
        vZ_GC_sun_kms =  W_LSR_kms           # = W               [km/s]

        # keep proper motion of Sgr A* constant! 
        vY_GC_sun_kms = X_GC_sun_kpc * vY_GC_sun_kms / X_GC_sun_kpc

        gc = coordinates.Galactocentric(
            galcen_distance = X_GC_sun_kpc*u.kpc,
            galcen_v_sun = coordinates.CartesianDifferential(
                [-vX_GC_sun_kms, vY_GC_sun_kms, vZ_GC_sun_kms] * u.km/u.s),
            z_sun = Z_GC_sun_kpc*u.kpc)

        self.galcen = galcen = coords.transform_to(gc)
        xs, ys, zs = galcen.x.to(u.kpc), galcen.y.to(u.kpc), galcen.z.to(u.kpc)
        vxs, vys, vzs = galcen.v_x, galcen.v_y, galcen.v_z

        # centre view on sun
        xmin, ymin, radius = -1 * X_GC_sun_kpc, -1 * Z_GC_sun_kpc, 35

        d2d = np.sqrt(xs.value ** 2 + ys.value ** 2)
        xperps = ys.value / d2d
        yperps = -xs.value / d2d
        vtans = np.nan_to_num((xperps * vxs.value) + (yperps * vys.value))

        print(f'observations: {len(ra)}')
        cdata = table['radial_velocity']
        
        rmax = 40.
        offset = (X_GC_sun_kpc / self.fudge) * (self.fudge - 1)
        mask = ((-500 <= vtans) & (vtans <= 700) &
                (np.abs(table['b']) < 10.) &
                (d2d > offset) & (d2d < rmax + offset))

        print(f'Filtering from {len(mask)} to {len(mask[mask])}')
        minv, maxv = -300, 500
        rr = d2d[mask]
        vv = vtans[mask]

        buckets = self.buckets
        counts = self.counts
        rsize = rmax/(self.nbins-1)
        vsize = (maxv-minv)/(self.nbins-1)
        
        for r, v in zip(rr, vv):
            bb = int((r-offset) // rsize)
            vv = int((max(min(v, maxv), minv) - minv) // vsize)
            self.vrcounts[bb, vv] += 1
            buckets[bb] += v
            counts[bb] += 1

    async def plots(self):
        
        rmax = 40.
        X_GC_sun_kpc = self.fudge * 8.    #[kpc]
        offset = (X_GC_sun_kpc / self.fudge) * (self.fudge - 1)

        ax = await self.get()
        minv, maxv = -300, 500
        extent = (offset, rmax+offset, minv, maxv)

        counts = self.counts
        assert np.alltrue((self.vrcounts.T/(counts+1)) <= 1.)
        #extent=None
        #ax.scatter(d2d[mask], vtans[mask].clip(minv, maxv), c=ys.value[mask], s=0.05)
        ax.imshow(self.vrcounts[:, 1:-1].T/(counts+1),
                  origin='lower',
                  extent=extent,
                  aspect='auto',
                  cmap=magic.random_colour())
        #ax.plot(offset + np.linspace(0, rmax, self.nbins),
        #        (buckets/counts).clip(minv, maxv), 'ro')
        ax.show()

        #ax = await self.get()
        #ax.scatter(xs.value[mask], ys.value[mask],
        #           c=vtans[mask], cmap=magic.random_colour(), s=0.05)
        #ax.show()

async def run(args):

    if args.download:
        # just download the data
        get_samples(args.bunch)
        return

    milky = Milky(args.bunch, args.topn)

    farm = fm.Farm()
    farm.add(milky)

    await farm.start()

    await farm.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--bunch', type=int, default=100)
    parser.add_argument('--topn', type=int, default=10)
    parser.add_argument('--download', action='store_true')

    magic.run(run(parser.parse_args()))
    

    
    
