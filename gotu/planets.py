"""
Simulate the solar system
"""

#from blume import magic, farm

from astropy import constants, units, coordinates, table, time

import datetime
import math

MOON_IN_EARTH_MASSES = 0.01

names = [
    'sun', 'mercury', 'venus', 'earth', 'moon', 'mars',
    'jupiter', 'saturn', 'neptune']
    
start = time.Time(datetime.datetime.now())

bodies = {}
for name in names:
    bodies[name] = coordinates.solar_system.get_body(name, start)

# add the masses, if we know them
bodies['earth'].mass = constants.M_earth
bodies['jupiter'].mass = constants.M_jup
bodies['sun'].mass = constants.M_sun
bodies['moon'].mass = bodies['earth'].mass * MOON_IN_EARTH_MASSES

print(bodies)    

# add their angular velocities
bodies['earth'].omega = 2 * math.pi * 24 * units.radian / units.hour
bodies['jupiter'].omega = 2 * math.pi * 10 * units.radian / units.hour
bodies['moon'].omega = 2 * math.pi * 28 * 24 * units.radian / units.hour
