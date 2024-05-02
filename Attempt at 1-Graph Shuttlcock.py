# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 00:59:10 2024

@author: noahg
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
from numpy import * # imports all of numpy without "np" nickname
#%%
def Service_Deg(THETA, PHI):
    # Constants and Variables
    m = (0.18 / 16) # lbs (since everything is in feet in J.M.A. Danby; 0.18 oz divided by 16 oz/lb) - https://rb.gy/nowitg
    t_0 = 0
    x_0 = 8.5 # ft (if back court line is 0.0 ft, then service line is 13.5 ft, given the total length is 20 ft to the net)
    y_0 = 13.5 # ft (if far-left court line is 0.0 ft, then divider is 8.5 ft, given the width is 17 ft)
    z_0 = (1.15 * 3.281) # ft (1.15 m times 3.281 ft/m) - https://rb.gy/lwa9pw
    # v = 10 m/s, so (82*3.281) ft/s, and if v = sqrt(v_x**2 + v_y**2 + v_z**2)
    v_0 = 10 * 3.281 # ft/s
    theta = np.pi * THETA / 180
    phi = np.pi * PHI / 180
    v_x_0 = v_0 * np.sin(phi)
    v_y_0 = v_0 * np.cos(theta) * np.cos(phi)
    v_z_0 = v_0 * np.sin(theta) * np.cos(phi)
    k_D = 0.00643 # ft^-1
    g = 32.17 # ft/s^2

    # Start time variations of Position and Velocity
    delta_t = 0.001
    Numerical_pos_x = np.array([])
    Numerical_pos_y = np.array([])
    Numerical_pos_z = np.array([])
    Numerical_v_x = np.array([])
    Numerical_v_y = np.array([])
    Numerical_v_z = np.array([])
    Numerical_speed = np.array([])
    time = np.array([])
    t_min = 0
    t_max = 3 # Analytical Guess from Changing t_max and viewing graphs
    n = round((t_max-t_min)/ delta_t)

    # Put initialized vars into first rows of arrays
    Numerical_pos_x = np.append(Numerical_pos_x, x_0)
    Numerical_pos_y = np.append(Numerical_pos_y, y_0)
    Numerical_pos_z = np.append(Numerical_pos_z, z_0)
    Numerical_v_x = np.append(Numerical_v_x, v_x_0)
    Numerical_v_y = np.append(Numerical_v_y, v_y_0)
    Numerical_v_z = np.append(Numerical_v_z, v_z_0)
    time = np.append(time,t_0)


    x = Numerical_pos_x[0] # initaial x value
    y = Numerical_pos_y[0] # initaial y value
    z = Numerical_pos_z[0] # initial z value
    x_dot = Numerical_v_x[0] # initial v_x value
    y_dot = Numerical_v_y[0] # initial v_y value
    z_dot = Numerical_v_z[0] # initial v_z value
    t = time[0] # initial t value
    
    for i in range(1, n): #For all the time steps
        x_ddot = -k_D * sqrt(x_dot**2 + y_dot**2 + z_dot**2) * x_dot
        y_ddot = -k_D * sqrt(x_dot**2 + y_dot**2 + z_dot**2) * y_dot
        z_ddot = -k_D * sqrt(x_dot**2 + y_dot**2 + z_dot**2) * z_dot - g

        x_dot += x_ddot*delta_t  #Euler method equation
        y_dot += y_ddot*delta_t 
        z_dot += z_ddot*delta_t 

        x -= x_dot*delta_t # Starting from midline, serving to the left (-x direction)
        y += y_dot*delta_t
        z += z_dot*delta_t

        t += delta_t #Update t to a new value based on Δt

        Numerical_pos_x = np.append(Numerical_pos_x, x) #Put your newest x value at the end of your table of x values
        Numerical_pos_y = np.append(Numerical_pos_y, y) 
        Numerical_pos_z = np.append(Numerical_pos_z, z) 
        Numerical_v_x = np.append(Numerical_v_x, x_dot)
        Numerical_v_y = np.append(Numerical_v_y, y_dot)
        Numerical_v_z = np.append(Numerical_v_z, z_dot)

        time = np.append(time, t)  #Put your newest t value at the end of your table of t values
        
        zero = 0
        for hits_ground in range(len(time)):
            if Numerical_pos_z[hits_ground] <= 0:
                zero = hits_ground
                break
                
    return Numerical_pos_x, Numerical_pos_y, Numerical_pos_z, zero

#%%
theta_f_l = 78.07
phi_f_l = 8.32

theta_f_r = 78.35
phi_f_r = 0.01

theta_b_l = 23.72
phi_b_l = 16.4

theta_b_r = 19.96
phi_b_r = 0.01

