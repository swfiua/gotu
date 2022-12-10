============================
 The State of this Universe
============================

I will try to give updates from time to time as to what is happening
here.

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

::

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

There are three main pieces that need fleshing out at this point.

* :ref:`dss`, geodesics, gamma-ray-bursts and red-shift.
* :ref:`cmb`, a model with all the harmonics.
* :ref:`spiral`

I also want to rework my code that is downloading Gaia data, to allow
me to zoom in on a particular part of the data.

.. _sphinx: https://sphinx.readthedocs.io

.. _blume:  https://github.com/swfiua/blume
