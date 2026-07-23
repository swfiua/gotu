"""I am exploring the python project bilby.

This is Bilbo Bilby, boldly going where no astrophysicist has gone before.

`bilby`_ takes priors and waveforms and calculates odds.

It is a general Bayesian inference library primarily designed for
inference of compact binary coalescence events in interferometric
data.  This `bilby paper`_ is an excellent guide.

Armed with Bilby it is just necessary to specify prior distributions
for parameters and a function that takes those parameters and creates
the waveform given the parameters.

Bilby also allows for a parameter conversion function to be applied to
the sample before calling the waveform generator.

.. _bilby paper: https://arxiv.org/pdf/1811.02042
.. _bilby: https://pypi.org/project/bilby/


2026/07/03
==========

The inspiral phase is still causing some headaches.  This caused me to
explore the calculations for the merging black hole waveforms.

This leads to the world of post-Newtonian gravity and approximations to General Relativity.

In the arriving galaxy model there are some adjustments we need to
make, compared to merging black holes:

* the arrivals are all at the Hubble distance, they are just entering our visible universe.

* they arrive at extreme blueshift, rather than the redshift of the distant black hole mergers.

* no black holes are merging, rather the wavefront arrives like a tsunami

The wavefront has the essential 1/r**3 shape of the Kerr metric, but
this is distorted due to the curvature of space time.

The switch from redshift to blueshift means that a. the masses have to
be proportionately larger to create a wave of the same frequency.
After taking acount in the change from redshift to blueshift and the
change in distance, we get a signal many orders of magnitude larger.

This is what we would get if two black holes just happened to merge as
they entered our visible universe, but that is not what is happening.

Remember, black holes do not merge in this story.

We can however compare the Kerr wave that the black holes in the
merger would make, to the wave detected.  This will give a scale
factor to apply to convert from one to the other.


2026/03/27
==========

I am now at the point where I just have to generate waveforms given priors.

It may just be my choice of units that is causing me trouble.

We are interested in the first few seconds of a new arrival.

It turns out that the distribution of events that occur is strongly
biased to ones whose blue-shift time is short compared to the Hubble time.

The larger phi, the shorter the blue shift time.  So is there any
limit to how large phi can be?

Rourke argued that the low level wobbles of spacetime mean no light
can travel more than a certain distance, a handful of Hubbble times,
before being thoroughly diverted from it's original direction.

A second 2e-18 times the Hubble time, which is 1 in my units.

At the same time, when an object initially appears it is infitely blue shifted.

Actual gamma-ray bursts are powerful, but not infinite.  The burst associated with
GW20170817 is a good example.

There were observations in ultra-violet (15 hours), x-ray (9 days rising to a peak at 150 days)

In short, there is sufficient data to fit a phi/theta model that gives the blueshift over time of
a new arrival.

It is also necessary to take into account that galaxy's are energetic
in different frequency bands, for instance, glowing in the infrared,
which might appear as ultra-violet, soon after the arrival.

150 days is around 1e-11 Hubble times.

One observation is that we do not see very short gamma-ray bursts.
These would be associated with very large phi, huge hyperbolic
rotations.  The same wobbles in space time may limit the size of
rotation that is possible.

For the inspiral, it is necessary to take account of how theta and phi
affect distances from the source.

Now suppose we detect the front of the Kerr wave-front at t*.  A short
time, dt, afterwards, the source will have moved a distance x'.

In the inspiral we are only interested within some multiple of the
Schwartzchild radius of the source, and this will be small compared to
the size of the universe.  To a first approximation all objects near
the source will have moved x' closer.

Turning this around, a time dt before the event peak we will see the
Kerr wave at distance x' from the source.

The second problem to deal with is figure out the amplitude of wave we
should expect.

There is a limit to how far a wave can travel before being thouroughly
diverted from its original direction.  This limit is why the cosmic
microwave background is not brighter.

The CMB is around 45 times brighter than you would expect from all the
energy from galaxies within the visible universe.  Rourke suggests
this indicates light cannot travel more than a handful of Hubble
distance before being diverted from its original direction.

This will place a cap on the actual energy received.

2026/08/04
==========

A story with no beginning.
A time and a place when everything started?

Currently going round in circles working on the waveforms for incoming objects.

Whilst plotting potential ringdown plots I noticed a peculiar
discontinuity in the curves, which has lead me back to the
Spiral.uoft() method and a closer look at the formulae I am using for
uoft().

I recall that originally I thought there may be no such formula, and
the code used a solver instead.  I thought I tested the new version
against the solver, but I need to re-check.

2026/06/05
==========

Lots of thrashing around with the ringdown and inspirals.

I am now happy with the ringdown and back to thinking about inspirals.

I have added a *maxage* to the prior to model Rourke's idea that the
intensity of arrivals is reduced because light (and gravitational waves).

This in effect gives a maximum blue-shift for the new arrival.

Now, for the inspiral the whole wavefront arrives with this blue-shift.

I had been thinking that the theta and phi are what give rise to the
interesting modulations in the inspiral, it is not just a simple
1/r**3 curve.

The wavefront is the sum of contributions from all masses in the
system.

A solution is to add a second mass to the model and then the curve
is the combination of the two.

Presumably the ratios of the masses that produce the best match will
be the same as the ratio of masses of two merged black holes that
provide the best match in the merging black hole theory.

If this is the case it will speed up my model fitting!

Theta and phi may not be needed as Rourke notes that for a short time
after arrival t-t* = 1+z.

Now to fix up the code.

"""
import sys
from math import *
from blume import magic, farm
np = magic.np