n = round(3 / 0.001)
#%%
ax = plt.axes(projection='3d')
ax.set_title(f'Ideal Shuttlecock Services', fontsize=20)
ax.set_xlabel('x(t) (ft)', fontsize=16)
ax.set_ylabel('y(t) (ft)', fontsize=16)
ax.set_zlabel('z(t) (ft)', fontsize=16)

# Starting Point
x_0 = 8.5
y_0 = 13.5
z_0 = 1.15 * 3.281
start_point = ax.plot(x_0, y_0, z_0, 'blue', marker='x', label=r'Serve Start', linewidth=3)
start_point_ground = ax.plot(x_0, y_0, 0, 'blue', marker='x', linewidth=3)
start_drop_down = ax.plot(linspace(x_0, x_0, n), linspace(y_0, y_0, n), linspace(0, z_0, n), 'blue', linestyle='--', linewidth=3)

# Plot trajectories for each type of serve
front_left = Service_Deg(theta_f_l, phi_f_l)
front_left_x = front_left[0]
front_left_y = front_left[1]
front_left_z = front_left[2]
zero_fl = front_left[3]
end_point = ax.plot(front_left_x[zero_fl], front_left_y[zero_fl], 0, 'red', marker='x', label=r'Serve End', linewidth=3)
ax.plot(front_left_x[:zero_fl], front_left_y[:zero_fl], front_left_z[:zero_fl], 'teal', label='Front Left', linewidth=3)

front_right = Service_Deg(theta_f_r, phi_f_r)
front_right_x = front_right[0]
front_right_y = front_right[1]
front_right_z = front_right[2]
zero_fr = front_right[3]
ax.plot(front_right_x[:zero_fr], front_right_y[:zero_fr], front_right_z[:zero_fr], 'gold', label='Front Right', linewidth=3)
end_point = ax.plot(front_right_x[zero_fr], front_right_y[zero_fr], 0, 'red', marker='x', linewidth=3)

back_left = Service_Deg(theta_b_l, phi_b_l)
back_left_x = back_left[0]
back_left_y = back_left[1]
back_left_z = back_left[2]
zero_bl = back_left[3]
ax.plot(back_left_x[:zero_bl], back_left_y[:zero_bl], back_left_z[:zero_bl], color='sienna', label='Back Left', linewidth=3)
end_point = ax.plot(back_left_x[zero_bl], back_left_y[zero_bl], 0, 'red', marker='x', linewidth=3)

back_right = Service_Deg(theta_b_r, phi_b_r)
back_right_x = back_right[0]
back_right_y = back_right[1]
back_right_z = back_right[2]
zero_br = back_right[3]
ax.plot(back_right_x[:zero_br], back_right_y[:zero_br], back_right_z[:zero_br], 'purple', label='Back Right', linewidth=3)
end_point = ax.plot(back_right_x[zero_br], back_right_y[zero_br], 0, 'red', marker='x', linewidth=3)

# Court Code
court_back = ax.plot(linspace(0,17,n), linspace(0,0,n), linspace(0,0,n), 'black', linewidth=2)
#, label=r'Court Design'
court_left = ax.plot(linspace(0,0,n), linspace(0,40,n), linspace(0,0,n), 'black', linewidth=2)
court_up = ax.plot(linspace(0,17,n), linspace(40,40,n), linspace(0,0,n), 'black', linewidth=2)
court_right = ax.plot(linspace(17,17,n), linspace(0,40,n), linspace(0,0,n), 'black', linewidth=2)
long_mid = ax.plot(linspace(8.5,8.5,n), linspace(0,40,n), linspace(0,0,n), 'black', linewidth=2)
service_line_1 = ax.plot(linspace(0,17,n), linspace(13.5,13.5,n), linspace(0,0,n), 'black', linewidth=2)
service_line_2 = ax.plot(linspace(0,17,n), linspace(25.5,25.5,n), linspace(0,0,n), 'black', linewidth=2)
net_left = ax.plot(linspace(0,0,n), linspace(20,20,n), linspace(0,5,n), 'black', linewidth=2)
net_right = ax.plot(linspace(17,17,n), linspace(20,20,n), linspace(0,5,n), 'black', linewidth=2)
net_bottom = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(3,3,n), 'black', linewidth=2)
net_top = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(5,5,n), 'black', linewidth=2)
net_top = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(0,0,n), 'black', linestyle='--', linewidth=2)

ax.tick_params(labelsize=14)

ax.view_init(azim=-25, elev=30)
ax.set_xlim3d(-1, 18)
ax.set_ylim3d(-1, 41)
ax.set_zlim3d(0, 18)

ax.legend(loc='best', fontsize=15)
# ax.figsize=(100,100,100)
#%%

