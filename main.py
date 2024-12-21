import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters for the simulation
Lx, Ly = 1.0, 1.0   # Domain size (meters)
nx, ny = 50, 50     # Number of grid points
alpha = 0.01        # Thermal diffusivity (m^2/s)
dx = Lx / (nx - 1)  # Grid spacing in x direction
dy = Ly / (ny - 1)  # Grid spacing in y direction
dt = 0.25 * min(dx, dy)**2 / alpha  # Time step for stability (CFL condition)
time_steps = 500    # Number of time steps to simulate

# Initialize temperature field
T = np.zeros((nx, ny))

# Initial condition: hot spot in the center
cx, cy = nx // 2, ny // 2
T[cx - 5:cx + 5, cy - 5:cy + 5] = 100.0  # Hot region

# Boundary conditions (fixed at 0 degrees)
def apply_boundary_conditions(T):
    T[0, :] = 0.0  # Bottom boundary
    T[-1, :] = 0.0  # Top boundary
    T[:, 0] = 0.0  # Left boundary
    T[:, -1] = 0.0  # Right boundary

# Time-stepping loop
def solve_heat_equation(T, alpha, dx, dy, dt, steps):
    for _ in range(steps):
        T_new = T.copy()
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                T_new[i, j] = T[i, j] + alpha * dt * (
                    (T[i + 1, j] - 2 * T[i, j] + T[i - 1, j]) / dx**2 +
                    (T[i, j + 1] - 2 * T[i, j] + T[i, j - 1]) / dy**2
                )
        T = T_new
        apply_boundary_conditions(T)
    return T

# Apply boundary conditions before starting the simulation
apply_boundary_conditions(T)

# Solve the heat equation
T_final = solve_heat_equation(T, alpha, dx, dy, dt, time_steps)

# Visualization of the final temperature distribution
plt.figure(figsize=(8, 6))
plt.imshow(T_final, extent=[0, Lx, 0, Ly], origin='lower', cmap='hot', aspect='auto')
plt.colorbar(label='Temperature (°C)')
plt.title('Final Temperature Distribution')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.show()

# Animation of temperature evolution
def update(frame):
    global T
    T = solve_heat_equation(T, alpha, dx, dy, dt, 1)
    im.set_array(T)
    return [im]

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(T, extent=[0, Lx, 0, Ly], origin='lower', cmap='hot', aspect='auto')
plt.colorbar(im, label='Temperature (°C)')
plt.title('Temperature Evolution')
ani = FuncAnimation(fig, update, frames=time_steps, interval=50, blit=True)
plt.show()
