import numpy as np
from Utilities import plotRoverState

# z = [x,y, heading, psi1,psi2]

r = 5
w = 15

def euler_disc_kplus1(z_k, u_k):
    x_k, y_k, psi_k, phiL_k, phiR_k = z_k

    B = np.array([[-r/2*np.cos(psi_k), r/2*np.cos(psi_k)],
                  [-r/2*np.sin(psi_k), r/2*np.sin(psi_k)],
                  [r/w, -r/w],
                  [1, 0],
                  [0, 1]])
    z_kplus1 = z_k + B @ u_k
    return z_kplus1

# Simulate the system
z0 = np.array([0, 0, 0, 0, 0])
u = np.array([0, 0.01])

N = 200
trajectory = [z0]
timesteps = range(N)
u = np.array([u]*N)
for t in timesteps:
    trajectory.append(euler_disc_kplus1(trajectory[-1], u[t]))

trajectory = np.array(trajectory)
x,y, psi, phiL,phiR = trajectory.T

print(x)


import matplotlib.pyplot as plt
import numpy as np

# Enable interactive mode
plt.ion()

# Create the figure and axes
fig = plt.figure(figsize=(14, 6))  
ax1 = plt.subplot2grid((2, 4), (0, 0), colspan=2, rowspan=2)  # Large square axes
ax2 = plt.subplot2grid((2, 4), (0, 2))  # First row, first smaller plot
ax3 = plt.subplot2grid((2, 4), (0, 3))  # First row, second smaller plot
ax4 = plt.subplot2grid((2, 4), (1, 2))  # Second row, first smaller plot
ax5 = plt.subplot2grid((2, 4), (1, 3))  # Second row, second smaller plot

# Set axis limits and labels for ax1
ax1.set_xlim(-50, 50)
ax1.set_ylim(-50, 50)
ax1.set_aspect('equal')
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# Initialize empty plots for each axis
line2_x, = ax2.plot([], [], '.-', label='X-pos')
line2_y, = ax2.plot([], [], '.-', label='Y-pos')
line2_psi, = ax2.plot([], [], '.-', label='Heading')

line3_phiL, = ax3.plot([], [], '.-r', label="Lwhl θ")
line3_phiR, = ax3.plot([], [], '.-b', label="Rwhl θ")

line4_wheelL_x, = ax4.plot([], [], '.-r', label="Lwhl x")
line4_wheelL_y, = ax4.plot([], [], '.-r', label="Lwhl y")
line4_wheelR_x, = ax4.plot([], [], '.-b', label="Rwhl x")
line4_wheelR_y, = ax4.plot([], [], '.-b', label="Rwhl y")

line5_u1, = ax5.plot([], [], '.-r', label="u1")
line5_u2, = ax5.plot([], [], '.-b', label="u2")

# Add legends to the subplots
ax2.legend()
ax3.legend()
ax4.legend()
ax5.legend()

# Simulate real-time update
for frame in range(len(trajectory)):  # Replace with actual data source
    # Update the rover state plot
    ax1.clear()
    plotRoverState(ax1, *trajectory[frame], w, 0.3)

    # Update data for other subplots
    x, y, psi, phiL, phiR = trajectory.T
    wheelL_pos = np.array([x, y]).T + r*np.array([np.cos(psi+np.pi/2), np.sin(psi+np.pi/2)]).T
    wheelR_pos = np.array([x, y]).T + r*np.array([np.cos(psi-np.pi/2), np.sin(psi-np.pi/2)]).T

    # Update ax2 (X-pos, Y-pos, Heading)
    line2_x.set_data(range(frame+1), x[:frame+1])
    line2_y.set_data(range(frame+1), y[:frame+1])
    line2_psi.set_data(range(frame+1), psi[:frame+1])
    ax2.relim()
    ax2.autoscale_view()

    # Update ax3 (Wheel angles)
    line3_phiL.set_data(range(frame+1), phiL[:frame+1])
    line3_phiR.set_data(range(frame+1), phiR[:frame+1])
    ax3.relim()
    ax3.autoscale_view()

    # Update ax4 (Wheel positions)
    line4_wheelL_x.set_data(range(frame+1), wheelL_pos[:frame+1, 0])
    line4_wheelL_y.set_data(range(frame+1), wheelL_pos[:frame+1, 1])
    line4_wheelR_x.set_data(range(frame+1), wheelR_pos[:frame+1, 0])
    line4_wheelR_y.set_data(range(frame+1), wheelR_pos[:frame+1, 1])
    ax4.relim()
    ax4.autoscale_view()

    # Update ax5 (Inputs)
    if frame < len(u):  # Ensure we don't access out-of-bounds data
        line5_u1.set_data(range(frame+1), u[:frame+1, 0])
        line5_u2.set_data(range(frame+1), u[:frame+1, 1])
    else:
        line5_u1.set_data(range(len(u)), u[:, 0])  # Plot full input data once the trajectory is longer
        line5_u2.set_data(range(len(u)), u[:, 1])
    ax5.relim()
    ax5.autoscale_view()

    # Pause for real-time update
    plt.pause(0.01)

plt.ioff()  # Turn off interactive mode when done
plt.show()
