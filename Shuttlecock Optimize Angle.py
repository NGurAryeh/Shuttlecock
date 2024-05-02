# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:05:46 2024

@author: noahg
8.3244
"""

# prepares notebook for "inline" graphing, and imports libraries that we'll use later.
import numpy as np
import matplotlib.pyplot as plt
from numpy import * # imports all of numpy without "np" nickname
    
# Non-Changing Constants Variables
m = (0.18 / 16) # lbs (since everything is in feet in J.M.A. Danby; 0.18 oz divided by 16 oz/lb) - https://rb.gy/nowitg
t_0 = 0
x_0 = 8.5 # ft (if back court line is 0.0 ft, then service line is 13.5 ft, given the total length is 20 ft to the net)
y_0 = 13.5 # ft (if far-left court line is 0.0 ft, then divider is 8.5 ft, given the width is 17 ft)
z_0 = (1.15 * 3.281) # ft (1.15 m times 3.281 ft/m) - https://rb.gy/lwa9pw
# v = 82 m/s (https://www.mdpi.com/2076-3417/11/7/2903), so (82*3.281) ft/s, and if v = sqrt(v_x**2 + v_y**2 + v_z**2)
v_0 = 10 * 3.281 # ft/s
k_D = 0.00643 # ft^-1
g = 32.17 # ft/s^2


# Optimize Theta and Phi
theta_best = 0
phi_best = 0
# for theta_best in arange(78.079507621, 78.079507622, 1e-14):
for phi_best in arange(8.32364, 8.32365, 1e-14):
    theta = np.pi * theta_best / 180
    phi = np.pi * phi_best / 180
    v_x_0 = v_0 * np. sin(phi)
    v_y_0 = v_0 * np.cos(theta) * np.cos(phi)
    v_z_0 = v_0 * np.sin(theta) * np.cos(phi)
    
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
        

        # Check conditions with tolerance for floating-point comparison
    if (abs(x) < 1e-2) and (abs(y - 25.5) < 1e-2):  # Adjust tolerance as needed
        print(f"phi = {phi_best}, theta = {theta_best}")
                
        
    # # PLOT!
    # fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3,sharex=True)
    # fig.suptitle('Positions & Velocities, x, y, & z', fontsize=14)
    
    # x_position = ax1.plot(time, Numerical_pos_x,'b', label=r'$x(t)$')
    # y_position = ax2.plot(time, Numerical_pos_y, 'r', label=r'$y(t)$')
    # z_position = ax3.plot(time, Numerical_pos_z, 'purple', label=r'$z(t)$')
    # ground_line = ax3.plot(time, np.linspace(0,0,n), 'black', label=r'Ground')
    
    # x_velocity = ax4.plot(time, Numerical_v_x, 'b', label=r'$\dot{x}(t)$')
    # y_velocity = ax5.plot(time, Numerical_v_y, 'r', label=r'$\dot{y}(t)$')
    # z_velocity = ax6.plot(time, Numerical_v_z, 'purple', label=r'$\dot{z}(t)$')
    
    # ax1.set_ylabel('Position')
    # ax4.set_ylabel('Velocity')
    # ax4.set_xlabel('Time')
    # ax5.set_xlabel('Time')
    # ax6.set_xlabel('Time')
    
    
    # ax1.legend(loc='best', fontsize = 12)
    # ax2.legend(loc='best', fontsize = 12)
    # ax3.legend(loc='best', fontsize = 12)
    # ax4.legend(loc='best', fontsize = 12)
    # ax5.legend(loc='best', fontsize = 12)
    # ax6.legend(loc='best', fontsize = 12)
    # fig.tight_layout()
    # plt.show()

#%%

ax = plt.axes(projection='3d')
ax.set_title("3-Dimensional Shuttlecock Shot")
# ax.set_axhline(0, color='black', lw=1)
# ax.set_axvline(0, color='black', lw=1)
ax.set_xlabel('x(t) (ft)')
ax.set_ylabel('y(t) (ft)')
ax.set_zlabel('z(t) (ft)')

for hits_ground in range(len(time)):
    if Numerical_pos_z[hits_ground] <= 0:
        # print(hits_ground)
        z_vs_xy = ax.plot(Numerical_pos_x[:hits_ground], Numerical_pos_y[:hits_ground], Numerical_pos_z[:hits_ground], 'purple', label=r'3D Flight Path')
        
        start_point = ax.plot(x_0, y_0, z_0, 'blue', marker='x', label=r'Serve Start')
        start_point_ground = ax.plot(x_0, y_0, 0, 'blue', marker='x')
        start_drop_down = ax.plot(linspace(x_0, x_0, n), linspace(y_0, y_0, n), linspace(0, z_0, n), 'blue', linestyle='--')
        end_point = ax.plot(Numerical_pos_x[hits_ground], Numerical_pos_y[hits_ground], 0, 'red', marker='x', label=r'Serve End')
        
        # Plotting Court
        court_back = ax.plot(linspace(0,17,n), linspace(0,0,n), linspace(0,0,n), 'black', label=r'Court Design')
        court_left = ax.plot(linspace(0,0,n), linspace(0,40,n), linspace(0,0,n), 'black')
        court_up = ax.plot(linspace(0,17,n), linspace(40,40,n), linspace(0,0,n), 'black')
        court_right = ax.plot(linspace(17,17,n), linspace(0,40,n), linspace(0,0,n), 'black')
        long_mid = ax.plot(linspace(8.5,8.5,n), linspace(0,40,n), linspace(0,0,n), 'black')
        service_line_1 = ax.plot(linspace(0,17,n), linspace(13.5,13.5,n), linspace(0,0,n), 'black')
        service_line_2 = ax.plot(linspace(0,17,n), linspace(25.5,25.5,n), linspace(0,0,n), 'black')
        net_left = ax.plot(linspace(0,0,n), linspace(20,20,n), linspace(0,5,n), 'black')
        net_right = ax.plot(linspace(17,17,n), linspace(20,20,n), linspace(0,5,n), 'black')
        net_bottom = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(3,3,n), 'black')
        net_top = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(5,5,n), 'black')
        net_top = ax.plot(linspace(0,17,n), linspace(20,20,n), linspace(0,0,n), 'black', linestyle='--')
        
        # Viewing Angle
        # for azmith in range(0,30,15):
            # print(azmith)
        ax.view_init(elev=65, azim=-101)
        ax.set_xlim3d(-.025, .025)
        ax.set_ylim3d(25, 26)
        # ax.set_zlim3d(0, 6)

        ax.legend(loc='best', fontsize=10)
        plt.show()
        break