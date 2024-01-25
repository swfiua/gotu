"""de Sitter Space

It's a ball, expanding and contracting, like an Escher drawing.

Are gamma-ray bursts optical illusions?

Robert S Mackay, Colin Rourke.

https://pjm.ppu.edu/paper/247

The paper describes the relationships between pairs of geodesics in de
Sitter Space.

One geodesic corresponds to the path of a distant galaxy and the other
a receiver geodesic, such as our own galaxy.

Each emitter arrives in our visible universe highly blue shifted, then
becomes increasingly red-shifted as time goes by.

The actual blue shift period and full details depend on two
parameters, phi and theta.

phi corresponds to the minimum distance between the receiver and
emitter, in other words, the emitter's closest point of approach.

theta measures the angle of approach.

de Sitter Space and the Space Telescope
=======================================

Phillip James E. Peebles recently published a fascinating paper:

Anomalies in Physical Cosmology
https://arxiv.org/abs/2208.05018

It describes the standard, lambda-Cold-Dark-Matter model for the
universe and observations that suggest the model may need some new
insight.

The paper is timely, with our new view on the universe thanks to the JWST.

de Sitter Space is mentioned briefly in the paper, remarking that it
was not consistent with the observations.   

I believe Peebles is talking about that sub-space of de Sitter Space,
restricted to bodies with a common origin if you go back the Hubble
time.

de Sitter Space appears to disappear from consideration as a model for
the universe.   

The issue is not de Sitter Space, rather it is the assumption all
matter in the universe was co-located at a big bang some 13.7 billion
years ago.

So what is de Sitter Space?  Imagine a universe, of galaxies, as far
as the eye can see, and far, far beyond.

Moving in seemingly random directions, at around one thousandth the
speed of light.

To transform time at some distant galaxy, to time at our galaxy, we
have to take account of special relativity, the mixing of space and
time.

The result when you measure distance in this way is de Sitter Space.

It is the simplest possible model for a universe where special
relativity holds, and it matches observations extraordinarily well.

It also explains how redshift naturally occurs forwards through time
in space-time as a result of special relativity.

The space is highly symmetric, in time as well as space.

Backwards in time, paths separate exponentially in time too.

Each galaxy that passes through our visible universe, arrives in a
burst of blue shifted light, comes as near as it gets and then
separates exponentially from then, following a hyperbola.

Just as there is a first time that the source is visible, there is a
last time it will be visible, but the observer will have to wait until
the end of time to see that.

So at any time there is a large but finite set of galaxies in the
visible universe.

The modulation of a galaxy's arrival depends on the closest distance
it approaches and the angle of approach.

With this model for a universe there is an explanation for the
redshift that we see, whilst there being no overall expansion of
space-time, as the redshift is exactly balanced by the blue shift
period of a new arrival.

So when we observe through the JWST we may occassionally find
galaxies, new arrivals that are not as redshifedt as they would be
expected to be, given their distance.

There is a further complication, with associating red-shift with
distance.  If the light is coming from a place close to a
super-massive black hole, it may be highly redshifted by the local
gravity, following Einstein's general relativity.

The current assumption is that light producing regions are far enough
from any central mass for the gravitational redshift to be
significant.

Part of this belief comes from the theory of acretion models and
over-coming the angular-momentum obstruction to acretion.

According to Rourke, once you take account of the frame dragging due
to the rotation of the central mass, the angular momentum problem goes
away.

Some of the distant galaxies we are seeing may in fact be smaller
quasars, closer to home.   That's a story for another module.

JWST is also showing us how much dust is scattered across galaxies and,
the beautiful dust spirals that emerge.

The observations we have of our universe, show a place that is very
much in balance, it has had a long time to settle into its current
state.

Once we remove the time limit imposed, due to the big bang it is
possible to imagine very different galactic timescales and evolution.

It also explains the many observations that indicate a system in high
state of equilibrium, for example as shown by the Cosmic Microwave
Background.

Galaxies evolve over time, matter moves out along the spiral arms,
that journey would take of the order of 15 billion years, with many
super-novae along the way.

It should also be noted, that the conditions close to a galaxy's
central black hole are very similar to those shortly after the big
bang, making the journey of matter along spiral arms an even better
match to the big bang theory.   

We see, in the JWST pictures, baby quasars, spinning close to their
parent galaxies.

Galaxies grow from their surrounding dust, and there appears to be
just a steady flow of dust, with wonderful harmonics.  Matter moving
out along spiral arms before falling back into the centre.

But the Cosmic Microwave Background, what's that? It's the heat from
billions of billions of distant galaxies, the glowing dust of the
cosmos.

It's all modulated by the lense of de Sitter Space.

One criticism of de Sitter Space is that it is a vacuum solution to
Einstein's equations.  There is no matter and no Mach's Principle.

Now Rourke's proposal of intertial drag from rotation, dropping off as
1/radius, is also problematic.

The Kerr metric is the unique solution to Einstein's equations assuming
space is not a vacuum.

But space is clearly not a vacuum, it is full of dust and microwaves.
When you apply the Sciama Pricnciple to every celestial body, from the
smallest grain of dust to the largest central mass in a galaxy, then I
believe it will be clear why the Sciama Principle applies.

Now let's see if we can simulate some of this.


Hyperbolas
==========

I have been stuck at this part of the journey for a while, looking for
a good way to explain how space time seems to work.

At this point here, we suddenly run into a lot of mathematics.  

Conic sections, manifolds, matrices, rotations.  Four dimensional
hyperbolic space.

The key observation is that when you plot a distant galaxy's distance
against time we get a rectangular hyperbola.

These hyperbolae arise from the Lorentz transformations of special
relativity.

Most of the sources of light we see are galaxies that are now in the
rapidly receding part of their hyperbola, since that is where each
source spends all but a small finite time of the infinite time it is
visible.

Presumably, under current cosmology, the few exceptions are assumed to
be smaller objects nearer to our galaxy?   

To set the scene, consider someone on a planet in a distant galaxy.

It is possible to estimate the movement, relative to the distant fixed
stars.  For example, our own galaxy is cruising through space at some
2.1 million km/h.  With a little help rom `astropy`:

>>> from astropy import units, constants
>>> milky_way_speed = 2.1e6 * units.kilometer / units.hour
>>> milky_way_speed / constants.c.to(milky_way_speed.unit)
<Quantity 0.00194579>

We see that this is an appreciable fraction of the speed of light.  It
is also in line with the speeds for other galaxies in their locality
in the universe.

More generally, due to the Hubble expansion:

>>> from astropy import cosmology
>>> cosmology.WMAP9.H(0)
<Quantity 69.32 km / (Mpc s)>

So local velocities are large enough that Einstein's special
relativity has to be taken into account when mapping the distant
galaxy's space time to our space time.  [1]

Further, when Hubble expansion is taken into account, these relative
velocities go up by about one thousandth the speed of light every few
mega-parsecs.

But this is just what we would expect when we do an analysis of light
paths taking into account special relativity.

Just as we can naturally divide space time into 3 dimensions of space
and one of time, so can the alien on a distant galaxy.

We both measure the same speed of light locally.  This is an
assumption of special relativity.

However, to map their space time to ours, we need to know our relative velocity.

For distant galaxies, the redshift allows us to calculate a starting
point for this velocity.

Distant galaxies have high red shift, so let's suppose this galaxy is
called Zedten.

Now we want a transformation that preserves distances, and takes
Zedten space time to ours.

What does the path of the Zedten look like through our space-time?

First, let's answer a simpler question.

What does the distance of Zedten look like through our time?  

Reduce the three dimensions of space to one dimension, the distance.

So we need to be able to map a clock and a standard ruler to our clock
and standard ruler.

Light lines give the paths of light through space time.  Both
ourselves and the people of Zed10, the Zeeten, agree that on these
lines, time stands still.

...

References and Footnotes

[1]  The parameter to `WMAP9.H` allows the cosmology to have different
Hubble constants at different redshifts.
>>>>>>> 34b35a1aeac7ade2c0edeaf423f6c29c727dcc67

"""