# Initial Launch Conditions
x_0 = 8.5 # ft (if back court line is 0.0 ft, then service line is 13.5 ft, given the total length is 20 ft to the net)
y_0 = 13.5 # ft (if far-left court line is 0.0 ft, then divider is 8.5 ft, given the width is 17 ft)
z_0 = (1.15 * 3.281) # ft (1.15 m times 3.281 ft/m) - https://rb.gy/lwa9pw
v_0 = 10 * 3.281 # ft/s
theta = np.pi * 78.07 / 180
phi = np.pi * 8.32 / 180
v_x_0 = v_0 * np.sin(phi)
v_y_0 = v_0 * np.cos(theta) * np.cos(phi)
v_z_0 = v_0 * np.sin(theta) * np.cos(phi)

# Set up graph and plot
v_ax = plt.axes(projection='3d')
v_ax.set_title(f'Initial Shuttlecock Service Velocity', fontsize=20)
v_ax.set_xlabel('x(t) (ft)', fontsize=16)
v_ax.set_ylabel('y(t) (ft)', fontsize=16)
v_ax.set_zlabel('z(t) (ft)', fontsize=16)

# Init. Vel
v_ax.plot(linspace(x_0, -v_x_0+x_0, 100), linspace(y_0, v_y_0+y_0, 100), linspace(z_0, v_z_0+z_0, 100), 
          'purple', label=r'$\mathbf{v_{o}}$', linewidth=3)
v_ax.plot(-v_x_0+x_0, v_y_0+y_0, (v_z_0+z_0), 'purple', marker='<')

# Init. Vel in xy plane
v_ax.plot(linspace(x_0, -v_x_0+x_0, 100), linspace(y_0, v_y_0+y_0, 100), linspace(z_0, z_0, 100), 
          'red', label=r'$\mathbf{v_{xy}}$ Projection', linestyle='--', linewidth=3)
v_ax.plot(-v_x_0+x_0, v_y_0+y_0, z_0, 'red', marker='v')

# Init. Vel in xz plane
v_ax.plot(linspace(x_0, -v_x_0+x_0, 100), linspace(y_0, y_0, 100), linspace(z_0, v_z_0+z_0, 100), 
          'blue', label=r'$\mathbf{v_{xz}}$ Projection', linestyle='--', linewidth=3)
v_ax.plot(-v_x_0+x_0, y_0, v_z_0+z_0, 'blue', marker='^')

# Theta angle from xy up to Init. Vel ---------------------------------------------------------------------------
v_ax.text((x_0*.75), (y_0*1.2), (z_0*2), r'$\mathbf{\theta}$', color='orange', fontsize=16)


# radius = v_0
# x_y_plane = linspace(v_0, 0, 100)
# xy_to_z = sqrt(radius**2 - x_y_plane**2)
# circ = np.array([])
# circ_count = 0
# for i in range(100):
#     if xy_to_z[i] <= v_0:
#         circ = np.append(circ, xy_to_z[i]/2)
#         if xy_to_z[i] == v_0:
#             circ_count = i-10
# v_ax.plot(linspace(v_x_0/1.5, v_x_0/3, circ_count), linspace(v_y_0/1.5, v_y_0/3, circ_count), circ[:circ_count]/1.2, 'orange')


# Theta angle from xz over to Init. Vel -------------------------------------------------------------------------------
v_ax.text((x_0*.7), (y_0*1.1), (z_0*4), r'$\mathbf{\phi}$', color='green', fontsize=16)


# radius = v_0
# x_z_plane = linspace(v_0, 0, 100)
# xz_to_y = sqrt(radius**2 - x_z_plane**2)
# circ = np.array([])
# circ_count = 0
# for i in range(100):
#     if xz_to_y[i] <= v_0:
#         circ = np.append(circ, xz_to_y[i]/8)
#     if xz_to_y[i] == v_0:
#         circ_count = i
        
# v_ax.plot(linspace(v_x_0/2, v_x_0/6, circ_count), circ[:circ_count], linspace(v_z_0/2, v_z_0/6, circ_count), 'green')


# Plot xyz axis at origin
v_ax.plot(linspace(x_0, -v_x_0+x_0, 100), linspace(y_0, y_0, 100), linspace(0, 0, 100), 'black', linewidth=2)
v_ax.plot(linspace(x_0, x_0, 100), linspace(y_0, v_y_0+y_0, 100), linspace(0, 0, 100), 'black', linewidth=2)
v_ax.plot(linspace(x_0, x_0, 100), linspace(y_0, y_0, 100), linspace(0, v_z_0, 100), 'black', linewidth=2)

v_ax.tick_params(labelsize=14)

v_ax.view_init(azim=5, elev=15)
v_ax.legend(loc='best', fontsize=15)
plt.show()