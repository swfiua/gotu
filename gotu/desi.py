"""Splitting DESI data into bunches for easier viewing.


Getting the data:

wget https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/zcatalog/v1/zall-pix-iron.fits

It's bit, so use fitsio to just extract columns we want..

magic.TableCounts exists, it would be good to have separate counts for
each DESI_TARGET.

What I really need is a generic data explorer.

de Sitter begins with DESI

"""
import time
import fitsio
from astropy.table import Table
from astropy import io

from scipy import ndimage

from blume import magic, farm, train
from gotu import birch
np = magic.np

columns = ['TARGETID', 'SURVEY', 'PROGRAM', 'DESI_TARGET', 'Z',
           'SPECTYPE', 'ZWARN', 'DELTACHI2', 'FLUX_G', 'FLUX_R', 'FLUX_Z',
           'ZCAT_PRIMARY', 'HEALPIX']


def bunches(nbunch=1000):
    """ Split main file into nbunch separate files
    """
    filename = 'zall-pix-iron.fits'
    zcat = Table(fitsio.read(filename,
                             columns=columns))


    size = len(zcat)

    # want bunchsize such that we get nbunch files
    bunchsize = size//nbunch
    pos = 0

    for ix in range(nbunch):
        pos = ix * bunchsize
        rows = range(pos, pos+bunchsize)
        zcat = Table(fitsio.read(filename,
                                 columns=columns,
                                 rows=rows))

        print(ix)
    zcat.write(f'bunch_{ix}.fits')


def expand_targets():

    for path in magic.Path('.').glob('bunch_*.fits'):
        zcat = Table(fitsio.read(path))

        zcat = target_expand(zcat)

        # save modeified file
        zcat.write('target_' + path.name)


class Zplotter:

    def __init__(self,
                 minwl=1000., maxwl=6000, deltawl=0.1,
                 minz=0, maxz=4, deltaz=0.1):

        self.minwl = minwl
        self.maxwl = maxwl
        self.deltawl = deltawl
        self.minz = minz
        self.maxz = maxz
        self.deltaz = deltaz

        self.reset()

    def reset(self):
        """ Call after setting parameters """
        self.bands = int((self.maxz-self.minz) / self.deltaz)
        self.wls = int((self.maxwl - self.minwl) / self.deltawl)
        self.data = np.zeros((self.bands, self.wls))
        self.counts = np.zeros((self.bands, self.wls))
        deltawl2 = self.deltawl/2.
        self.dwaves = np.linspace(self.minwl + deltawl2,
                                  self.maxwl - deltawl2, len(self.data[0]))
    def update(self, zz, xx, yy):
        """ Update count

        zz  redshift
        xx  array of x values (wavelength)
        xx  array of y values (flux)
        """

        deltaz2 = self.deltaz/2.

        # adjust xx for zz
        xxz = xx / (1+zz)
        band = int((zz-self.minz)/ self.deltaz)
        band = min(band, self.bands-1)
        ix = int(max(xxz[0] - self.minwl, 0) / self.deltawl)
        lix = int(min(xxz[-1] - self.minwl, self.maxwl-self.minwl) / self.deltawl) - 1

        # range of wavelengths is xxz[0] - xxz[-1]
        data = np.interp(self.dwaves[ix:lix+1], xxz, yy, 0., 0)

        self.data[band][ix:lix+1] += data
        self.counts[band][ix:lix+1] += 1

    def show(self, ax):

        for ix, row in enumerate(self.data):
            ok = self.counts[ix] != 0
            xx = self.dwaves[ok]
            yy = (2*ix) + (row[ok]/(1+self.counts[ix][ok]))
            ax.plot(xx, yy)
    
def target_expand(zcat):

    bits = 0, 1, 2, 32, 60, 61, 62
    targets = 'lrg', 'elg', 'qso', 'sky', 'bgs', 'mws', 'scnd'
    
    desi_target = zcat.field('DESI_TARGET')
    for name, bit in zip(targets, bits):
        flag = (desi_target >> bit) & 1
        zcat.add_column(flag, name=name)

    return zcat

