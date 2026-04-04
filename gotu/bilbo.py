"""I am exploring the python project bilby.

This is Bilbo Bilby, boldly going where no astrophysicist has gone before.

bilby takes priors and waveforms and calculates odds.

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

"""
import sys
from math import *
from blume import magic, farm
np = magic.np

from gotu.spiral import RandomPhi, Spiral

import bilby
from bilby.core.prior import Prior, WeightedDiscreteValues
from gwpy.timeseries import TimeSeries

from astropy import units as u

import argparse

def get_args(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', default='outdir')
    parser.add_argument('--label', default='GW150914')
    parser.add_argument('--trigger_time', type=float, default=1126259462.4)
    parser.add_argument('--post_trigger_duration', type=float, default=2.)
    parser.add_argument('--duration', type=float, default=4.)
    parser.add_argument('--detectors', nargs='+', default=["H1", "L1"])

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

def time_domain_source_model(
        gtimes,
        geocent_time=None,
        mass=None,
        theta=None,
        phi=None,
        dec=None,
        ra=None,
        psi=None,
        phase=None,
        zboost=None,
        post_trigger_duration=None
):
    print('TDSM ******')
    print(len(gtimes), gtimes[0])
    print('mass/theta/phi', mass, theta, phi)

    print('gpstimes', geocent_time, post_trigger_duration)

    galaxy = Spiral()
    galaxy.set_mcent((mass * 3.0 * u.km << u.lyr).value)
    galaxy.phi = phi
    galaxy.theta = theta

    hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value

    print(geocent_time, gtimes[0], gtimes[-1], len(gtimes))

    tstar = galaxy.tstar()

    # two parts to this the inspiral. what is the definition of gps time?
    # inspiral is up to post_trigger_duration
    # ringdown is the piece after

    minz = -0.9999

    phi = galaxy.phi

    tinspiral = np.array([gtime for gtime in gtimes if gtime < geocent_time + post_trigger_duration])
    tringdown= np.array([gtime for gtime in gtimes if gtime >= geocent_time + post_trigger_duration])

    # now we run into some numeric precision woes.
    # to sidestep this, assume our time runs zboost times faster than this theta/phi

    ####################
    # calculate ringdown
    ####################
    ttt = (tringdown - (geocent_time+post_trigger_duration)) * zboost / hubble_time

    uuu = np.array([galaxy.uoft(tstar + t) for t in ttt])
    zandx = [galaxy.zandx(t, u) for t, u in zip(ttt, uuu)]
    zzz = np.array([zx[0] for zx in zandx])
    xxx = np.array([zx[1] for zx in zandx])

    # base signal is a sine wave, wavelength schwartzchild radius
    scr = (galaxy.schwartzchild() << u.lightsecond).value
    strain = scr * np.sin(2*pi*uuu * hubble_time/scr)

    # amplitude of wave we see
    zp1 = 1 + zzz
    lum = 1 / (zp1*zp1*xxx*xxx)
    ringdown = strain*lum/(hubble_time*hubble_time)
    tb = galaxy.tb()
    doplot(ttt * hubble_time/zboost, 1/(zp1*zp1*xxx*xxx),
           f'strain tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')
    doplot(ttt * hubble_time/zboost, ringdown,
           f'ringdown tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')

    doplot(ttt * hubble_time/zboost, np.log(lum).clip(0, 15),
           f'luminosity tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')

    ####################
    # calculate inspiral
    ####################
    # now for the inspiral calculate inspiral
    ttt = (tinspiral - (geocent_time+post_trigger_duration)) * zboost / hubble_time

    # ttt <= 0., flip sign here
    uuu = np.array([galaxy.uoft(tstar - t) for t in ttt])
    zandx = [galaxy.zandx(t, u) for t, u in zip(ttt, uuu)]
    zzz = np.array([zx[0] for zx in zandx])
    xxx = np.array([zx[1] for zx in zandx])

    rr = (1-xxx) * hubble_time
    

    strain = (scr << u.lightsecond).value / (rr ** 3.0)

    inspiral = strain * np.sin(2*pi*uuu * hubble_time/scr)

    doplot(ttt * hubble_time/zboost, inspiral.clip(-1e-11, 1e-11),
           f'inspiral tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')
    
    doplot(ttt * hubble_time/zboost, uuu.clip(-10,10),
           f'u v t, tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')
    doplot(ttt[1:] * hubble_time/zboost, uuu[1:] - uuu[:-1],
           f'delta-u tb,theta,phi={tb:.4},{theta:.2},{phi:.2}')
    
    return dict(foo=inspiral.tolist() + ringdown.tolist())

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

        ax.plot(ttt, np.clip(zdash, 0, 1000), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.4f}')
        xax.plot(ttt, np.clip(xxx, 0, 2.), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.4f}')
        lax.plot(ttt, np.clip(np.log10(lum), 0, 15), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.4f}')
        du = uuu[1:] - uuu[0:-1]
        uax.plot(ttt[1:], np.clip(du, -1000, 1000), label=f'phi={aphi:.4f} theta={atheta:.4f} tb={tb:.4f}')

        
    xax.set_title('Distance v time')
    ax.set_title('zdash v time')
    lax.set_title('luminosity v time')
    uax.set_title('du v t')

    ax.legend()
    xax.legend()
    lax.legend()
    uax.legend()
    ax.show()
    xax.show()
    lax.show()
    uax.show()
    


class Sinh2(WeightedDiscreteValues):

    def __init__(self, name=None, maximum=None):

        random_phi = RandomPhi(max_phi=maximum)

        super().__init__(random_phi.values[1:], random_phi.counts, name=name)


def identity(arg):
    return arg, None

class Bilbo(magic.Ball):

    def __init__(self, args):

        self.args = args
        super().__init__()
    
    async def run(self):
        
        logger = bilby.core.utils.logger
        args = self.args

        outdir = args.outdir
        label = args.label
        trigger_time = args.trigger_time

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

        # We now define the prior.
        # We have defined our prior distribution in a local file, GW150914.prior
        # The prior is printed to the terminal at run-time.
        # You can overwrite this using the syntax below in the file,
        # or choose a fixed value by just providing a float value as the prior.
        priors = bilby.core.prior.PriorDict(filename=label + ".prior")

        # Add the geocent time prior if it is not already there
        if "geocent_time" not in priors:
            priors["geocent_time"] = bilby.core.prior.Uniform(
                trigger_time - 0.1, trigger_time + 0.1, name="geocent_time"
            )

        # Add post trigger duration.  geocent_time + post_trigger_duration is end of inspiral
        priors["post_trigger_duration"] = bilby.core.prior.DeltaFunction(
                peak=post_trigger_duration, name="post_trigger_duration"
            )
        

        for key in priors:
            if isinstance(priors[key], Prior):
                print(key, priors[key].is_fixed)

        print(priors.sample_subset(priors.keys(), size=1))
        #import pdb
        #pdb.set_trace()
        
        # In this step we define a `waveform_generator`. This is the object which
        # creates the frequency-domain strain. In this instance, we are using the
        # the Spiral source model. We also pass other parameters:
        # the waveform approximant and reference frequency and a parameter conversion
        # which allows us to sample in chirp mass and ratio rather than component mass
        waveform_generator = bilby.gw.WaveformGenerator(
            time_domain_source_model=time_domain_source_model,
            parameter_conversion=identity,
        )

        # In this step, we define the likelihood. Here we use the standard likelihood
        # function, passing it the data and the waveform generator.
        # Note, phase_marginalization is formally invalid with a precessing waveform such as IMRPhenomPv2
        likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
            ifo_list,
            waveform_generator,
            priors=priors,
            time_marginalization=True,
            phase_marginalization=False,
            distance_marginalization=False,
        )

        # Finally, we run the sampler. This function takes the likelihood and prior
        # along with some options for how to do the sampling and how to save the data
        result = bilby.run_sampler(
            likelihood,
            priors,
            sampler="dynesty",
            outdir=outdir,
            label=label,
            nlive=1000,
            check_point_delta_t=600,
            check_point_plot=True,
            npool=1,
            plot=False,  # until I give up on blume...
            #conversion_function=bilby.gw.conversion.generate_all_bbh_parameters,
            #result_class=bilby.gw.result.CBCResult,
        )
        result.plot_corner()



if __name__ == '__main__':

    args = get_args()

    baggins = Bilbo(args)

    land = farm.Farm()
    land.add(baggins)
    farm.run(land)
