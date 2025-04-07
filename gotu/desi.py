"""Splitting DESI data into bunches for easier viewing.


Getting the data:

wget https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/zcatalog/v1/zall-pix-iron.fits

It's bit, so use fitsio to just extract columns we want..

magic.TableCounts exists, it would be good to have separate counts for
each DESI_TARGET.

What I really need is a generic data explorer.

"""
import fitsio
from astropy.table import Table

from blume import magic, farm

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



    
def target_expand():

    bits = 0, 1, 2, 32, 60, 61, 62
    targets = 'lrg', 'elg', 'qso', 'sky', 'bgs', 'mws', 'scnd'
    
    for path in magic.Path('.').glob('bunch_*.fits'):

        zcat = Table(fitsio.read(path))
        desi_target = zcat.field('DESI_TARGET')
        for name, bit in zip(targets, bits):
            flag = (desi_target >> bit) & 1
            zcat.add_column(flag, name=name)

        # add columns for attributes
        zcat.write('target_' + path.name)
