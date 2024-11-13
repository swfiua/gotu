==============================================
 Introduction to The Geometry of the Universe
==============================================

The workshop will feature modules from my gotu project, exploring the
geometry of the universe.

It will cover downloading and visualising data from the James Webb
Space Telescope and the Gaia mission to visualise the rotation curve
for the Milky Way.

Simulate the Milky Way's rotation curve assuming the Sciama Principle::

   a rotating mass induces a rotation on the surrounding space time
   with a magnitude proportional to the mass and inversely
   proportional to the 

           
Compare to the Gaia image.


Introduction to de Sitter Space.  This will use matplotlib to
visualise geodesics in de Sitter Space, allowing us to explore the
subtle relation between redshift and distance.

Downloading and visualising the supernovae data and testing whether it
is consistent with de Sitter Space.

Since gotu uses blume, the workshop will begin with an introduction to blume.

The goal is for attendees to have at least half the workshop time to
explore the ideas and data sets for themselves.

Introduction
============

Johnny Gill
-----------

Goals
-----

blume

gotu

Help me and others understand the ideas in the book.

Visualise space-time, understand curvature.

Visualise data to see if it supports the theory.

Gain insight into cosmological mysteries
----------------------------------------

Hubble Tension

Dark Matter

Dark Energy

Gravitational Waves

Dark Energy


Flash Warnings
--------------

Lots of axes flying around.

Install the software
====================

Create Virtual Environment
--------------------------

mkdir workshop

python3 -m venv gotuenv

Install blume
-------------

git clone https://github.com/swfiua/blume

cd blume

python3 -m pip install -e .

Install gotu
------------

git clone https://github.com/swfiua/gotu

cd gotu

python3 -m pip install -e .


Blume
=====

Is there anything better than an editor, a console and a bunch of 100
line python scripts?

Principles
----------

No module should exceed 1000 lines

Fix it upstream

Is there anything better than a folder full of 100 line python
scripts?

There is nothing a layer of abstraction cannot fix.  Can it be done
without adding complexity?

It is impossible to do anything if I obey all the principles?


Patterns
========

print to debug

add complexity while figuring out how things work.

no problem a layer of indirection cannot solve

Blume Magic Module
==================

blume.magic.RoundAbout

blume.magic.Carpet

blume.TableCounts

Gotu Modules
============

gotu.jwst
---------

astroquery and mast
+++++++++++++++++++

gotu.wits
---------

gotu.spiral
-----------

gotu.gaia
---------

Observations
============

Hubble Space Telescope

Event Horizon Telescope(s)

Planck Mission

LIGO

Pulsar Timing Array

JWST
====

Gaia
====


The Milky Way Rotation Curve
============================

astropy
-------

Spiral Galaxies
---------------

Dark Energy Survey
==================

de Sitter Space
===============

Simulation of geodesics in de Sitter Space
------------------------------------------

A Glimpse of Hubble Tension?
----------------------------

Closer to home
--------------

The Laniakea supercluster of galaxies
=====================================

Priors
------

The Wiener Filter
-----------------

Combining Sciama and de Sitter
==============================


Build your own blume.train
==========================

Never have to write code to view data again.

Find away to work with the magic carpet, feed it tables of meta data,
attach it to axes and then put them into queues based on the meta
data, which must be hashable.

meta data
---------

And the matplotlib.subplot_mosaic