class DESI(train.Train):
    """ de Sitter Space begins with DESI """

    def __init__(self):

        super().__init__()

        self.add_filter(' ', self.next_mode)
        self.add_filter('l', self.show_fibermap)

        self.mode = magic.deque(['elg', 'bgs', 'lrg', 'qso'])

        self.tablecounts = magic.TableCounts(
            minx=1000, maxx=6000,
            miny=0, maxy=16.
        )

        self.minz = 0.0
        self.maxz = 1.5

        self.zplot = Zplotter(minz=self.minz, deltaz=0.25)

    def next_mode(self):

        self.mode.rotate()
        self.next_table()
        self.tablecounts.reset()

    async def start(self):
        """ FIXME: scan a table of what's here

        generate meta data for carpet.
        option to save meta data.

        feels like next_table()
        should just be a deque of tables

        only if the deque is empty should it create a new one
        """

        self.runs = 0
        
        if not self.paths:
            if self.path.is_file():
                self.paths = [self.path]
            else:
                path = Path(self.path)
                self.paths = list(path.glob(self.glob))
        else:
            self.paths = [magic.Path(path) for path in self.paths]
        self.paths = magic.deque(sorted(self.paths))

        self.next_table()

    def next_table(self):
        
        redname = self.paths[0]
        specname = redname.with_name(redname.name.replace('redrock', 'coadd'))

        self.redrock = io.fits.open(redname)
        self.spectra = io.fits.open(specname)

        self.fibermap = target_expand(Table(self.spectra['FIBERMAP'].data))
        self.paths.rotate()

        reds = self.redrock['REDSHIFTS'].data['Z']
        mags = self.fibermap['FLUX_G']
        ixes = np.arange(0, len(reds))

        #ok = [True] * len(ixes)
        ok = self.fibermap[self.mode[0]] == 1

        if self.minz is not None:
            ok = ok & (reds > self.minz)

        if self.maxz is not None:
            ok = ok & (reds < self.maxz)

        ok = ok & (mags >= 5.)

        ixes = ixes[ok]
        #self.sixes = magic.deque([x[1] for x in sorted(zip(reds[ok], ixes))])
        self.sixes = magic.deque([x[1] for x in sorted(zip(reds[ok], ixes))])
        self.means = {}
        self.redname = redname

    def guess_parms(self):
        """ Estimate mass, distance and cosmological redshift (or blue shift)

        This is tricky!

        If cosmological redshift is not a good guide to distance and
        gravitational redshift is a thing then how do we unravel things?

        The mass gives us the redshift via a spiral.Spiral object.

        It also gives us the magnitude and hence distance.
        """
        # Work with current record
        ix = self.sixes[0]

        # wonder which flux value to use for magnitude
        flux = self.fibermap['FLUX_G']

        
    def show_fibermap(self):
        """ Try show something interesting about current observation """
        tab = self.fibermap[self.sixes[0]]
        rows = [['Z', self.redrock['REDSHIFTS'].data['Z'][self.sixes[0]]]]
        brows = []
        for key, value in zip(tab.keys(), tab.values()):

            good = False
            if key.lower() == key:
                good = True
            fields = key.split('_')
            for band in 'G', 'B', 'Z', 'R', 'W1', 'W2':
                if band in fields:
                    good = True
            if good:
                rows.append([key, value])
            else:
                brows.append([key, value])

        self.put_nowait(brows, 'help')
        self.put_nowait(rows, 'help')

    def waveplot(self, ax, band, vmin=-3, vmax=5.):

        tab = self.spectra
        ix = self.sixes[0]
        xx = tab[band + '_WAVELENGTH'].data
        #norm = self.fibermap['FLUX_'+band.replace('B', 'G')][ix]
        norm = self.fibermap['FLUX_Z'][ix]

        yy = tab[band + '_FLUX'].data[ix] / norm

        ok = tab[band + '_IVAR'].data[ix] > 0.

        def gf(x):

            return ndimage.gaussian_filter1d(x, 5.)

        reds = self.redrock['REDSHIFTS'].data['Z'][ix]

        offset = int(reds/0.25)

        if ax: ax.plot(xx[ok]/(1+reds), gf(yy[ok])+offset)
        
        mean = self.means.setdefault(band, yy)
        alpha = 0.95
        mean = alpha * mean + ((1-alpha) * yy)
        self.means[band] = mean
        
        #ax.plot(xx/(1+reds), np.clip(gf(mean), vmin, vmax))

        #ax.plot(xx[ok]/(1+reds),
        #        np.clip(np.sqrt(1./tab[band + '_IVAR'].data[ix][ok]),
        #                vmin, vmax)+vmin)

        self.tablecounts.update(xx[ok]/(1+reds), yy[ok] + offset)

        self.zplot.update(reds, xx[ok], yy[ok])

    async def run(self):


        tot = 0.0
        ax = None

        while True:
            self.runs += 1
        
            while self.sixes:
                ix = self.sixes[0]
                zwarn = self.redrock['REDSHIFTS'].data['ZWARN'][ix]
                norm = self.fibermap['FLUX_Z'][ix]

                if zwarn != 0 or norm ==  0.:
                    self.sixes.popleft()
                    continue

                t1 = time.time()
                self.waveplot(ax, 'B')
                self.waveplot(ax, 'R')
                self.waveplot(ax, 'Z')
                
                tot += time.time() - t1
                if tot > self.sleep:

                    axes = await self.tablecounts.show()

                    ax = await self.get()
                    self.zplot.show(ax)
                    ax.show()
                    await magic.sleep(self.sleep)
                    tot = 0.0

                    ax = axes['nonorm']
                else:
                    if ax:
                        ax.show()
                        self.show_fibermap()
                    ax = None
                    await magic.sleep(0)
        
                self.sixes.popleft()

            self.paths.rotate()
            print('loading next table', self.paths[0])
            self.next_table()


            
if __name__ == '__main__':

    
    land = farm.Farm()
    land.add(DESI())
    farm.run(land)
    
