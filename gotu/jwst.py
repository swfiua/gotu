"""Just What's a Space Telescope?

A super cool, giant infra-red eye.

From nearby galaxies it shows a view of the dust of the galaxies as it
glows in the infra-red.

Further out it sees galaxies red-shifted due to the speed of their
Hubble driven recession.

Then there are quasars too.

The light from the glowing of the dust is stretched by the slowing of
time by the baby galaxy's central black hole. 

The end result is that it is difficult to judge the distance of a galaxy. 

Size, distance, mass of central black hole all affect the actual red shift.

And then there are the beauties of de-Sitter Space to consider.  

Geodesics which separate expontentially in both forwards and backwards time. 

We see each source blue shifted, but a small finite part, which might
in fact be quite large, before it shifts for ever into the Hubble flow. 

Space is spinning by, not expanding, but rather bouncing in harmonies.

Red-shift is more complicated than a simple matter of distance.

Will we see baby galaxies that are red shifted due to dust clouds
close enough to central black holes that the infra-red energy we see
is in fact the light from the stars in the galaxy, red-shifted by the
massive black hole driving a quasar?

JWST Data
=========

If you can just find the url of the fits file you want then things are
quite simple.   

The way to find what you are looking for is to query the Mast
database.  

The simplest query you can make is to call query region and pass it
the location in the sky you are interested in.

To get the actual location to query there is another handy database
that you can query to get the location if you know it's name.

Right now, I happen to be interested in M74, also known as NGC 628.  

"""

from astroquery.mast import Observations
from astroquery.simbad import Simbad

from astropy.table import Table
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from glob import glob

import random
from collections import Counter, defaultdict, deque
from pathlib import Path

from blume import magic, farm, taybell, modnar
from matplotlib import image
import numpy as np
import json
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None

class Jwst(magic.Ball):

    def __init__(self):

        super().__init__()
        self.locations = deque((
            'HD 147980',
            'NGC 3132',
            'SMACS 0723',  #  deep field?
            'NGC 7318B',   # Stephen's Quintet?
            'M 74',       # NGC 628 Phantom Galaxy
            'NGC 3324',   # Carina Nebula
            'PGC 2248'))  # Cartwheel

        self.topn = 1
        self.do_product_list = False
        self.maxrows = 15

    async def show_stats(self, table):

        msg = self.table_count(table)
        await self.put(msg, 'help')
        
    def table_count(self, table, maxrows=None):

        msg = []
        counters = defaultdict(Counter)
        for ix, row in enumerate(table):
            if self.maxrows and ix > self.maxrows:
                break
            
            for key in row.colnames:
                value = row[key]
                if isinstance(value, np.ma.core.MaskedConstant):
                    value = value.tolist()
                counters[key].update([value])
        for key in table.colnames:
            for value, count in counters[key].most_common(self.topn):
                value = taybell.shortify_line(str(value), 20)
                
                msg.append([key, value, count])

        return msg

    def name_to_skycoord(self, name):

        location = Simbad.query_object(name)[0]
        ra, dec = location['RA'], location['DEC']
        skypos = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
        return skypos

    async def get_observations(self, skypos):

        filename = Path(f'skypos_{skypos.ra.deg}_{skypos.dec.deg}.fits')
        if filename.exists():
            results = Table.read(filename)
        else:
            print('querying mast database')
            results = Observations.query_region(skypos)
            # find the JWST ones
            mask = results['project'] == 'JWST'
        
            results = results[mask]

            # save a copy of the results
            results.write(filename)

        # Fileter some more -- need to make this optional
        mask = [Path(x['dataURL']).stem.endswith('i2d') for x in results]
        results = results[mask]
        mask = [Path(x['dataURL']).stem.endswith('i2d') for x in results]
        results = results[mask]

        await self.show_stats(results)

        return results
            
    async def start(self):

        skypos = self.name_to_skycoord(self.locations[0])
        print(self.locations[0], skypos)

        # get observations
        results = await self.get_observations(skypos)

        print('Region size:', len(results))
        names = list(results.colnames)
        products = {}
        counters = defaultdict(Counter)

        for x in results:

            if 'JWST' in x['dataURL']:
                print(x['dataURL'])
                products[x['dataURL']] = x
                         
                if self.do_product_list:
                    plist = Observations.get_product_list(x)
                    print("JJJJJJJ", len(plist))
                    for product in plist:
                        
                        for name in product.colnames:
                            counters[name].update([str(product[name])])
                         

                    products[product['dataURI']] = product
                         

                for key, counts in counters.items():
                    print(key)
                    print(counts.most_common(3))
            
        self.products = products
        self.locations.rotate()

    async def run(self):
                         

        product = random.choice(list(self.products.keys()))

        prod = self.products[product]
        msg = []
        for key in prod.colnames:
            msg.append([key, taybell.shortify_line(str(prod[key]), 20)])
        #print(msg)

        #await self.put(msg, 'help')

        #print(type(prod))
        #print('FFFFFFFFFFFFFFFFF', 'jpegURL' in prod)

        # download the product
        #result = Observations.download_file(prod['dataURI'])
        #for key in ('jpegURL', 'dataURL', 'dataURI'):
        for key in ('jpegURL',):
            
            if key not in prod.colnames:
                continue

            path = Path(prod[key])
            filename = path.name
            print(path)
            if not path.stem.endswith('i2d'):
                print('skipping', filename)
                print()
                continue
            
            result = Observations.download_file(str(path))
            
            if not Path(filename).exists():
                print('DOWNLOAD FAIL for ', filename)
                continue
            
            if filename.endswith('fits'):
                continue
                tab = fits.open(filename)
                for item in tab:
                    print(item.size)
                if isinstance(item.size, int):
                    print('Array size:', item.size)
                elif item.size:
                    #await self.show_stats(item)
                    pass
                
                print(tab.info())

            elif filename.endswith('jpg') or filename.endswith('png'):
                ax = await self.get()
                ax.imshow(image.imread(filename), cmap=modnar.random_colour())
                ax.show()

            elif filename.endswith('json'):
                msg = json.load(open(filename))
                msg = [(key, value) for item in msg.items()]
                await self.put(msg, 'help')

        
                             

def messier(n=74):

    messy = f'M{n}'
    
    return Simbad.query_object(messy)

if __name__ == '__main__':

    from blume import magic, farm

    fm = farm.Farm()
    fm.add(Jwst())
    magic.run(farm.start_and_run(fm))
    
