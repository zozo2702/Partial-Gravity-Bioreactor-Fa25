# bioreactor_generalized.py
#--- Importing Libraries

import pandas as pd #for data handling and Excel export
import numpy as np #for math
import itertools #for clean nested loops 
from functools import lru_cache #to skip recomputed results and return from memory

#--- Set Variables

#gravity
g_e= np.array([0.0, 0.0, -9.80665]) 

#--- Functions

#rotation matrix about the x-axis
def rotation_matrix(theta_rad_plane):
    return np.array([[1.0, 0.0, 0.0],
                     [0.0, np.cos(theta_rad_plane), np.sin(theta_rad_plane)], 
                     [0.0, -np.sin(theta_rad_plane), np.cos(theta_rad_plane)]]) 

#tangent plane 
def tangent(theta_rad_plane):
    return np.array([0.0, np.cos(theta_rad_plane), np.sin(theta_rad_plane)])

#normal plane
def norm(theta_rad_plane):
    return np.array([0.0, -np.sin(theta_rad_plane), np.cos(theta_rad_plane)])

#RPM to angular velocity
def rpm_to_w(rpm):
    return (2.0* np.pi* rpm)/ 60.0 

#zones
def zones(radius, zone_choice):
    zones= np.linspace(0.0, radius, 4) #to have 3 zones with a start of 0
    inner_zone= np.linspace(1e-6,zones[1], 5) #5 data points for the inner zone
    middle_zone= np.linspace(zones[1],zones[2], 5) #5 data points for the middle zone
    outer_zone= np.linspace(zones[2],zones[3], 5) #5 data points for the outer zone
    radius_range= np.unique(np.concatenate([inner_zone, middle_zone, outer_zone])) #all zone points

    if zone_choice== "Inner Zone":
        radius_select= inner_zone 
    elif zone_choice== "Middle Zone":
        radius_select= middle_zone
    elif zone_choice== "Outer Zone":
        radius_select= outer_zone
    elif zone_choice== "All Zones":
        radius_select= radius_range
    elif zone_choice== "Outer Radius":
        radius_select= np.array([radius])
    else: 
        raise ValueError("Zone Choice Invalid") #checkpoint for error

    return radius_select

#gravity on the plane

@lru_cache(maxsize= None) 
def gravity(radius, rpm, tilt, zone_choice):
    ### What is happening: 
    #User input: radius, rpm, tilt angle, and zone choice
    #Find angular velocity and centripetal acceleration
    #Find the rotated Earth's gravity 
    #Find the centripetal acceleration in each particle position 
    #Find the total gravity and the gravity component
    #Now we have certain zones and the user should choose which zone for the output gravity for the zone
    ###

    #zones
    radius_select= zones(radius, zone_choice)

    #get angular velocity
    w= rpm_to_w(rpm)

    #angles
    tilt_angle= np.radians(tilt) 
    bioreactor_rotation_angle= np.radians(np.linspace(0, 360, 361)) #radians for particle positions

    #tilted 
    tangent_plane= tangent(tilt_angle)
    normal_plane= norm(tilt_angle)

    #make empty lists
    g_along_plane_list= np.zeros((len(bioreactor_rotation_angle), len(radius_select)))
    g_perpendicular_plane_list= np.zeros((len(bioreactor_rotation_angle), len(radius_select)))

    #particle position (assuming y doesn't change; no y component) "depending on zone"
    for a_idx, a in enumerate(bioreactor_rotation_angle): 
        for r_idx, r in enumerate(radius_select): 
            particle_x= r* np.cos(a) #x component of particle position (radically out)
            particle_y= np.zeros_like(particle_x)
            particle_z= r* np.sin(a) #z component of particle position	(radically out)
            particle_vector= np.array([particle_x, particle_y, particle_z]) #particle vector

            #centripetal acceleration
            centri_acc= -w**2* particle_vector #negative to be centripetal not centrifugal 

            #felt
            acceleration_tot= g_e+ centri_acc #total acceleration felt by particle
            g_along_plane_list[a_idx, r_idx]= np.dot(acceleration_tot, tangent_plane) #gravity along plane
            g_perpendicular_plane_list[a_idx, r_idx]= np.dot(acceleration_tot, normal_plane) #gravity perpendicular to the plane

    #RMS
    #mean along the plane 
    column_every_radi_along= np.sqrt(np.mean(g_along_plane_list**2, axis= 0)) #mean for all radii
    row_every_pos_along= np.sqrt(np.mean(g_along_plane_list**2, axis= 1)) #mean for all particle positions
    tot_along= np.sqrt(np.mean(g_along_plane_list**2)) #mean gravity

    #mean perpendicular to the plane
    column_every_radi_perpendicular= np.sqrt(np.mean(g_perpendicular_plane_list**2, axis= 0)) #mean for all radii
    row_every_pos_perpendicular= np.sqrt(np.mean(g_perpendicular_plane_list**2, axis= 1)) #mean for all positions
    tot_perpendicular= np.sqrt(np.mean(g_perpendicular_plane_list**2)) #mean gravity

    #flattening it out for data frame
    radius_list, angle_list= np.meshgrid(radius_select, np.degrees(bioreactor_rotation_angle), indexing= "ij")
    radius_list= radius_list.flatten()
    angle_list= angle_list.flatten()
    g_along_plane_flat= np.array(g_along_plane_list).T.flatten()
    g_perpendicular_plane_flat= np.array(g_perpendicular_plane_list).T.flatten()

    #put in data frame
    results_radius= {"Radius (m)": radius_select, "Mean Gravity at Every Radii": column_every_radi_along, "Mean Perpendicular Gravity at Every Radii": column_every_radi_perpendicular}
    data_frame_radius= pd.DataFrame(results_radius)

    results_angles= {"Angle (deg)": np.degrees(bioreactor_rotation_angle), "Mean Parallel Gravity at Every Position": row_every_pos_along, "Mean Perpendicular Gravity at Every Position": row_every_pos_perpendicular}
    data_frame_angle= pd.DataFrame(results_angles)

    results_overall= {"Mean Parallel Gravity": [tot_along], "Mean Perpendicular Gravity": [tot_perpendicular]}
    data_frame_overall= pd.DataFrame(results_overall)

    # RETURN original data + raw 2D arrays for heatmaps
    return tot_along, data_frame_radius, data_frame_angle, data_frame_overall, g_along_plane_list, g_perpendicular_plane_list



# finding tilt
def gravity_to_rpm_n_tilt(radius, g_intended, zone_choice):
    ### What is happening: 
    #User input: radius, gravity intended, and zone choice
    #Vectorize Earth's gravity 
    #Find the angle to get the intended gravity parallel to the plane
    #Add the centripetal acceleration to the perpendicular acceleration to get the intended centripetal acceleration
    #Find the rpm

    #zones
    radius_select= zones(radius, zone_choice)

    #gravity vectors and tilt
    g_normalized= np.linalg.norm(g_e)
    tilted= g_intended/ g_normalized
    tilted= np.clip(tilted, -1.0, 1.0) #remove ends to avoid errors 
    tilt= np.degrees(np.arcsin(tilted))
    tilt_rad= np.radians(tilt)

    g_perpendicular= g_normalized* np.cos(tilt_rad) #the rest of the gravity vector

    #get angular velocity
    w= np.sqrt(g_perpendicular/ radius_select)
    w_avg= np.mean(abs(w))

    #get rpm
    rpm= np.sqrt(w_avg* 60/ (2* np.pi))
        
    return rpm, tilt
