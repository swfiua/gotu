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

Update 2022/8/20
================

The code here has been on a bit of an adventure, because I wanted to
get this running under pyodide in the browser.

There is no access to sockets, so querying databases is more complex.

There is no requests module on pyodide but there is pyodide-requests
that implements a minimal requests using javascript apis.

Everything is working except for the download of the file, which the
browser blocks due to it being a *cross origin request sharing* issue.

The code has got a little more complicated, but no longer requires
*astroquery*, which is also unavailable on pyodide.  

But what is JWST seeing?
------------------------

There has been a lot of excitement about galaxies of high redshift.
The key number is *z* and is the ratio of the wavelenth we observe to
what it was at the origin.

There are many reports of many z>=10 in the first images.  There has
also been some recalibration of the instrument that has generally
reduced the red shifts observed.


"""

#from astroquery.mast import Observations
#from astroquery.simbad import Simbad
import asyncio
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
import io
import requests

# make things pretty 
from pprint import pprint

import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None

MAST_URL = "https://mast.stsci.edu/api/v0/invoke?request="
MAST_DOWNLOAD = "https://mast.stsci.edu/api/v0.1/Download/file?uri="


def query_region(skypos, project='JWST'):

    request = {'service':'Mast.Caom.Cone',
               'params': {'ra':skypos.ra.deg,
                          'dec':skypos.dec.deg,
                          'radius':0.2,
                          
                         
                          'filters': [
                              {"paramName": "dataRights",
                               "values": ['public'],
                               },
                              {"paramName": "project",
                               "values": [project],
                               },
                          ]},
               'format':'json',
               'pagesize':2000,
               'removenullcolumns':True,
               'timeout':30,
               }

    pprint(request)
    response = mast_query(request)
    
    return response_to_table(response)

def response_to_table(response):
    
    content = response_to_json(response)

    fields = content['fields']
    names = [x['name'] for x in fields]
    dtype = [x['type'] for x in fields]

    typemap = dict(string=str,
                   boolean=bool)
    dtype = [typemap.get(x, x) for x in dtype]
    
    return Table(content['data'], names=names, dtype=dtype)

def object_lookup(obj):
    """ Return location give string such as M74 or NgC3132
    
    Returns an astropy.coordinates.SkyCoord
    """
    
    request = {'service':'Mast.Name.Lookup',
               'params':{'input':obj,
                         'format':'json'},
               }
    print(f'looking up {obj} {request}')
    response =  mast_query(request)

    info = response_to_json(response)

    records = info['resolvedCoordinate']
    location = records[0]
    
    ra, dec = location['ra'], location['decl']
    skypos = SkyCoord(ra, dec, unit=(u.deg, u.deg))
    return skypos

def response_to_json(response):

    return json.loads(response.text)

def mast_query(request):
    
    result = requests.get('%s%s' % (MAST_URL, json.dumps(request)))
    if result.status_code != 200:
        raise requests.HTTPError(result.status_code)

    return result

    

def open_file(uri):

    target = f'{MAST_DOWNLOAD}{uri}'
    print(target)
    result = requests.get(target)

    if result.status_code != 200:
        print('STATUS', result)
        raise IOError()

    return io.BytesIO(result.content)

def download_file(uri):

    filename = Path(Path(uri).name)

    if filename.exists():
        print('Using cached file', filename)
        return

    try:
        # make this async?
        data = open_file(uri)
    except:
        return False
    
    filename.write_bytes(data.read())
    
    return True

class Jwst(magic.Ball):
    """ Explore JWST data """
    def __init__(self):

        super().__init__()
        self.locations = deque((
            'M 16',  # pillars of creation, eagle nebula
            'HD 147980',
            'NGC 3132',
            'SMACS 0723',  #  deep field?
            'NGC 7318B',   # Stephen's Quintet?
            'M 74',       # NGC 628 Phantom Galaxy
            'NGC 3324',   # Carina Nebula
            'PGC 2248'))  # Cartwheel

        self.project = 'JWST'
        self.i2d = False
        self.filetypes = set(('.jpg', '.png'))

        self.topn = 1
        self.do_product_list = False
        self.maxrows = 15

    async def show_stats(self, table):

        msg = self.table_count(table)
        print(table.colnames)
        if len(table) != 0:
            print(msg)
            await self.put(msg, 'help')
        else:
            await self.put([['no data'], ['for'], [self.locations[0]]], 'help')
        
    def table_count(self, table, maxrows=None):
        """ Do some counts on a table 
        
        pretty sure there is some sort of table.info.stats()
        """
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

        return object_lookup(name)

    async def get_observations(self, skypos, name='unknown'):

        if self.project:
            filename = Path(f'skypos_{name}_{self.project}_{skypos.ra.deg}_{skypos.dec.deg}.fits')
        else:
            filename = Path(f'skypos_{name}_{skypos.ra.deg}_{skypos.dec.deg}.fits')
        if filename.exists():
            results = Table.read(filename)
        else:
            print('querying mast database')
            #loop = asyncio.get_event_loop()
            results = query_region(skypos, self.project)
            #results = loop.run_in_executor(
            #    query_region, (skypos, self.project))
            #results = Observations.query_region(skypos)
            # find the JWST ones
            if self.project:
                mask = results['project'] == self.project
        
                results = results[mask]

            await self.show_stats(results)

            #results.info()
            #results.info('stats')
                  
            
            # save a copy of the results
            results.write(filename)

        # Filter some more -- need to make this optional
        if self.i2d:
            mask = [Path(x['dataURL']).stem.endswith('i2d') for x in results]

            results = results[mask]

        await self.show_stats(results)

        return results
            
    async def start(self):

        name = self.locations[0]
        skypos = self.name_to_skycoord(name)
        print(name, skypos)

        # get observations
        results = await self.get_observations(skypos, name=name)

        print('Region size:', len(results))
        names = list(results.colnames)
        products = {}
        counters = defaultdict(Counter)

        for x in results:

                print(x['dataURL'])
                products[x['dataURL']] = x
                         
                if self.do_product_list:
                    plist = Observations.get_product_list(x)
                    print("JJJJJJJ", len(plist))
                    for product in plist:
                        
                        for name in product.colnames:
                            counters[name].update([str(product[name])])
                         

                    products[product['dataURI']] = product
                         

                #for key, counts in counters.items():
                #    print(key)
                #    print(counts.most_common(3))
            
        self.products = products
        self.locations.rotate()

    async def run(self):
                         
        while True:
            product = random.choice(list(self.products.keys()))
            if self.products[product]:
                break

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
        filetypes = self.filetypes
        #for key in ('jpegURL', 'dataURL', 'dataURI'):
        for key in ('jpegURL', 'dataURL'):
            
            if key not in prod.colnames:
                continue

            filename = Path(prod[key])

            if filename.suffix not in filetypes:
                print('filtered out by filetype ', filename.suffix, filename)
                if product in self.products:
                    del self.products[product]
                continue
            
            result = download_file(str(filename))

            if not Path(filename.name).exists():
                print('DOWNLOAD FAIL for ', filename)
                continue
            
            if filename.suffix == '.fits':
                
                tab = fits.open(filename.name)
                print(tab.info())
                for item in tab:
                    print(item.size)
                if isinstance(item.size, int):
                    print('Array size:', item.size)
                elif item.size:
                    #await self.show_stats(item)
                    pass
                
                #print(tab.info())

            elif filename.suffix == '.jpg' or filename.suffix == '.png':
                ax = await self.get()
                ax.imshow(image.imread(filename.name),
                          cmap=modnar.random_colour())
                ax.show()

            elif filename.suffix == '.json':
                msg = json.load(open(filename))
                msg = [(key, value) for item in msg.items()]
                await self.put(msg, 'help')

        
                             


if __name__ == '__main__':

    from blume import magic, farm
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--location')
    parser.add_argument('--survey')
    parser.add_argument('--size', type=int)
    parser.add_argument('--project', default=None)
    parser.add_argument('--i2d', action='store_true')
    parser.add_argument('--fits', action='store_true')

    args = parser.parse_args()

    fm = farm.Farm()

    jwst = Jwst()
    if args.location:
        jwst.locations.appendleft(args.location)

    if args.project:
        jwst.project = args.project

    if args.survey:
        jwst.locations.clear()
        locations = [args.survey + str(int(x)) for x in range(1, args.size+1)]
        random.shuffle(locations)
        for location in locations:
            jwst.locations.append(location)

    jwst.i2d = args.i2d
    if args.fits:
        jwst.filetypes = ['.fits']
        
    fm.add(jwst)
    magic.run(farm.start_and_run(fm))
    
