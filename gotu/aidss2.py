""" Another chatgpt stab at geodesics in de Sitter Space 


"""
import math
import numpy as np
import matplotlib.pyplot as plt

# Define parameters
H = 1.0  # Hubble constant
L = 1.0  # de Sitter radius
m = 0.1  # mass of particle
tmax = 5.0  # maximum time
N = 1000  # number of time steps
dt = tmax / N  # time step size

# Define initial conditions
x0 = 0.0
y0 = L
px0 = m * np.sqrt((H*L)**2 - 1.0)  # ho-hum this is zero.
py0 = 0.0

# results
results = None

# Define the differential equations for x, y, px, and py
def f(t, X):
    x, y, px, py = X
    
    r = np.sqrt(x**2 + y**2)
    f_x = px / (m * r)
    f_y = py / (m * r)
    f_px = -m * H**2 * x / r**3
    f_py = -m * H**2 * y / r**3
    return np.array([f_x, f_y, f_px, f_py])

def main():
    # Solve the differential equations using the Runge-Kutta method

    t = 0.0
    X = np.array([x0, y0, px0, py0])
    xvals = [x0]
    yvals = [y0]
    tvals = [t]
    Xvals = [dict(t=t, x=x0, y=y0, px=px0, py=py0)]
    while t < tmax:
        k1 = dt * f(t, X)
        k2 = dt * f(t + 0.5*dt, X + 0.5*k1)
        k3 = dt * f(t + 0.5*dt, X + 0.5*k2)
        k4 = dt * f(t + dt, X + k3)
        X = X + (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0
        xvals.append(X[0])
        yvals.append(X[1])
        tvals.append(t)
        x, y, px, py = X
        Xvals.append(dict(t=t, x=x, y=y, px=px, py=py))
        t += dt

    global results
    results = Xvals
    
    # Plot the geodesic
    #plt.plot(xvals, yvals)
    plt.plot(tvals, xvals, label='x')
    plt.plot(tvals, yvals, label='y')
    plt.plot(tvals, list(x['py'] for x in Xvals), label='py')
    plt.plot(tvals, list(x['px'] for x in Xvals), label='px')
    plt.plot(tvals, list(math.sqrt(x['x']**2 + x['y']**2) for x in Xvals), label='r')
    #plt.xlim(-2*L, 2*L)
    #plt.ylim(-2*L, 2*L)
    #plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.xlabel('t')
    plt.show()

if __name__ == '__main__':

    main()