from gotu.spiral import RandomPhi, Spiral

import bilby
from bilby.core.prior import Prior, WeightedDiscreteValues, Sine, Cosine, Uniform, Normal, Exponential
from gwpy.timeseries import TimeSeries

from astropy import units as u, constants as c
from mpmath import mp, mpf
mp.dps = 70

import argparse

def get_args(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir')
    parser.add_argument('--label', default='GW150914')
    parser.add_argument('--trigger_time', type=float, default=1126259462.4)
    parser.add_argument('--post_trigger_duration', type=float, default=2.)
    parser.add_argument('--duration', type=float, default=4.)
    parser.add_argument('--detectors', nargs='+', default=["H1", "L1"])
    parser.add_argument('--chirp', action='store_true', default=False)

    return parser.parse_args(args)

def find_r(galaxy, tdash, utest=-5., factor=1000):
    """

    tdash is tstar for a point r nearer than galaxy
    what is r at tdash?

    This is tricky, because u is infinite at tstar and near to tstar this
    leads to overflow problems.

    The larger phi, the smaller the blue shift period.

    At large phi, we run into overflow problems.

    r is also small compared to the size of the visible universe.

    This creates computational problems in studying the region of interest.

    We are interested in a short period of time, before and after tstar.

    Before tstar, we are seeing the building Kerr wave-front.

    We are interested in the first time a point a distance r from the centre
    becomes visible to us.

    We know this happens for some time tdash and a time udash in the emitter time.

    (-a * sinh(udash) * sinh(tdash)) + (d * (cosh(udash) - r) * cosh(tdash) = 1.

    
    """
    a = cosh(galaxy.phi)
    d = cos(galaxy.theta)

    umax = utest

    def f(r):
        value = (-a * sinh(umax) * sinh(tdash)) + (d * (cosh(umax) - r) * cosh(tdash) - 1.0)

        return value

    r = (factor * galaxy.schwartzchild() << u.lightyear).value

    while True:

        value = f(r)

        if value > 1.:
            r /= 2.
        if value < 0.:
            r *= 1.5
        print(r, f(r))
        if r > 1e50: break
        if r == 0.0: break


def doplot(xx, yy, title):

    magic.runner(adoplot(xx, yy, title))
                 

async def adoplot(xx, yy, title):

    ax = await magic.TheMagicRoundAbout.get()

    if ax is not None:
        
        ax.plot(xx, yy)
        ax.set_title(title)
        ax.show()

    await magic.asyncio.sleep(1)
    
def find_t_forz(galaxy, hubble_time, z, epsilon=1e-6):

    tstar = galaxy.tstar()
    tmin = tstar
    tb = galaxy.tb()
    tmax = tb + tmin

    while True:
        t = (tmax+tmin)/2
        zoft, xx = galaxy.zandx(t)
        #print(t-tstar, zoft)
        if abs(zoft-z) < epsilon:
            break
        #print(tb, tmax, tmin, zoft, z)
        if zoft > z:
            if tmax == t:
                print('tforz is tmax')
                break
            tmax = t
        else:
            if tmin == t:
                print('tforz is tmin')
                break
            tmin = t

        if tmax == tmin: break

    return t

async def tfortb_show(mintheta=0.001, maxtheta=.8, minphi=.5, maxphi=5., tb_factor=0.001,
                      minz=-0.999):

    width = height = 128
    tc = magic.TableCounts(title=f'z for tb * {tb_factor}',
        minx=mintheta, maxx=maxtheta, miny=minphi, maxy=maxphi,
        width=width, height=height, xname='theta', yname='phi',
        colorbar=True)
    
    tbtab = magic.TableCounts(title=f'blueshift time',
        minx=mintheta, maxx=maxtheta, miny=minphi, maxy=maxphi,
        width=width, height=height, xname='theta', yname='phi',
        colorbar=True)

    tabminz = magic.TableCounts(title=f't for {minz}',
        minx=mintheta, maxx=maxtheta, miny=minphi, maxy=maxphi,
        width=width, height=height, xname='theta', yname='phi',
        colorbar=True)

    thetas = np.linspace(mintheta, maxtheta, width)
    phis = np.linspace(minphi, maxphi, height)

    galaxy = Spiral()
    hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value

    for theta in thetas:
        for phi in phis:
            galaxy.theta = theta
            galaxy.phi = phi
            tb = galaxy.tb()
            z, x = galaxy.zandx(galaxy.tstar() + galaxy.tb() * tb_factor)
            tc.update([theta], [phi], 1/(1+z))
            tbtab.update([theta], [phi], tb)

            tminz = find_t_forz(galaxy, minz, hubble_time)
            tabminz.update([theta], [phi], tminz)

    await tc.show()
    await tbtab.show()
    await tabminz.show()

async def pow_show(theta=0.1, phi=5., powers=[0.5], tbfactor=1, samples=1000):

    ax = await magic.TheMagicRoundAbout.get()
    xax = await magic.TheMagicRoundAbout.get()
    lax = await magic.TheMagicRoundAbout.get()
    uax = await magic.TheMagicRoundAbout.get()
    for power in powers:
        atheta = acos(cos(theta)**power)
        aphi = acosh(cosh(phi)**power)
        print('theta/phi/atheta/aphi/power', theta, phi, atheta, aphi, power)
        galaxy = Spiral()
        hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value

        galaxy.theta = atheta
        galaxy.phi = aphi
        tb = galaxy.tb()
        tstar = galaxy.tstar()
        ttt = np.linspace(0., tb/tbfactor, samples+1)[1:]

        uuu = np.array([galaxy.uoft(tt+tstar) for tt in ttt])
        zzz = np.array([galaxy.zandx(tt+tstar)[0] for tt in ttt])
        xxx = np.array([galaxy.zandx(tt+tstar)[1] for tt in ttt])
        zdash = []
        for zz in zzz:
            if zz < 0:
                zz = 1/(1+zz)

            zdash.append(zz)
            
        lum = []
        for ix, zz in enumerate(zzz):
            xx = xxx[ix]
            lum.append(1/(xx*xx*(1+zz)*(1+zz)))

        ax.plot(ttt, np.clip(zdash, 0, 1000), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:6g}')
        xax.plot(ttt, np.clip(xxx, 0, 2.), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.6g}')
        lax.plot(ttt, np.clip([mp.log10(lll) for lll in lum], 0, 15), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.6g}')
        llum = np.array([log10(lll) for lll in lum]).clip(0, 15)
        dllum = llum[1:] - llum[0:-1]
        uax.plot(ttt[1:], np.clip(dllum, -1000, 1000), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.6g}')

        
    xax.set_title('Distance v time')
    ax.set_title('zdash v time')
    lax.set_title('luminosity v time')
    uax.set_title('dlum v t')

    ax.legend()
    xax.legend()
    lax.legend()
    uax.legend()
    ax.show()
    xax.show()
    lax.show()
    uax.show()
    


class Sinh2(WeightedDiscreteValues):

    def __init__(self, name=None, maximum=None, minimum=None, n=10000):

        random_phi = RandomPhi(max_phi=maximum, min_phi=maximum, n=n)

        super().__init__(random_phi.values[1:], random_phi.counts, name=name)


def identity(arg):
    print(arg)
    return arg, None

class Bilbo(magic.Ball):

    def __init__(self, args):

        self.args = args

        self.showtable = False
        self.galaxy = Spiral()
        
        super().__init__()
    
        
    def load_ifos(self):
        """ Load the list of observations """
        logger = bilby.core.utils.logger
        args = self.args

        label = args.label
        outdir = args.outdir or label
        
        trigger_time = args.trigger_time or datasets.gps_time(label)

        # Note you can get trigger times using the gwosc package, e.g.:
        # > from gwosc import datasets
        # > datasets.event_gps("GW150914")
        detectors = args.detectors
        maximum_frequency = 512
        minimum_frequency = 20
        roll_off = 0.4  # Roll off duration of tukey window in seconds, default is 0.4s
        duration = args.duration  # Analysis segment duration
        post_trigger_duration = args.post_trigger_duration  # Time between trigger time and end of segment
        end_time = trigger_time + post_trigger_duration
        start_time = end_time - duration

        psd_duration = 32 * duration
        psd_start_time = start_time - psd_duration
        psd_end_time = start_time

        # We now use gwpy to obtain analysis and psd data and create the ifo_list
        ifo_list = bilby.gw.detector.InterferometerList([])
        form = '.hdf5'
        for det in detectors:
            ifo = bilby.gw.detector.get_empty_interferometer(det)

            filename = magic.Path(outdir, det + label + form)
            if filename.exists():
                logger.info("Reading cached analysis data for ifo {}".format(det))
                data = TimeSeries.read(filename)
            else:
                logger.info("Downloading analysis data for ifo {}".format(det))
                data = TimeSeries.fetch_open_data(det, start_time, end_time)
                data.write(filename)
            ifo.strain_data.set_from_gwpy_timeseries(data)

            filename = magic.Path(outdir, det + label + 'psd' + form)
            if filename.exists():
                logger.info("Reading cached psd data for ifo {}".format(det))
                psd_data = TimeSeries.read(filename)
            else:
                logger.info("Downloading psd data for ifo {}".format(det))
                psd_data = TimeSeries.fetch_open_data(det, psd_start_time, psd_end_time)
                psd_data.write(filename)

            psd_alpha = 2 * roll_off / duration
            psd = psd_data.psd(
                fftlength=duration, overlap=0, window=("tukey", psd_alpha), method="median"
            )
            ifo.power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
                frequency_array=psd.frequencies.value, psd_array=psd.value
            )
            ifo.maximum_frequency = maximum_frequency
            ifo.minimum_frequency = minimum_frequency
            ifo_list.append(ifo)

        logger.info("Saving data plots to {}".format(outdir))
        bilby.core.utils.check_directory_exists_and_if_not_mkdir(outdir)
        ifo_list.plot_data(outdir=outdir, label=label)

        return ifo_list

    async def start(self):

        label = args.label
        outdir = args.outdir or label

        self.ifo_list = self.load_ifos()
        if not hasattr(self, 'priors'):
            self.priors = self.load_priors()

        # In this step we define a `waveform_generator`. This is the object which
        # creates the frequency-domain strain. In this instance, we are using the
        # the Spiral source model. We also pass other parameters:
        # the waveform approximant and reference frequency and a parameter conversion
        # which allows us to sample in chirp mass and ratio rather than component mass
        self.waveform_generator = bilby.gw.WaveformGenerator(
            time_domain_source_model=self.tdsm,
            parameter_conversion=self.conversion,
        )

    def pre_run(self):

        # In this step, we define the likelihood. Here we use the standard likelihood
        # function, passing it the data and the waveform generator.
        # Note, phase_marginalization is formally invalid with a precessing waveform such as IMRPhenomPv2
        self.likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
            self.ifo_list,
            self.waveform_generator,
            priors=self.priors,
            time_marginalization=False,
            phase_marginalization=False,
            distance_marginalization=False,
        )

        from bilby.core.sampler import dynesty

        label = args.label
        outdir = args.outdir or label

        meta_data = dict()
        self.likelihood.label = label
        self.likelihood.outdir = outdir

        bcu = bilby.core.utils
        meta_data["likelihood"] = self.likelihood.meta_data
        meta_data["loaded_modules"] = bcu.loaded_modules_dict()
        meta_data["environment_packages"] = bcu.env_package_list(as_dataframe=True)
        meta_data["global_meta_data"] = bcu.global_meta_data

        self.sampler = dynesty.Dynesty(
            self.likelihood,
            priors=self.priors,
            outdir=outdir,
            label=label,
            plot=False,
            npool=1,
            meta_data=meta_data,
        )
        
    def load_priors(self):
        
        # We now define the prior.
        # We have defined our prior distribution in a local file, GW150914.prior
        # The prior is printed to the terminal at run-time.
        # You can overwrite this using the syntax below in the file,
        # or choose a fixed value by just providing a float value as the prior.
        label = args.label
        trigger_time = args.trigger_time or datasets.gps_time(label)
        filename = magic.Path(label + ".prior")
        if filename.exists():
            priors = bilby.core.prior.PriorDict(filename=filename.name)
        else:
            priors = bilby.core.prior.PriorDict(dict(
                m1 = Uniform(name='m1', minimum=5, maximum=12),
                m2 = Uniform(name='m2', minimum=5, maximum=12),
                phi = Sinh2(name='phi', maximum=55., minimum=54.9999, n=1000),
                theta =  Sine(name='theta'),
                #theta =  0.001,
                dec =  Cosine(name='dec'),
                ra =  Uniform(name='ra', minimum=0, maximum=2 * np.pi, boundary='periodic'),
                psi =  Uniform(name='psi', minimum=0, maximum=np.pi, boundary='periodic'),
                phase =  Uniform(name='phase', minimum=0, maximum=2 * np.pi, boundary='periodic'),
                #logzboost =  Uniform(name='logzboost', minimum=0, maximum=17, boundary='periodic'),
                logzboost = 0,
                logscale = 0.,
                minz = Uniform(name='minz', minimum=-10, maximum=-4, boundary='periodic'),
            ))

        # Add post trigger duration.  geocent_time + post_trigger_duration is end of inspiral
        priors["post_trigger_duration"] = bilby.core.prior.DeltaFunction(
                peak=args.post_trigger_duration, name="post_trigger_duration",
            )

        # Add the geocent time prior if it is not already there
        if "geocent_time" not in priors:
            priors["geocent_time"] = bilby.core.prior.Uniform(
                trigger_time - 0.1, trigger_time + 0.1, name="geocent_time",
                boundary='periodic'
            )

        for key, value in priors.items():
            print(key, value.is_fixed)

        return priors

    def conversion(self, priors):

        result = priors.copy()

        result['minz'] = -1 + 10**priors['minz']
        result['m1'] = 10**priors['m1']
        result['m2'] = 10**priors['m2']

        
        m2 = np.where(result['m1'] < result['m2'], result['m2'], result['m1'])
        m1 = np.where(result['m1'] < result['m2'], result['m1'], result['m2'])
        result['m1'], result['m2'] = m1, m2

        if self.args.chirp:
            m1 = result['m1']
            m2 = result['m2']

            chirp = (m1*m2)**0.6/((m1+m2)**.2)

            result['m1'] = chirp
            result['m2'] = chirp * 0
        
        
        return result, None
    

    def tstar1000(self, galaxy, zz=-0.999):

        tstar = galaxy.tstar()

        tb = galaxy.tb()

        tguess = tb/2
        offset = tguess/2

        z, x = galaxy.zandx(tstar+tguess)

        zz = mpf(zz)
        count = 0
        while z != zz:
            #print(z, x, tb, tguess, offset)
            if z < zz:
                tguess += offset
            else:
                tguess -= offset
            offset /= 2
            z, x = galaxy.zandx(tstar+tguess)
            if offset == 0: break
            if count > 100: break
            count += 1

        return tstar + tguess

    def tdsm(self,
            gtimes,
            geocent_time=None,
            m1=None,
            m2=None,
            theta=None,
            phi=None,
            dec=None,
            ra=None,
            psi=None,
            phase=None,
            logzboost=None,
            logscale=None,
            minz=None,
            post_trigger_duration=None):
        """Waveform generator

        Events are known to be strongly biassed to short blueshift
        period, but these have very large phi.

        We are also interested in just the a few seconds of time, when
        the radius of curvature is of the order 1e18 seconds.

        The problem here is that the events we are seeing are
        for large (10-100) phi and there are numerical precision errors.

        This affects the calculation of z and x for the ringdown.

        hifi_zandx tries to get around this
        """

        galaxy = self.galaxy
        galaxy.set_mcent((m1 * 3.0 * u.km << u.lyr).value)
        galaxy.phi = phi
        galaxy.theta = theta
        scr = (galaxy.schwartzchild() << u.lightsecond).value 
        hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value
        zboost = 10**logzboost
        #tstar = galaxy.tstar()

        # use time for z = -0.999 as start of event
        tstar = self.tstar1000(galaxy, minz)

        # calculate some values based on theta/phi
        ttt = (gtimes - gtimes[0]) * zboost / hubble_time

        uuu = [galaxy.uoft(tstar + t) for t in ttt]
        zandx = [galaxy.zandx(tstar+t, u) for t, u  in zip(ttt, uuu)]

        zzz = np.array([float(zx[0]) for zx in zandx])
        zz1 = np.array([float(1+zx[0]) for zx in zandx])
        xxx = np.array([float(zx[1]) for zx in zandx])

        ringdown = 1. / (zz1.clip(1+minz)*xxx*hubble_time)**2

        strain = np.zeros((len(ttt)))


        kerrs = []
        tins = ttt[gtimes < geocent_time] * hubble_time / cos(theta)

        # distance from event horizon in seconds

        uuu0 = np.array([float(uu - uuu[0]) for uu in uuu])
        
        tins = tins[::-1]
        delta_t = tins[1] - tins[0]
        epsilon = 1e9
        for mass in m1, m2:
            if not mass: continue
            radius = mass * scr/m1

            # gravitational length contraction near black hole this
            # increases the frequency as tge event horizon approaches
            # enhancing the effect of blueshift.
            
            # kerr depends on distance from the black hole centre
            distance = tins + radius
            kerr = (radius**4)/(distance**3.)
            kerrs.append([kerr, radius])

        for ix, tt in enumerate(tins):

            if ix:
                ss = strain[ix:]
                rd = ringdown[:-ix]
                uu = uuu0[:-ix]
            else:
                ss, rd, uu = strain, ringdown, uuu0

            for kerr, radius in kerrs:
                weight = kerr[ix]

                lc = np.sqrt(1-radius/(tt+radius+epsilon)) * (1+minz)

                wavelength = radius * lc
            
                ss += ((weight * rd * np.sin((2*pi*uu*hubble_time/wavelength) + phase)) * c.c).value

            phase += delta_t / wavelength
            #print(kk.shape, uu.shape, ix)

        kerr = np.concat((kerrs[0][0], np.zeros(len(gtimes)-len(kerr))))
        #return dict(strain=strain, ringdown=ringdown, kerr=kerr,
        #            uuu=uuu, zzz=zzz, xxx=xxx)
        return dict(strain=strain)


    def hifi_zandx(self, ttt):
        """ Approximate zandx for large phi

        Take square root and look at ratio of tb
        """
        galaxy = self.galaxy
        phi = galaxy.phi
        theta = galaxy.theta
        tb = galaxy.tb()

        galaxy.phi = sqrt(phi)
        galaxy.theta = sqrt(theta)

        tb2 = galaxy.tb()

        print(tb2, tb, tb/tb2)

        # put original values back
        galaxy.phi = phi
        galaxy.theta = theta

    async def run(self):

        self.pre_run()
        
        logger = bilby.core.utils.logger
        args = self.args

        priors = self.priors
        for key in priors:
            if isinstance(priors[key], Prior):
                print(key, priors[key].is_fixed)

        print(priors.sample_subset(priors.keys(), size=1))
        #import pdb
        #pdb.set_trace()
        

        # Finally, we run the sampler. This function takes the likelihood and prior
        # along with some options for how to do the sampling and how to save the data
        result = self.sampler.run_sampler()

        result.plot_corner()

    async def show_waveforms(self):

        gtimes = np.linspace(self.args.trigger_time-self.args.post_trigger_duration,
                             self.args.trigger_time+self.args.post_trigger_duration,
                             10000)
        while True:

            sample = self.sample = self.sample_prior()

            sample = self.conversion(sample)[0]

            parms = {k: v[0] for k,v in sample.items()}

            waveform = self.waveform = self.tdsm(gtimes, **parms)

            for key in waveform.keys():
                ax = await self.get()

                ax.plot(gtimes, waveform[key])
                ax.set_title(key)
                ax.show()

            if self.showtable:
                self.put_nowait(sorted(sample.items()), 'help')
            await magic.sleep(self.sleep)

    def sample_prior(self):
        
        return self.priors.sample_subset(self.priors.keys(), size=1)
        
    async def oddity(self):

        theta = pi / 120
        phi = 12.
        
        t0 = 2e-5
        tmax = 3e-5

        sp = Spiral()
        sp.theta = theta
        sp.phi = phi

        a = cosh(phi)
        d = cos(theta)
        A = D = (a-d)/2
        B = C = (a+d)/2

        tt = np.linspace(t0, tmax, 1000)
        tstar = sp.tstar()
        T = np.exp(tt+tstar)
        square = C*D + ((1 - B*C - A*D) * T*T) + A * B * T*T*T*T
        num = T - [sqrt(x) for x in square]
        den = C - A * T*T
        U = num/den

        print('tstar, sqrt(C/A)', tstar, sqrt(C/A))

        await adoplot(tt, [sp.uoft(t+tstar) for t in tt], 't v u')
        await adoplot(tt, square, 't v square')
        await adoplot(tt, num, 't v num')
        await adoplot(tt, den, 't v den')
        await adoplot(tt, U, 't v U')




if __name__ == '__main__':

    args = get_args()

    baggins = Bilbo(args)

    land = farm.Farm()
    land.add(baggins)
    farm.run(land)
