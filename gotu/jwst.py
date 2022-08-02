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

from glob import glob

import random

from blume import magic, farm


class Jwst(magic.Ball):

    def __init__(self):

        super().__init__()

        self.location = messier(74)

    async def start(self):
        region = str(self.location[0]['RA']) + str(self.location[0]['DEC'])
        print(region)
        results = Observations.query_region(region)
        print(len(results))
        print(results.colnames)
        products = {}
        for x in results:

            if 'JWST' in x['dataURL']:
                plist = Observations.get_product_list(x)
                print("JJJJJJJ", len(plist))
                for product in plist:
                    #print(product)
                    #print(product.colnames)
                    print(product['size'],
                          product['dataURI'],
                          product['productFilename'])

                    products[product['dataURI']] = product
        self.products = products

    async def run(self):

        product = random.choice(list(self.products.keys()))

        print(self.products[product])

        await self.put(str(self.products[product]), 'help')

        
                             

def messier(n=74):

    messy = f'M{n}'
    
    return Simbad.query_object(messy)

if __name__ == '__main__':

    from blume import magic, farm

    fm = farm.Farm()
    fm.add(Jwst())
    magic.run(farm.start_and_run(fm))
    
