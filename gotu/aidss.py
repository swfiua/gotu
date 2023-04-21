import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define the parameters of de Sitter space
H = 1.0  # Hubble parameter
c = 1.0  # speed of light
G = 1.0  # gravitational constant
L = c**2 / H  # de Sitter radius

# Define the geodesic equation
def geodesic(y, t):
    x, y, z, u, v, w = y
    r = np.sqrt(x**2 + y**2 + z**2)
    dxdt = u
    dydt = v
    dzdt = w
    dudt = -G * L**2 * x / r**4
    dvdt = -G * L**2 * y / r**4
    dwdt = -G * L**2 * z / r**4
    return [dxdt, dydt, dzdt, dudt, dvdt, dwdt]

# Define the initial conditions and time range
y0 = [1.0, 0.0, 0.0, 0.0, 0.5, 0.0]  # initial position and velocity
t = np.linspace(0, 20, 1000)  # time range

# Solve the geodesic equation
sol = odeint(geodesic, y0, t)

# Plot the trajectory in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol[:, 0], sol[:, 1], sol[:, 2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

# Plot the trajectory in the x-y plane
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(sol[:, 0], sol[:, 1])
ax2.set_xlabel('x')
ax2.set_ylabel('y')
plt.show()
