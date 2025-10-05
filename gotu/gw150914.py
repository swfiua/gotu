"""
Thanks to the Gravitational Wave Open Science Center for event catalogs and data.

https://gwosc.org/eventapi/html/GWTC/
"""

from astropy import table, io, units as u, constants as c

from pycbc import waveform

import csv

from blume import magic, farm

from . import spiral

m1 = 35.6 * u.M_sun
m2 = 30.6 * u.M_sun

mfinal = 63.1 * u.M_sun

mwave = 3.1 * u.M_sun

chirp =  28.6 * u.M_sun

distance = 430 * u.Mpc


def read_csv(infile):

    line = infile.readline()
    
    fields = [x.strip() for x in line.split(',')]

    reader = csv.DictReader(infile, fieldnames=fields)

    # skip first line
    reader.__next__()

    data = [x for x in reader]
    
    spell = magic.Spell(keys=fields)

    spell.find_casts(data, sniff=218)
    print(spell.casts)
    print(len(data))
    yield from spell.spell(data)
    
def transdict(data):

    result = {}

    for row in data:
        for k, v in row.items():
            result.setdefault(k, []).append(v)

    return result


class View(magic.Ball):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


    async def zerochirp(self):

        data = self.table
        
        m1 = data['mass_1_source']
        m2 = data['mass_2_source']

        chirp = ((m1 * m2)**0.6)/((m1 + m2)**0.2)
        
        redshift = data['redshift']

        zzerochirp = chirp / (1 + redshift)

        ax = await self.get()
        bins = 25
        ax.hist(zzerochirp, bins)
        ax.set_title('z-zero chirp')
        #ax.plot(sorted(zzerochirp))

        ax.show()
        ax = await self.get()
        ax.hist(chirp, bins)
        ax.show()
        ax = await self.get()
        ax.plot(redshift)
        ax.show()


        
    async def run(self):

        fields = ['mass_1_source', 'mass_2_source', 'redshift']
        
        for row in self.table.iterrows(*fields):

            m1, m2, redshift = row

            delta_t = 0.001
            
            try:
                wf = waveform.get_td_waveform(
                    mass1=m1,
                    mass2=m2,
                    approximant='TaylorF2', delta_t=delta_t, f_lower=20)
            except:
                print(m1, m2, 'bad')
                continue

            ts = wf[0]
            nn = len(ts)


            ax = await self.get()
            ax.plot(magic.np.arange(len(ts)) * delta_t, ts)
        
            ax.set_title(f"Solar Masses: {m1:.1f} {m2:.1f}")
            ax.show()

            await magic.sleep(self.sleep)



            
if __name__ == '__main__':

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--events', default='events.csv')

    args = parser.parse_args()
    
    data = list(read_csv(open(args.events)))

    data = transdict(data)
    
    data = table.Table(data)


    land = farm.Farm()
    land.add(View(table=data))
    farm.run(land)
        
