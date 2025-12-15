#--- Importing Libraries

import pandas as pd #for data handling
import numpy as np #for math
from bioreactor_generalized import zones 

#--- Set Variables

#gravity
g_e= np.array([0, 0, -9.80665]) 

#--- Functions

#concentration change
def particle_concentration_time(initial_concentration, growth_rate, duration):
	return initial_concentration* np.exp(growth_rate* duration)

#volume 
def volume_sphere(particle_radius):
	return (4/3)* np.pi* particle_radius**3

#particle fraction change
def particle_fraction(particle_concentration, particle_radius):
	return particle_concentration* volume_sphere(particle_radius)


#fluid viscosity 
#link for equations: https://wiki.anton-paar.com/en/the-influence-of-particles-on-suspension-rheology/
def fluid_viscosity_time(p_fraction, fluid_viscosity_initial, intrinsic_viscosity, maximum_fraction):

	viscosity= np.zeros_like(p_fraction)

	for i, f in enumerate(p_fraction): 
		if i==0: 
			viscosity[i]= fluid_viscosity_initial 
		elif f<= 0.3: 
			viscosity[i]= fluid_viscosity_initial* (1+ intrinsic_viscosity* p_fraction[i-1]) #if the particle fraction is less than or equal 0.3 use Einstein's equation for fluid viscosity (linearity in dilute)
		else: 
			viscosity[i]= fluid_viscosity_initial* (1- (f/maximum_fraction))**(-intrinsic_viscosity* maximum_fraction) #if the particle fraction is greater than 0.3 use Krieger-Doughetry equation for fluid viscosity (non linear in concetrated)

	return viscosity	
					 

# sedimentation velocity 
#based on the gravitational- buoyancy- stokes drag
# for hindrance exponent https://web.iitd.ac.in/~sbasu/CHL331/R-Z1.pdf
def sedimentation_velocity(particle_density, fluid_density, particle_radius, p_fraction, viscosity, g_intended, hindrance_exponent):

	#initializing 
	v_sedimentation= np.zeros_like(p_fraction)
	g_normalized= np.linalg.norm(g_intended)

	for i, f in enumerate(p_fraction):	
		v_s= ((2/9)* (particle_density- fluid_density)* (particle_radius**2)* g_normalized)/ viscosity[i] #sedimentation velocity using Stokes Law
		if f> 0.3:
			v_sedimentation[i]= v_s* (1-f)**hindrance_exponent #with particle interaction
		else: 
			v_sedimentation[i]= v_s #without particles interacting with one another

	return v_sedimentation


#reynolds number
def reynolds_number(fluid_density, particle_radius, v_sedimentation, viscosity):
	return (2* fluid_density* v_sedimentation* particle_radius)/ viscosity


#laminar flow
def flow_type(reynolds): 
	return np.where(reynolds< 1, "Laminar Flow", "Not Laminar Flow") 


#angular linear velocity and shear
#the v(r) is a simplified Couette flow approx.
#the maximum angular velocity can be found by rearranging the Newtonian law
#the shear rate (gamma) is due to the parabolic laminar velocity 
def ang_linear_v_and_shear(maximum_shear_stress, viscosity, zone_choice, total_radius, delta_radius):

	radius_range= zones(total_radius, zone_choice)

	#initializing
	maximum_angular_velocity= np.zeros((len(viscosity), len(radius_range)))
	linear_velocity= np.zeros((len(viscosity), len(radius_range)))
	shear_stress= np.zeros((len(viscosity), len(radius_range)))

	for t in range(len(viscosity)):
		for r_i, r in enumerate(radius_range):
			maximum_angular_velocity[t, r_i]= maximum_shear_stress/ viscosity[t] 
			maximum_w= maximum_angular_velocity[t, r_i]

			if delta_radius== 0: #linear velocity
				linear_velocity[t, r_i]= maximum_w* total_radius* (1- (r/ total_radius)**2)  #velocity change
				gamma= -2* maximum_w* (r/ total_radius) #shear rate (change of velocity over radius change)
				shear_stress[t, r_i]= viscosity[t]* abs(gamma) #shear stress= viscosity* shear rate


			else: #parabolic velocity caused by the change of particle position 
				radius_min= max(0, r- delta_radius)
				radius_max= min(total_radius, r+ delta_radius)
				sampled_radius= np.linspace(radius_min, radius_max, 10)

				v_sampled= maximum_w* total_radius* (1- (sampled_radius/ total_radius)**2) #velocity change
				gamma_sampled= -2* maximum_w* (sampled_radius/ total_radius) #shear rate (change of velocity over radius change)
				ss_sampled= viscosity[t]* np.abs(gamma_sampled) #shear stress= viscosity* shear rate

				linear_velocity[t, r_i]= np.mean(v_sampled)
				shear_stress[t, r_i]= np.mean(ss_sampled)

	return maximum_angular_velocity, linear_velocity, shear_stress


#particle properties (the ones included there is definitely more to add!)
def particles_property(duration, particle_radius, particle_density, initial_particle_concentration, growth_factor, fluid_density, fluid_viscosity_initial, intrinsic_viscosity, maximum_fraction, maximum_shear_stress, g_intended, hindrance_exponent, total_radius, zone_choice, delta_radius):

	duration= np.array(duration)
	radius_range= zones(total_radius, zone_choice)
	concentration= particle_concentration_time(initial_particle_concentration, growth_factor, duration)
	fraction= particle_fraction(concentration, particle_radius)
	viscosity= fluid_viscosity_time(fraction, fluid_viscosity_initial, intrinsic_viscosity, maximum_fraction)
	v_sedimentation= sedimentation_velocity(particle_density, fluid_density, particle_radius, fraction, viscosity, g_intended, hindrance_exponent)
	rey_number= reynolds_number(fluid_density, particle_radius, v_sedimentation, viscosity)
	flow= flow_type(rey_number)
	angular_velocity, linear_velocity, shear= ang_linear_v_and_shear(maximum_shear_stress, viscosity, zone_choice, total_radius, delta_radius)

	#looping for data saving
	results= []
	for t in range(len(duration)):
		for r_i, r in enumerate(radius_range):
			results.append({"Time (hr)": duration[t], 
				"Concentration (particles/mL)": concentration[t], 
				"Particle Fraction": fraction[t], 
				"Viscosity (Pa.s)": viscosity[t], 
				"Sedimentation Velocity (m/s)": v_sedimentation[t], 
				"Reynolds Number": rey_number[t], 
				"Flow Type": flow[t], 
				"Delta Radius (m)": delta_radius[t],
				"Linear Velocity (m/s)": linear_velocity[t, r_i],
				"Shear Stress (Pa)": shear[t, r_i]})

	data_frame_particle_properties= pd.DataFrame(results)

	return data_frame_particle_properties
