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
        self.level = 6
        self.clip = 25  # either side

        self.keys = deque(('parallax', 'radial_velocity'))


    async def start(self):
        """ start async task to read/download data """

        # load any bunches there are
        # for now, keep them separate
        path = Path()
        for bunch in path.glob('bunch*.fits.gz'):
            if bunch.exists():
                table = Table.read(bunch)
                self.bunches.append(table)

            if len(self.bunches) == self.nbunch:
                break

            await magic.sleep(0)

    def build_table(self):
        
        #print(hpxmap)
        # Sag A*

        table = vstack(list(self.bunches))

        self.table = table

    async def run(self):

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

        fudge = 2.

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

        XS = np.nan_to_num(
            np.vstack([xs.value, ys.value, zs.value, vxs.value, vys.value, vzs.value]).T)

        # centre view on sun
        xmin, ymin, radius = -1 * X_GC_sun_kpc, -1 * Z_GC_sun_kpc, 35

        Xlimits = [[xmin - radius, xmin + radius], [-radius, radius], [-20, 20], 
                   [-250, 250], [-250, 250], [-250, 250]]
        Xlabels = ['$x$', '$y$', '$z$', r'$v_x$', r'$v_y$', r'$v_z$']

        d2d = np.sqrt(XS[:, 0] ** 2 + XS[:, 1] ** 2)
        units = XS[:, 0:2] / d2d[:, None]
        perps = np.zeros_like(units)
        perps[:, 0] = units[:, 1]
        perps[:, 1] = -units[:, 0]
        vtans = np.nan_to_num(np.sum(perps * XS[:, 3:5], axis=1))
        R = np.sqrt(XS[:, 0] ** 2 + XS[:, 1] ** 2) # in cylindrical coordinates! # + XS[:, 2] ** 2)

        print(f'observations: {len(ra)}')
        cdata = table['radial_velocity']
        
        vmin, vmax = np.percentile(cdata, (self.clip, 100-self.clip))

        if False:
            ax = await self.get()
            ax.projection('polar')

            dist = dist.clip(max=6000)

            ax.scatter(ra,
                       dist,
                       s=0.1,
                       c=cdata.clip(vmin, vmax),
                       cmap=magic.random_colour())
            #plt.colorbar()
            #await self.put(magic.fig2data(plt))
            ax.show()
                
        ax = await self.get()
        ax.projection('mollweide')

        ras = coords.ra.rad - math.pi
        decs = coords.dec

        print(len(ras), len(decs))
        ax.scatter([x for x in ras],
                   [x.rad for x in decs],
                   s=0.1,
                   #c=cdata.clip(vmin, vmax),
                   c=vtans.clip(-300, 300),
                   cmap=magic.random_colour())


        sagra = coordinates.Angle('17h45m20.0409s')
        sagdec = coordinates.Angle('-29d0m28.118s')

        self.sagastar = sagastar = coordinates.SkyCoord(sagra, sagdec)
        print(f'sag A* {sagastar.ra} {sagastar.dec} {sagastar.galactic.l} {sagastar.galactic.b}')
        ax.scatter([sagastar.ra.rad], [sagastar.dec.rad], c='r')
        ax.show()

        ax = await self.get()
        ax.projection('mollweide')
        ax.scatter(
            (((table['l'] + 180.) % 360.)-180.)*math.pi/180.,
            table['b'] * math.pi/180., s=0.1, c=vtans, vmin=-300, vmax=300,
            cmap=magic.random_colour())
        self.vtans = vtans
        ax.show()

        ax = await self.get()
        mask = abs(vtans) < 300
        ax.scatter(R[mask], vtans[mask], c=table['l'][mask])
        ax.show()


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
    

    
    
