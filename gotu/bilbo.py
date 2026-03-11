"""
I am exploring the python project bilby.

This is Bilbo Bilby, boldly going where no astrophysicist has gone before.

bilby takes priors and 
"""

from blume import magic
np = magic.np

from gotu.spiral import RandomPhi, Spiral

import bilby
from bilby.core.prior import Prior, WeightedDiscreteValues
from gwpy.timeseries import TimeSeries

from astropy import units as u

import argparse

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', default='outdir')
    parser.add_argument('--label', default='GW150914')
    parser.add_argument('--trigger_time', type=float, default=1126259462.4)
    parser.add_argument('--detectors', nargs='+', default=["H1", "L1"])

    return parser.parse_args()


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
):
    print('TDSM ******')
    print(len(gtimes), gtimes[0])
    print('mass/theta/phi', mass, theta, phi)

    galaxy = Spiral()
    galaxy.set_mcent((mass * 3.0 * u.km << u.lyr).value)
    galaxy.phi = phi
    galaxy.theta = theta

    hubble_time = (galaxy.cosmo.cosmo.hubble_time << u.s).value

    print(geocent_time, gtimes[0], gtimes[-1], len(gtimes))

    tstar = galaxy.tstar()

    minz = -0.9999

    phi_factor = phi
    zeds = [1 - (1/(10**blue)) for blue in range(1, 8)]
    while phi_factor < 35.:
        galaxy.phi = phi_factor

        tstar = galaxy.tstar()
        tminz = find_t_forz(galaxy, hubble_time, minz)
        tforz = [find_t_forz(galaxy, hubble_time, z) for z in zeds]
        tb = galaxy.tb()
        for zed, tforz in zip(zeds, tforz):
            print('phi z t tb', phi_factor, zed, tforz-tstar, tb, galaxy.zandx(tstar+tb))


        phi_factor *= 2.
    # reset galaxy.phi
    phi = galaxy.phi

    inspiral = gtimes[:int(len(gtimes)/2)]

    ttt = [tminz+((gtime-geocent_time)/hubble_time) for gtime in inspiral]
    uuu = [galaxy.uoft(t) for t in ttt]
    zandx = [galaxy.zandx(t, u) for t, u in zip(ttt, uuu)]
    zzz = [zx[0] for zx in zandx]
    xxx = [zx[1] * hubble_time for zx in zandx]

    wavelength = (galaxy.schwartzchild() << u.lightsecond).value

    delta_u = np.array(uuu[1:]) - np.array(uuu[:-1])
    print('urange:', uuu[0], uuu[-1])
    print('theta/phi/tb/tstar/umax', galaxy.theta, galaxy.phi, galaxy.tb(), galaxy.tstar(), galaxy.umax())

    return dict(foo=np.array([1e-18] * len(gtimes)))

def find_t_forz(galaxy, hubble_time, z, epsilon=1e-6):

    tstar = galaxy.tstar()
    tmin = tstar
    tb = galaxy.tb()
    tmax = tb + tmin

    while True:
        t = (tmax+tmin)/2
        zoft, xx = galaxy.zandx(t)
        print(t-tstar, zoft)
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

async def tfortb_show(galaxy, mintheta=0.001, maxtheta=.8, minphi=.5, maxphi=5., tb_factor=0.001):

    width = height = 1024
    tc = magic.TableCounts(title=f'z for tb * {tb_factor}',
        minx=mintheta, maxx=maxtheta, miny=minphi, maxy=maxphi,
        width=width, height=height, xname='theta', yname='phi',
        colorbar=True)
    
    tbtab = magic.TableCounts(title=f'blueshift time',
        minx=mintheta, maxx=maxtheta, miny=minphi, maxy=maxphi,
        width=width, height=height, xname='theta', yname='phi',
        colorbar=True)
    
    thetas = np.linspace(mintheta, maxtheta, width)
    phis = np.linspace(minphi, maxphi, height)

    sp = Spiral()
    for theta in thetas:
        for phi in phis:
            galaxy.theta = theta
            galaxy.phi = phi
            tb = galaxy.tb()
            z, x = galaxy.zandx(galaxy.tstar() + galaxy.tb() * tb_factor)
            tc.update([theta], [phi], 1/(1+z))
            tbtab.update([theta], [phi], tb)

    await tc.show()
    await tbtab.show()


class Sinh2(WeightedDiscreteValues):

    def __init__(self, name=None, maximum=None):

        random_phi = RandomPhi(max_phi=maximum)

        super().__init__(random_phi.values[1:], random_phi.counts, name=name)


def identity(arg):
    return arg, None

if __name__ == '__main__':

    logger = bilby.core.utils.logger

    args = get_args()

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
    duration = 4  # Analysis segment duration
    post_trigger_duration = 2  # Time between trigger time and end of segment
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

    # Add the geocent time prior
    priors["geocent_time"] = bilby.core.prior.Uniform(
        trigger_time - 0.1, trigger_time + 0.1, name="geocent_time"
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
        #parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
        #waveform_arguments={
        #    "waveform_approximant": "IMRPhenomPv2",
        #    "reference_frequency": 50,
        #},
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
        #conversion_function=bilby.gw.conversion.generate_all_bbh_parameters,
        #result_class=bilby.gw.result.CBCResult,
    )
    result.plot_corner()
