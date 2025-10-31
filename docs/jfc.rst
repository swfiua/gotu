========================
 Fred, Colin and Jayant
========================

Fred Hoyle, Colin Rourke and Jayant Narlikar.

::

   The Big Bang is an Exploding Myth

   Jayant Narlikar


Fred Hoyle was the original Big Bang sceptic, and founder of the term,
Big Bang.

Fred Hoyle guided Jayant Narlikar through his doctorate in theoretical
cosmology at Cambridge in 1963.

Colin Rourke provided a geometric model for the universe.
   
All three are no longer with us.  Hoyle died in 2001.  It was around
that time that Rourke started his work on cosmology, so this was not
in time to point Hoyle in the right direction.

Rourke died in December 2024, believing it could be another 50 years
before the community moves away from the big bang theory.

I had submitted the talk proposal, :ref:`birch` to the :ref:`gr24`
conference before I learnt of his passing.  The talk was not accepted,
which was likely a blessing.  It turns out the story is more complex
than I originally thought, I had over-looked the importance of
understanding the :ref:`quasar` galaxy spectrum, as explained in his
work.

With Rourke's passing it seemed more important than ever for me to
explore gravitational waves in the context of his geometric model for
the universe.  Glasgow was an excellent opportunity to explore the
world of gravitational wave science and seek out others that might
have an interested in static universe theories.

Sadly, it was during the conference that I learn of Jayant Narlikar's
passing in June 2025.  I spoke to a number of researchers from India
during the conference, there was a lot of excitement about the
prospects for the Indian LIGO.  One recalled the quote on Jayant's
office door and also broke the news of his passing.

It is not clear if Jayant Narlikar was aware of Rourke's work, but he
remained confident that the Big Bang theory was a mistake.

He explored models based on Hoyle's continuous creation idea.  Hoyle
had noted that it was only necessary to create one new proton, for
every skyscraper sized volume of space, per year, in order to balance
the observed expansion.

::

   >>> from gotu import spiral
   >>> from astropy import units as u, constants as c

   >>> skyscraper = (100 * u.m) ** 3

   >>> sm = spiral.SkyMap()

   >>> sm.volume_of_universe / skyscraper

   >>> suns_per_galaxy = 1e12

   >>> (c.m_p * sm.volume_of_universe / skyscraper) / (c.M_sun * suns_per_galaxy)
   <Quantity 9005.30129857>


So based on a sky-scraper being a 100m cube, and galaxies of a mass of
1e12 solar masses, we would need 9000 new galaxies arriving each year.

The number of large gamma-ray bursts per year that we see each year is
somewhat lower than this.

There are some details missing from Hoyle's calculation.  With a
larger Hubble constant, the universe is smaller and the calculation
gives a good match, if we also increase sky-scraper height by a factor
of 3.

Then we have to factor in how the outward flow changes with the size.

    >>> lcdm = cosmology.FlatLambdaCDM(H0=100, Om0=0.3)
    >>> lcdm .hubble_distance
    >>> <Quantity 2997.92458 Mpc>

    >>> hd = lcdm.hubble_distance
    >>> 
    >>> volume_of_the_universe = (pi * 4/3) * (hd**3)
    >>> 
    >>> ((volume_of_the_universe / skyscraper) * c.m_p / (c.M_sun * suns_per_galaxy)).decompose()
    <Quantity 278.92935871>
    >>> skyscraper = ((100 * u.m) ** 3) * 3
    >>> ((volume_of_the_universe / skyscraper) * c.m_p / (c.M_sun * suns_per_galaxy)).decompose()
    <Quantity 92.9764529>


There is no continuous creation in Rourke's model for the universe,
but there is a continuous replenishment of matter in our visible
universe through new arrivals.  

The idea is that the universe is vast and ancient, a view shared by
this trio, myself and many others, including Einstein.

It is also curved, that curvature creates a visibility horizon at the
Hubble distance. 

This is what creates the redshift we see, but it also creates
blue-shift.

When a galaxy becomes visible for the first time, we see it's entire
history in a short period of time.  Rourke suggests this as an
explanation for gamma-ray bursts and provides a model which fits the
observations.

Is it the same for any gravitational waves that we see? All the
gravitational waves it has emitted through it's life time arrive at
the same time!

There are natural parallels with the merging black hole model.

We are seeing the effects of horizons in our visible universe.

Rourke's model can also inform models of galactic potential, the
Pulsar Timing Array can help test models and Rourke's belief in a much
larger black hole than Sagittarius A*.





   