# we are going to need this
import random
import math
import numpy as np
from astropy import constants, units
from scipy import integrate
from traceback import print_exc

from blume import magic
from blume import magic
from blume import farm as fm

class Dss(magic.Ball):

    def __init__(self):
        """ initialise """
        super().__init__()

        self.theta = math.pi / 4
        self.phi = 0.5
        self.size = 50
        self.aaa = magic.modes

        self.set_abcd()

    def set_abcd(self):

        self.alpha, self.beta, self.gamma, self.delta = (
            math.cosh(self.phi), 0., 0., math.cos(self.theta))
        self.a = (self.alpha + self.beta - self.gamma - self.delta) / 2
        self.b = (self.alpha - self.beta - self.gamma + self.delta) / 2
        self.c = (self.alpha + self.beta + self.gamma + self.delta) / 2
        self.d = (self.alpha - self.beta + self.gamma - self.delta) / 2
        

    def constraints(self):

        print(self.alpha**2 - self.gamma**2 >= 1.)

        print(self.alpha > 0)

        a, b, c, d = self.alpha, self.beta, self.gamma, self.delta

        print((a * b - c * d)**2 <= (a*a - c*c - 1) * (b*b - d*d +1))
        print((b*b - d*d +1) >= 0)

    def blue_shift_time(self, alpha=None, delta=None):
        """ """
        a = alpha or self.alpha
        d = delta or self.delta

        sqrt = math.sqrt
        etb = sqrt((1+a)/(a+d)) + sqrt((1-d)/(a-d))
        
        return math.log(etb)

    def tofu(self, u):
        """ -a sinh(t) sinh(u) + d cosh(t) cosh(u) = 1

        work with U=e**u and T=e**t
        """
        U = math.e ** u

        a, b, c, d = self.a, self.b, self.c, self.d

        xx = (b * d) + ((U**2) * (1 - b*c - a*d)) + (a * c * U**4)
        T = (U + math.sqrt(xx)) / (b - a * U**2)

        # check equation
        print(U,T)
        check2 =  (-a*T*U) + (b*T/U) + (c*U/T) - (d/T*U)
        print('check should be 2:', check2)

        t = math.log(T)
        u = math.log(U)
        sh = math.sinh
        ch = math.cosh

        a, b, c, d = self.alpha, self.beta, self.gamma, self.delta
        check = - a * sh(t) * sh(u) + d * ch(t) * ch(u)
        print('check should be 1:', check)
        
        return t

    def time_until_red_shift_matches_expected_for_distance(self, error=0):
        """ Curious how this value varies with phi and theta """
        raise NotImplemented        

    def time_until_red_shift_turns_light_into_microwaves(self, error=0):
        """ Curious how this value varies with phi and theta """
        raise NotImplemented        


    def deSitter(self):

        pass

    def cmb(self):
        """Show why there is gravitational fog.
        

        What would the distant light from a universe a few orders of
        magnitude larger and older than the Hubble distance look like?

        Curvature means that light that appears to come from a
        specific, very distant point, is actually a mixture of light
        from all points on the sphere at that radius.

        At least that's how I think de Sitter Space works.

        The goal here is to explore what we might expect to see.

        Bonus marks for a model which produces the spherical harmonics
        observed in the cmb.

        Perhaps restrict to a circle of radius phi and use 0 theta for the
        angle around the circle.

        """
        raise NotImplemented

    async def run(self):

        size = self.size
        epsilon = 1e-3

        img = np.zeros((size, size))

        for row in range(1, size+1):

            delta = math.cos(math.pi * row/(size+1))
            for col in range(1, size+1):
                alpha = math.cosh(self.phi * col/(size+1))

                try:
                    img[row-1][col-1] = self.blue_shift_time(
                        alpha or epsilon, delta or epsilon)
                except:
                    print_exc()
                    print(alpha, delta)
                    raise
 
            #print(img[row-1])

            await magic.sleep(0)

        ax = await self.get()

        extent = [0, math.pi, 0, self.phi]
        aximg = ax.imshow(
            img,
            cmap=magic.random_colour(),
            extent=extent,
        )

        #ax.figure._axstack.bubble(ax.delegate)
        #ax.figure.colorbar(aximg)
        #ax.axis('off')
        ax.show()


