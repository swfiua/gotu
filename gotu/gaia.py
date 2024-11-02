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
from math import *
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

class Star(Ball):

    def d2d(self):
        """  Distance from origin in x/y plane """
        return ((self.x ** 2) + (self.y ** 2))**0.5

    def vtan(self):
        """ Tangential Velocity """
        d2d = self.d2d()
        
        xperp = self.y / d2d
        yperp = -self.x / d2d
        
        return (xperp * self.v_x) + (yperp * self.v_y)

    def rdot(self):
        """ Radial Velocity """
        d2d = self.d2d()
        
        xperp = self.x / d2d
        yperp = self.y / d2d

        return (xperp * self.v_x) + (yperp * self.v_y)

    def speed(self):

        return ((self.v_x ** 2) + (self.v_y ** 2))**0.5

    def step(self, galaxy, deltat=1e6):
        """ Step the star forward detat

        deltat:  number of years

        galaxy: spiral.Spiral() at centre of the galaxy.
        """
        r = (self.d2d() << u.lyr).value
        vtan = (self.vtan() / c.c).decompose().value


        # set galaxy CC value based on current tangential velocity
        cc = galaxy.find_cc(vtan, r)

        #if hasattr(self, 'cc'):
        #    # print some info if this is an update -- see how it is changing
        #    print('cc delta_cc', self.cc, self.cc - cc)
        #else:
        #    print('CC', cc, galaxy.v(r), vtan)
            

        self.cc = cc


        # set galaxy EE value based on rdot
        galaxy.EE = 0.
        ee = galaxy.energy(r)
        # want energy == (self.rdot ** 2)/2., so set EE so it is so
        # if rdot is negative, then want energy negative
        rdot = (self.rdot() / c.c).decompose()
        energy = (rdot*rdot)/2
        if rdot < 0:
            energy *= -1
        galaxy.EE = energy - ee

        #if hasattr(self, 'ee'):
        #    print('ee delta_ee', self.ee, self.ee - galaxy.EE)

        self.ee = galaxy.EE
        
        # change in radius if rdot were constant. FIXME take account of rdoubledot
        vinert = galaxy.vinert(r, vtan)
        rdoubledot = galaxy.rdoubledot(r, vinert)
        delta_rdot = rdoubledot * deltat
        #print('delta_rdot', delta_rdot, (self.rdot()/c.c).decompose())

        # mean rdot
        mean_rdot = (self.rdot()/c.c).decompose().value + (delta_rdot/2.)

        dr = (mean_rdot * deltat).value

        # set x to radius, y to zero
        self.x = (r + dr) * u.lyr
        self.y = 0. * u.lyr

        energy = galaxy.energy(r+dr)
        self.v_x = (((2.0 * abs(energy))**0.5) * c.c) << u.km/u.s
        if energy < 0.0:
            self.v_x *= -1
        self.v_y = -(galaxy.v(r+dr) * c.c) << u.km/u.s
 
        #self.vx = 0.0001
        #print('r dr', r, dr)
        vtan1 = galaxy.v(r + dr)
        vtan0 = galaxy.v(r)
        #print('vtan 0 1 2', vtan, vtan0, vtan1)
        energy = galaxy.energy(r + dr)
        energy = galaxy.energy(r)
        #if energy > 0.0:
        #    print('energy v_x compare', sqrt(energy) * c.c << u.km/u.s, self.v_x)
        #print('vtan delta-vtan', -vtan, vtan1, vtan1+vtan)
        #print()
        
    async def show(self):

        ax = await self.get()

        distance = self.d2d().value
        speed = self.speed().value
        x = self.x.value / distance
        y = self.y.value / distance
        vx = self.v_x.value / speed
        vy = self.v_y.value / speed
        rdot = self.rdot().value / speed
        vtan = self.vtan().value / speed
        
        #ax.arrow(0, 0, x/distance, y/distance, linestyle=':')
        ax.arrow(0, 0, x, y, linestyle='dotted')

        ax.arrow(x, y,
                 vx, vy, color='r')
        ax.arrow(x, y,
                 y * vtan,
                 -x * vtan, color='g')
        ax.arrow(x, y,
                 x * rdot,
                 y * rdot, color='b')
        ax.show()



    
