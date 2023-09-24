"""The Spanish Dancer, NGC 1566


WALLABY Early Science - III. An HI Study of the Spiral Galaxy
NGC 1566

Elagali, A.; et al. (August 2019). "WALLABY early science - III.
An HI study of the spiral galaxy NGC 1566".
Monthly Notices of the Royal Astronomical Society. 487 (2): 2797–2817.
arXiv:1905.09491. Bibcode:2019MNRAS.487.2797E. doi:10.1093/mnras/stz1448.

This paper is full of interesting information about NGC 1566.

It has estimates of key parameters such as the H1 mass of the galaxy.

"""

from astropy import constants as c, units as u

distance = 21.3 * u.megaparsec

# at 21 Mega parsec 
h1mass = 1.94e10 * c.M_sun

h2mass = 1.3e9 * u.M_sun

mbh = 8.3e6

h1_systematic_velocity = 1496 * u.km / u.s

# central_bar = 32".5

# inter galactic medium density
igm_density = 5e-5 / (u.cm**3)

# from reference... 
h1_density = 3.7e20 / (u.cm**2)

stellar_mass = h1mass / 0.29

print(f'{stellar_mass / c.M_sun:e}')

# density of earth's atmosphere
earth_atmosphere = 1e25 / (u.meter ** 3) # oxygen/nitrogen

# inter galactic medium density
density_igm = 1e-6 / (u.cm ** 3)

# so to get h1_density, just from the background would need
# a distance of
print((h1_density / density_igm).to(u.lightyear))

# to get the density of the cloud, need to figure out how thick it is
disk_height = 2.5e4 * u.lightyear

local_density = ((h1_density / density_igm).to(u.lightyear)/disk_height)

print(local_density, disk_height)
