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

h1mass = 1.94e10 * c.M_sun

h2mass = 1.3e9 * u.M_sun

mbh = 8.3e6

h1_systematic_velocity = 1496 * u.km / u.s

# central_bar = 32".5

stellar_mass = h1mass / 0.29

print(f'{stellar_mass / c.M_sun:e}')
