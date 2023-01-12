============================
 The State of this Universe
============================

I will try to give updates from time to time as to what is happening
here.

2023/1/9
========

Time for a new year review of how the models presented in `gotu`_ are
faring under the scrutiny of the new space telescope.


Quasars
-------

As time goes on more and more of ARP's peculiar galaxies will be
observed by the JWST.

Many of these contain examples where Arp observed quasars with
intrinsic redshift, caused by the light producing region being close
enough to the central black hole to cause gravitational redshift.

With the new infrared view, we see these galaxies with a new, improved
perspective, providing stronger evidence that they are associated with
the galaxy, yet have significantly larger redshift.


Distant galaxies in deep fields
-------------------------------

Very high red-shift galaxies have been observed by the telescope, in
numbers higher than predicted by the current big bang models.

There is a lot of freedom in the big bang model, but parameters will
need to be tuned.

The observations are entirely consistent with the model proposed in
`gotu`_.

There was no big bang, the universe is essentially static, it is
galaxies as far as we can see.

The universe also happens to be curved, and this does impact the
view.  With expanding and contracting fields intertwined, like an
Escher drawing.

In short, some work to do for the big bang theorists.   Galaxy
formation models need to be refined.

The static universe, with curvature too, is alive and well.


CMB
---

The Cosmic Microwave background has been in the news too.  With the
big bang model, the CMB gives the value of the Hubble constant.

The problem: other methods of calculating the constant give a value
almost 10% higher.

This is the so-called Hubble tension, an indication there's something
amiss.

The `gotu`_ explanation for the CMB is that it is the thermalised
radiation of all the galaxies back-lighting our view of the universe.

It is complicated by the curvature of the universe, that has a
visibility horizon at around the Hubble distance.  On top of that
there are the spherical harmonics that are observed in the CMB to
take account of.


Sgr A*
------

We already have excellent observations of this central black hole.  It
is one of the most observed objects in the Universe.  

According to `gotu`_, it is a baby quasar, in the general direction of
the centre of our galaxy, but not actually at the centre.

I think in time JWST will allow us to see analogues in other
galaxies.  This is key to appreciating the true mass of black holes at
the centre of galaxies the size of the Milky Way.


Gamma-Ray Bursts
----------------

These are assumed to result from cataclysmic events, such as the
collision of neutron stars.

`gotu`_ gamma-ray bursts could herald the arrival of a distant galaxy
in our visible universe.

We see it's infinite past in a very short period of our time, before
the new arrival rapidly recedes according to the Hubble law.

The gravitational wave detectors have been upgraded and are ready for
another obaservational run, starting in March.

We will likely see more gamma-ray bursts with associated gravitational
waves.

If the distant rotating mass of the galaxy bursts on the scene as blue
shifted light, presumably the inertial drag that it exerts on it's
surrounding space time is also modulated in the same way.

It would be good to try and estimate what these waves actually look
like and understand any relation between a gamma-ray burst and a
gravitational wave.


2022/12/9
=========

It has been a fascinating year for this project, with the JWST
constantly in the news.

Since the first pictures in July there has been one beautiful image
after another.

The data is openly available, considered public domain.  The astropy
world has done an excellent job making everything accessible.  It
really is a wonderful time for observations of our universe.

Each JWST image also has background data, not necessarily the focus of
the particular study that proposed the observation.   By making the
data available it increases its value as more theories can be tested
with a single observation.

There is now a `gotu.jwst` module that can be used to download and
view JWST data and images.

You can pass it the name of your favourite target using the --location
option::

  python -m gotu.jwst --location  ngc1566

The module queries the MAST database to convert the name into sky
coordinates and then queries MAST again for JWST observations in that
location.

It then pops up a matplotlib figure window with a table summarising
the records that were found.

Press 'r' and it will start downloading and displaying images.

I have not got past displaying the images with matplotlib, using
random colour maps.  There is always something fascinating in these
images.

Here is a one of NGC 1566, also known as the Spanish Dancer.

.. image:: images/ngc1566.png


Recently, I have been focussing on the `gotu.dss` module, trying to
get a natural understanding of Minkowski and de Sitter space, as this
is the key to the explanation of why an essentially static universe
appears to be expanding.

For a while I have been lost in a world of Lorentz transformations,
hyperbolic rotations and curvature in five dimensions, with parallel
transport of vectors around curves in two dimensional slices.

How to visualise it all?  How to show what a curved universe looks
like?

I feel it is the key to showing that there are other universes than a
big bang universe, that fit the observations, as any argument for a
static universe needs to address red-shift.


  
2021/12/3
=========

It is very much a work in progress, an outline of ideas.

I've tamed the `sphinx`_ enough so that from here most of the
documentation will be in the form of comments in code.

I am still using some things from another of my projects `blume`_
that gives me an interactive framework to work with.  I will likely
have to change a few lines of code as blume settles down.

Here I should be able to move ahead, knowing very little will need
changing here as `blume`_ evolves.   Check the news in blume land for
how that is going.


Plans
-----

There are several pieces that need fleshing out at this point.

* :ref:`dss`, geodesics, gamma-ray-bursts and red-shift.
* :ref:`quasar`, a quasar model.
* :ref:`cmb`, a model with all the harmonics.
* :ref:`spiral`

I also want to rework my code that is downloading Gaia data, to allow
me to zoom in on a particular part of the data.

.. _sphinx: https://sphinx.readthedocs.io

.. _blume:  https://github.com/swfiua/blume