class Milky(Ball):

    def __init__(self, bunch=1, path='.'): 

        super().__init__()

        self.bunches = deque()
        self.nbunch = bunch
        self.runs = 0
        self.clip = 25  # either side
        self.fudge = 2.
        self.keys = deque(('parallax', 'radial_velocity'))
        self.sleep = 1.

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
        self.window = 25000.
        self.stepsize = 1e5
        self.accelerationx = 5e-9
        self.accelerationy = 0.
        self.stepsamples = 10000
        self.nsteps = 50
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
        vrads = np.nan_to_num((yperps * vxs.value) + (-xperps * vys.value))

        print(f'observations: {len(ra)}')
        cdata = table['radial_velocity']

        rmin, rmax = self.tablecounts.minx, self.tablecounts.maxx
        mask = ((np.abs(table['b']) < 15.) &
                (d2d>rmin) & (d2d < rmax))

        rr = d2d[mask]
        vv = vtans[mask]

        print(vv[:10])
        self.gimage(table)

        self.tablecounts.update(rr, vv)
        #self.tablecounts.update(rr, vrads[mask])

        await self.tablecounts.show()
        #await self.galaxy_image.run()


    def gimage(self, table=None):
        """ Show mollweide view of galaxy """
        gi = self.galaxy_image

        table = table or self.table

        sid = 'source_id'
        if sid not in table.colnames:
            sid = sid.upper()
        pixels = [gi.ix2pixel(xx >> 35) for xx in table[sid]]
        gi.update(pixels,
                  weight=table['radial_velocity'])
        gi.update(pixels)


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


        # Find the stars in the window to use as a sample
        d2d = ((gc.x ** 2) + (gc.y ** 2))**0.5
        mask = (d2d > rmin)
        mask = mask & (d2d < rmin + rwin)
        mask = mask & ~np.isnan(dist)

        print(len(gc))
        gc = gc[mask]
        await self.spiral_gcs(gc)
        
    async def spiral_gcs(self, gc):

        mw = self.milkyway
        # simulate in radial steps of stepsize lightyears
        stepsize = self.stepsize

        # use mw rmax and rmin to get the stepsize
        nsteps = 10

        # loop round the stars in gc
        tot=self.sleep

        self.stars = deque()
        for star in gc:
            self.stars.append(
                Star(x=star.x,
                     y=star.y,
                     z=star.z,
                     v_x=star.v_x,
                     v_y=star.v_y,
                     v_z=star.v_z))

        ax = await self.get()
        ax.hist([star.d2d().value for star in self.stars], bins=40)
        ax.show()
        
        for star in self.stars:
            for step in range(nsteps):
                t1 = time.time()

                self.tablecounts.update(
                    [(star.d2d() << u.kpc).value],
                    [(star.vtan() << u.km/u.s).value])


                star.step(self.milkyway, self.stepsize)

                self.tablecounts.update(
                    [(star.d2d() << u.kpc).value],
                    [(star.vtan() << u.km/u.s).value])

                # add acceleration along the spiral
                star.v_x += (self.stepsize * self.accelerationx * c.c) << u.km/u.s
                star.v_y -= (self.stepsize * self.accelerationy * c.c) << u.km/u.s

                t2 = time.time()
                tot += t2 - t1

                if tot > self.sleep:
                    await self.tablecounts.show()
                    tot=0.
                else:
                    await magic.sleep(0)

        return
            
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

    async def circle(self):

        ax = await self.get()
        vx, vy = (np.random.random(2) - 0.5) * 2.
        #vx, vy = .5, -.5
        ax = await self.get()
        
        for theta in np.linspace(0.001, 2*pi, 16):

            x, y = cos(theta), sin(theta)

            # tangential velocity
            vtan = vx * y - vy * x

            # radial velocity
            radial = vx * x + vy * y

            print('vcheck', (vtan ** 2) + (radial ** 2), vx ** 2 + vy ** 2)

            lines = [
                [[0, x * 0.9], [0, y * 0.9]],
                [[x, x+vx], [y, y+vy]],
                [[x, x+(y*vtan)], [y, y-(x*vtan)]],
                [[x, x+(x*radial)], [y, y+(y*radial)]],
                ]

            names = ['', 'velocity', 'vtan', 'vradial']
            modes = ['--k', '-r', '-b', '-g']

            ax.plot(x, y, 'ro')

            for name, line, mode in zip(names, lines, modes):
                xx, yy = line
                ax.plot(xx, yy, mode, label=name)

        #ax.legend()
        ax.grid(True)
        ax.show()

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
    

    
    