class DeSitterSpace(magic.Ball):
    """Another go at de Sitter Space.

    Suppose that the universe is just an endless stream of galaxies,
    like the billions

    The idea is to consider a distant galaxy, as it arrives in our
    visible universe
    
    
    """
    def __init__(self):


        super().__init__()

        self.k = 1.
        
        self.x = 0.
        self.dt = 0.01
        self.t = 0.

        self.v = 1 / random.randint(5, 10)


    async def uvxt(self):
        """ """

    async def zedten(self, z=10, theta=0, nearest=1):
        """a galaxy at zed ten
        
        z: redshift, optional, default 10
        theta: angle of approach
        nearest: point of closest approach

        plots future and past of a galaxy at zed10

        if nearest is zero, then it is a big bang universe.

        but what if nearest is one or more? Where one is the Hubble distance.

        The answer is a hyperbolic rotation, but how to get there?

        Focus on the intersection of our timeline with the future
        light cone of `Zed10`.

        The plots below are an attempt to follow the arguments on page
        163 of `gotu`.

        
        """
        ax = await self.get()

        ax.set_ylabel('x')
        ax.set_xlabel('t')

        # light lines in our co-ordinates 
        for c in range(10):
            t = np.arange(-5, 5)
                        
            # x = t + c, positive distance
            ax.plot(t + c, t, c='blue') 

            # negative distance x = -t + c
            ax.plot(-t + c, t, c='b') 

        #ax.show()

        
        #ax = await self.get()
        # now think about transformations that preserve `distance`

        # distance_squared = (x1-x2)**2 - (t1-t2)**2
        # on light lines, dx = dt

        # u * v = k, u = x - t, v = x + t
        k = self.k

        for ix in range(20):
            
            x = np.arange(k**-2, 10, 0.1)

            # x**2 - t**2 = k
            #t**2 = x**2 - k

            t = ((x**2) - k)**0.5

            ax.plot(x, t)
            ax.plot(x, -t)

            k *= 1.5

        k = self.k * 2

        for trial in range(5):
            u = random.random() + random.randint(1, 5)
            v = random.random() + random.randint(1,5)
        
            print([(u+v)/2, (u/k + k*v)/2])
            print([(v-u)/2, ((v * k) - u/k)/2])
            ax.plot((u+v)/2, (v-u)/2, 'ro')
            ax.plot((u/k + k*v)/2, ((v * k) - u/k)/2, 'bo')

        ax.show()
        
    async def run(self):
        """ """

        
        await self.zedten()
        return

    async def lorentz(self):
        """ FIXME """
        
        # increment t
        self.x += self.v * self.dt
        self.t += self.dt

        # we see
        gamma = 1/math.sqrt(1 - (self.v * self.v))
        dr = gamma * self.v * self.dt  # ???
        dt = self.dt / gamma

        v = dr/dt

        print(v, self.v)
        self.v = v

async def run():

    dss = Dss()

    dss.set_abcd()
    dss.constraints()

    farm = fm.Farm()

    dss2 = DeSitterSpace()
    farm.add(dss2)
    farm.add(dss)
    
    await farm.start()

    await farm.run()
        

if __name__ == '__main__':

    # theta distributed as cos(theta) * delta_theta
    theta = math.cos(random.random() * math.pi) * math.pi
    # phi distributed as sinh ** 2 * delta_phi
    phi = None

    thetas = np.array([math.cos(theta * math.pi * xx) for xx in range(1, 1000)])

    shines = np.array([math.sinh(x/100) ** 2 for x in range(1,1000)])

    weights = integrate.cumulative_trapezoid(shines, initial=0)
    #plt(weights)
    #plt.show()
    #0/1

    wm = False
    magic.run(run())
