""" Another chatgpt stab at geodesics in de Sitter Space 


"""
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
px0 = m * np.sqrt((H*L)**2 - 1.0)
py0 = 0.0

# Define the differential equations for x, y, px, and py
def f(t, X):
    x, y, px, py = X
    r = np.sqrt(x**2 + y**2)
    f_x = px / (m * r)
    f_y = py / (m * r)
    f_px = -m * H**2 * x / r**3
    f_py = -m * H**2 * y / r**3
    return np.array([f_x, f_y, f_px, f_py])

# Solve the differential equations using the Runge-Kutta method
t = 0.0
X = np.array([x0, y0, px0, py0])
xvals = [x0]
yvals = [y0]
while t < tmax:
    k1 = dt * f(t, X)
    k2 = dt * f(t + 0.5*dt, X + 0.5*k1)
    k3 = dt * f(t + 0.5*dt, X + 0.5*k2)
    k4 = dt * f(t + dt, X + k3)
    X = X + (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0
    xvals.append(X[0])
    yvals.append(X[1])
    t += dt

# Plot the geodesic
plt.plot(xvals, yvals)
plt.xlim(-2*L, 2*L)
plt.ylim(-2*L, 2*L)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
