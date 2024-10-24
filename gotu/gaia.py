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
linearly to 200km/s, remaining at that velocity out to 25kpc.  After
that point the found a steady drop in tangential velocity.

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

At the console prmompt enter::

   magic.show()


Milky Way Rotation Curve
------------------------
The bottom 35 bits of the Gaia *source_id* encodes the Healpix pixel
number that the source lies in.

Currently going through gymnastics to get all this working nicely, it
opens up lots of interresting ideas for simulation.

"""
import argparse
from collections import deque
import time

from astropy.table import Table, vstack
from astropy import coordinates
from astropy import units as u, constants as c

from astroquery.gaia import Gaia

from scipy import integrate

from blume.magic import Ball

import numpy as np
import math
import random
from pathlib import Path

from blume import magic, hp

from blume import farm as fm

from gotu import spiral

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

    def __init__(self, bunch=1, path='.'): 

        super().__init__()

        self.bunches = deque()
        self.nbunch = bunch
        self.runs = 0
        self.clip = 25  # either side
        self.fudge = 2.
        self.keys = deque(('parallax', 'radial_velocity'))


        title = 'Milky Way rotation curve'
        self.tablecounts = magic.TableCounts(
            maxx=40.,
            miny=-300, maxy=500,
            width=200, height=200,
            title=title,
            xname='distance from galactic centre (kpc)',
            yname='tangential velocity (km/s)'
        )

        self.galaxy_image = hp.PixelCounter()

        path = Path(path)
        for bunch in path.glob('bunch*.fits.gz'):
            if bunch.exists():
                self.bunches.append(bunch)

            if len(self.bunches) == self.nbunch:
                break

        # for simulating the Milky Way, use a spiral.Spiral
        self.milkyway = spiral.Spiral()
        self.milkyway.rmax = (self.tablecounts.maxx * u.kpc / u.lyr).decompose()
        self.milkyway.rmin = 10000.
        self.window = 5000.
        self.stepsize = 100000
        self.stepsamples = 1000
        self.addfoft = True
        self.speed_factor = 1.


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

        d2d = np.nan_to_num(np.sqrt(xs.value ** 2 + ys.value ** 2))
        xperps = ys.value / d2d
        yperps = -xs.value / d2d
        vtans = np.nan_to_num((xperps * vxs.value) + (yperps * vys.value))

        print(f'observations: {len(ra)}')
        cdata = table['radial_velocity']

        rmin, rmax = self.tablecounts.minx, self.tablecounts.maxx
        mask = ((np.abs(table['b']) < 15.) &
                (d2d>rmin) & (d2d < rmax))

        rr = d2d[mask]
        vv = vtans[mask]

        self.tablecounts.update(rr, vv)

        await self.tablecounts.show()
        await self.gimage(table)

    async def gimage(self, table):
        """ Show mollweide view of galaxy """
        gi = self.galaxy_image
        pi = math.pi

        sid = 'source_id'
        if sid not in table.colnames:
            sid = sid.upper()
        pixels = [gi.ix2pixel(xx >> 35) for xx in table[sid]]
        gi.update(pixels,
                  weight=table['radial_velocity'])
        gi.update(pixels)

        await gi.run()

    async def spirals(self):
        """Use Gaia data to simulate the Milky Way rotation curve

        Take a sample from the table and simulate the rotation
        curve for the sample.

        The idea is to use a gotu.Spiral() object.

        This has a central mass, Mcent, in light years, and has
        methods to calculate the tangential velocity for a given list
        of distances from the galactic centre.

        For each Gaia observation, we know it's initial tangential
        velocity and use this to initialise integration constants.

        """
        table = self.add_bunch()

        mw = self.milkyway
        
        ra = table['ra']
        dec = table['dec']
        pmra = table['pmra']
        pmdec = table['pmdec']
        radial_velocity = table['radial_velocity']
        dist = table['parallax'].to(u.parsec, equivalencies=u.parallax())

        # get the subset we want
        gc = self.to_galactocentric()

        rmin = mw.rmin * u.lyr
        rwin = self.window * u.lyr

        # simulate in radial steps of stepsize lightyears
        stepsize = self.stepsize

        # use mw rmax and rmin to get the stepsize
        nsteps = int((mw.rmax - mw.rmin) / stepsize)

        # Find the stars in the window to use as a sample
        d2d = ((gc.x ** 2) + (gc.y ** 2))**0.5
        mask = (d2d > rmin)
        mask = mask & (d2d < rmin + rwin)
        mask = mask & ~np.isnan(dist)

        gc = gc[mask]


        tt = 0.

        rrr = np.linspace(0, stepsize, self.stepsamples)
        ttt = np.linspace(0, stepsize, self.stepsamples)
        
        # loop round the stars in gc
        for ix in range(len(gc)):

            # get the star at this index
            star = gc[ix]

            for step in range(nsteps):

                t1 = time.time()

                velocity = ((star.v_x ** 2) + (star.v_y ** 2)) ** 0.5
                d2d = ((star.x ** 2) + (star.y ** 2))**0.5
                xperp = star.x / d2d
                yperp = -star.y / d2d
                vtan = (xperp * star.v_x) + (yperp * star.v_y)
                # vradial = (yperp * star.v_x) + (xperp * star.v_y) # ??
                
                vel =  ((velocity / c.c).decompose()).value

                myrstart = (d2d << u.lyr).value
                # set CC value of mw object
                mw.find_cc((vtan / c.c))

                # use my starting radius to get rvals to evaluate
                rvals = myrstart + rrr

                # set mw.EE based on energy at start
                mw.EE = 0.0
                ee = mw.energy(rvals[:1])

                # want (vel ** 2)/2.  to be energy, so set EE to make this happen
                mw.EE = ((vel ** 2.0) / 2.0) - ee

                # tangential velocity from mw
                vv = ((mw.v(rvals) * c.c) << u.km/u.s).value

                # add a random term based on time and an acceleration too
                fudge = 0.
                if not self.addfoft:
                    # calculate rdot and tvalues
                    rdots = np.array([2 * (mw.energy(rval)**0.5) for rval in rvals])
                    tvalues = integrate.cumtrapz(1/rdots, rvals, initial=0) 
                    print(rvals)
                    print(rdots)
                    print(tvalues)
                    fudge = np.nan_to_num(self.foft(tvalues, vv))
                    
                self.tablecounts.update(
                    ((rvals * u.lyr) << u.kpc).value,
                    vv + fudge)

                # update the star position and velocity to that
                # at the end of the steps

                # get final rdot, needed for updating star
                rfinal = rvals[-1]
                rdot = 2 * (mw.energy(rvals[-1]))**0.5

                gc.data.x[ix] = rfinal * u.lyr
                gc.data.y[ix] = 0. * u.lyr

                gc.v_y[ix] = (vv[-1] * c.c) << u.km/u.s
                gc.v_x[ix] = (rdot * c.c)

                # we are changing gc in place so
                # this voodoo is needed to pick up new values
                # properly -- hope it works!
                gc.cache.clear()

                # update star
                star = gc[ix]
                
                # check radii make sense
                newd2d = ((star.x ** 2) + (star.y ** 2))**0.5

                t2 = time.time()
                tt += t2-t1
                if tt > self.sleep:
                    tt = 0.
                    await self.tablecounts.show()
                else:
                    await magic.sleep(0)
                    
        await self.tablecounts.show()
            
    def foft(self, tvalues, vtans):
        """ Model factors not modelled in spirals.

        Each star is subject to random motions as it moves outward
        along the spiral arms.

        Each star feels the curvature of space time.
        """

        last_tt = tvalues[0]
        last_vtan = vtans[0]

        errors = [0.]
        for tt, vtan in zip(tvalues[1:], vtans[1:]):
            delta_t = tt - last_tt
            error = np.random.normal()
            error *= (delta_t * self.speed_factor * u.km/u.s)
            errors.append(errors[-1] + error.value)

        return errors
        
        delta_t = tvalues[-1] - tvalues[0]
        vtan = np.mean(vtans)
        distance = abs(vtan) * delta_t
        curve = self.milkyway.cosmo.H0 * distance * u.km << u.km/u.s

        rand = np.random.normal() * delta_t * self.speed_factor
        #print('tvdh', delta_t, vtan, distance, curve, rand)
        return curve.value + rand


async def run(args):

    if args.download:
        columns = None
        if args.full:
            columns = '*'
            
        # just download the data
        get_samples(args.bunch, columns=columns, table=args.table)
        return

    milky = Milky(args.bunch)

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
    

    
    
