"""Big Bang or Biggest Blunder?


According to the big bang theory, all matter in the universe was at
essentially the same point in space just 13.7 billion years ago.


This provides a universal clock that all observers can use to agree on
what happened where and when: just measure time since the big bang.


Chapter 2 of the book covers the period of model building, following
Einstein's discovery of general relativity, applying the theory to
the universe as a hole.  And it appears that Einstein favoured a
*cylinder* model that had a universal time.

This is problematic for special relativity, where space and time get
inextricably intertwined and observers in relative motion to each
other do not agree on what happened where and when.

It leads to the assumption that space time is restricted to a subspace
of the full de Sitter Space, that which originated at a single point a
mere 13.7 billion years ago.


The Big Bang theory
===================

Einstein's biggest blunder?  

It is more than a little unreasonable to question the models of the
day given today's observational astrophysics.

I think it is safe to admit that there will, in time be plenty of
worthy winners, but in most cases the blunders will turn out to be
extremely informative, once viewed with a new perspective.

It is the experiments that don't work as expected that tend to have
the biggest effect.  Michelson-Morley is one.

It is the mistakes we make that we do not know we have made that are
most problematic.

For now, this model will just be a collection of visualisations from
the project.

"""

from .spiral import Spiral
from .dss import Dss
from .wits import SolarSystem

from blume import farm, magic

if __name__ == '__main__':

    widgets = [Spiral(), Dss(), SolarSystem()]

    fm = farm.Farm()

    for widget in widgets:
        fm.add(widget)

    fm.shep.path.append(widgets[0])
    farm.run(fm)
    

