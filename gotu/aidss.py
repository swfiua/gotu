"""Conversing with chatgpt about the geometry of the universe.

It generated the code below when asked::

   Write python code to explore geodesics in de Sitter space

I have found chatgpt's willingness to answer questions regarding
astrophysics quite refreshing, as well as somewhat helpful.

I have started updating the code that chatgpt produced, as I want to
see how things change as you vary the initial conditions.

For now, I have had to change things around a bit so I can run the code 
with blume.   

2023/04/26 
==========

After playing with this a little, and switching to solve_ivp to avoid
some numerical madness, the geodesics aren't behaving quite how I might expect.

Time to go down the rabbit hole of curvature.

2023/05/07
==========

I am currently trying to reconcile the equations implicit in the
geodesic function with the presentation in the geometry of the universe.

Here, geodesics all converge to the origin eventually.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the parameters of de Sitter space
H = 1.0  # Hubble parameter
c = 1.0  # speed of light
G = 1.0  # gravitational constant
L = c**2 / H  # de Sitter radius
SIGN = -1

# Define the initial conditions and time range
u, v, w = 0., 0.5, 0.
x, y, z = 1.0, 0., 0.
t0, tfinal = 0.0, 20
axes = [True] * 4

show_time = False

# Define the geodesic equation
def geodesic(t, y):
    x, y, z, u, v, w = y
    r = np.sqrt(x**2 + y**2 + z**2)
    dxdt = u
    dydt = v
    dzdt = w

    # Calculate the acceslerations
    # Note how these are independent of t.
    
    dudt = SIGN * G * L**2 * x / r**4
    dvdt = SIGN * G * L**2 * y / r**4
    dwdt = SIGN * G * L**2 * z / r**4
    return [dxdt, dydt, dzdt, dudt, dvdt, dwdt]


def main():

    y0 = [x, y, z, u, v, w]

    results = solve_ivp(geodesic, (t0, tfinal), y0)

    sol = results['y']
    t = results['t']
    
    # Plot the trajectory in 3D
    ax = axes[0]


    ax.projection('3d')


    ax.plot(sol[0], sol[1], sol[2])
    if show_time:
        ax.plot(sol[0], sol[1], self.t)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.show()

    # Plot the trajectory in the x-y plane
    print('axe', type(ax))
    ax = axes[1]

    ax.plot(sol[0], sol[1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.show()

    ax = axes[2]

    r = (sol[0]**2 + sol[1] ** 2) ** 0.5
    ax.plot(t, r)
    ax.set_xlabel('t')
    ax.set_ylabel('r')
    ax.show()

    ax = axes[3]

    ax.plot(sol[3], sol[4])
    ax.set_xlabel('u')
    ax.set_ylabel('v')
    ax.show()

    
if __name__ == '__main__':

    from blume import farm
    fm = farm.Farm()

    dss = Dss()
    fm.add(dss)
    
    farm.run(fm)
