"""Display data from Gaia

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

2024/4/29
=========

In a recent paper X. Ou et al.
https://doi.org/10.1093/mnras/stae034 used Gaia and other data sources
to calculate a galactic rotation curve for the Milk Way.

The finding was that the galaxy had a typical rotation curve, rising
linearly to 200km/s, remaining at that velocity out to 25kpc.

Xiaowei was kind enough to provide code
(https://github.com/aceilers/spectroscopic_parallax) which shows how
to set up astropy coordinates for each Gaia observation based on a
given location of the galactic centre.

The code now has a --download option, that will download the Gaia
observations for all stars for which there is a non-null radial
velocity into a number (default=1000) of bunches.

This splits the ~34 million observations into separate files that are
downloaded using separate queries.  It is likely there will be
timeouts and failures, but you can start looking at the data as soon
as a few bunches have been downloaded.

It is recomended to create a fresh folder, cd to that folder and then
run:

    python3 -m gotu.gaia --download

You can then run:

    python3 -m gotu.gaia

To view the bunches that have been downloaded, the full dataset is not
needed to get a good qualitative feel for what is going on.

Please be nice to the Gaia servers.  TODO: look into options for
sharing tables on Gaia servers.  Also, how to summarise the data?  Bin
counts?

"""
import argparse
from collections import deque

from astropy.table import Table, vstack
from astropy import coordinates
from astropy import units as u

from astroquery.gaia import Gaia

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

def get_squeal(bunch, nbunch, columns=None, table=None):

    columns = columns or (', ').join(COLUMNS)
    table = table or TABLE

    bunch_size = int(TABLE_SIZE / nbunch)
    start = bunch * bunch_size
    end = start + bunch_size


    squeal = (f'SELECT {columns} ' +
        f'FROM {table} ' +
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


def get_samples(n=1000, columns=None, table=None):

    for bid in range(n):

        path = Path(f'bunch_{bid}.fits.gz')

        if path.exists():
            print('already exists:', path)
            continue

        squeal = get_squeal(bid, n, columns=columns, table=None)
        
        print('launching gaia async job for:', path)
        job = Gaia.launch_job_async(
            squeal,
            output_file=str(path),
            dump_to_file=True)


class Milky(Ball):

    def __init__(self, bunch=1, topn=1, path='.'): 

        super().__init__()

        self.bunches = deque()
        self.nbunch = bunch
        self.bix = 0
        self.topn = topn
        self.runs = 0
        self.clip = 25  # either side
        self.fudge = 2.
        self.keys = deque(('parallax', 'radial_velocity'))

        self.tablecounts = magic.TableCounts(
            maxx=40.,
            miny=-300, maxy=500,
            width=200, height=200)

        path = Path(path)
        for bunch in path.glob('bunch*.fits.gz'):
            if bunch.exists():
                self.bunches.append(bunch)

            if len(self.bunches) == self.nbunch:
                break

    def add_bunch(self):

        table = Table.read(self.bunches[0])
        self.bunches.rotate()
        self.table = table
        return table

    def to_galactocentric(self):

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

        self.X_GC_sun_kpc = X_GC_sun_kpc = fudge * 8.    #[kpc]
        self.Z_GC_sun_kpc = Z_GC_sun_kpc = 0.025 #[kpc] (e.g. Juric et al. 2008)

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
        
        return galcen
    
    async def run(self):

        self.runs += 1
        print("number of runs", self.runs)
        
  
        table = self.add_bunch()
        

        ra = table['ra']
        dec = table['dec']
        pmra = table['pmra']
        pmdec = table['pmdec']
        radial_velocity = table['radial_velocity']
        dist = table['parallax'].to(u.parsec, equivalencies=u.parallax())

        # get galactocentric coords
        galcen = self.to_galactocentric()

        xs, ys, zs = galcen.x.to(u.kpc), galcen.y.to(u.kpc), galcen.z.to(u.kpc)
        vxs, vys, vzs = galcen.v_x, galcen.v_y, galcen.v_z

        # centre view on sun
        X_GC_sun_kpc = self.X_GC_sun_kpc
        Z_GC_sun_kpc = self.Z_GC_sun_kpc
        
        xmin, ymin = -1 * X_GC_sun_kpc, -1 * Z_GC_sun_kpc

        d2d = np.nan_to_num(np.sqrt(xs.value ** 2 + ys.value ** 2))
        xperps = ys.value / d2d
        yperps = -xs.value / d2d
        vtans = np.nan_to_num((xperps * vxs.value) + (yperps * vys.value))

        print(f'observations: {len(ra)}')
        cdata = table['radial_velocity']

        rmin, rmax = self.tablecounts.minx, self.tablecounts.maxx
        mask = ((np.abs(table['b']) < 15.) &
                (d2d>rmin) & (d2d < rmax))

        phi = np.arctan2(xs.value, -(ys.value)) - (np.pi / 3)
        phi[phi < math.pi] += 2 * math.pi

        rr = d2d[mask]
        vv = vtans[mask]
        pp = phi[mask]

        self.tablecounts.update(rr, vv)

        await self.tablecounts.show()


    async def spirals(self):

        table = self.add_bunch()
        

        ra = table['ra']
        dec = table['dec']
        pmra = table['pmra']
        pmdec = table['pmdec']
        radial_velocity = table['radial_velocity']
        dist = table['parallax'].to(u.parsec, equivalencies=u.parallax())

        # get galactocentric coords
        galcen = self.to_galactocentric()

        
    

async def run(args):

    if args.download:
        columns = None
        if args.full:
            columns = '*'
            
        # just download the data
        get_samples(args.bunch, columns=columns, table=args.table)
        return

    milky = Milky(args.bunch, args.topn)

    farm = fm.Farm()
    farm.add(milky)

    await farm.start()

    await farm.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--bunch', type=int, default=1000)
    parser.add_argument('--topn', type=int, default=10)
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--full', action='store_true',
                        help='download all columns in table')
    parser.add_argument('--table', default=TABLE,
                        help='table name to extract')

    magic.run(run(parser.parse_args()))
    

    
    
