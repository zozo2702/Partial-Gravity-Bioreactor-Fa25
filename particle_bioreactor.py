#--- Importing Libraries

import pandas as pd #for data handling and Excel export
import numpy as np #for math
from bioreactor_generalized import gravity, gravity_to_rpm_n_tilt, zones
from particle_properties import particle_concentration_time, particle_fraction, fluid_viscosity_time, sedimentation_velocity, reynolds_number, flow_type, ang_linear_v_and_shear

#--- Functions

#particle simulated

def particle_rotating(duration, g_intended, radius, zone_choice, particle_radius, particle_density, initial_particle_concentration, growth_factor, fluid_density, fluid_viscosity_initial, intrinsic_viscosity, maximum_fraction, hindrance_exponent, maximum_shear_stress, d_radius):

	#radius and time initiation and finding the particle properties
	radius_points= zones(radius, zone_choice)
	time_points= np.linspace(0, duration, 50)
	concentration= particle_concentration_time(initial_particle_concentration, growth_factor, time_points)
	fraction= particle_fraction(concentration, particle_radius)
	viscosity= fluid_viscosity_time(fraction, fluid_viscosity_initial, intrinsic_viscosity, maximum_fraction)
	v_sedimentation= sedimentation_velocity(particle_density, fluid_density, particle_radius, fraction, viscosity, g_intended, hindrance_exponent)
	angular_velocity, linear_velocity, shear= ang_linear_v_and_shear(maximum_shear_stress, viscosity, zone_choice, radius, d_radius)

	results= []

	#what is happening to the particle in the RPM
	for t_i, time in enumerate(time_points):
		for r_i, r in enumerate(radius_points):
			particle_state= "Particle is suspended" if linear_velocity[t_i, r_i]> v_sedimentation[t_i] else "Particle is settling" #seeing particle status
			results.append({"Time (hr)": time, "Radius (m)": r, "Linear Velocity (m/s)": linear_velocity[t_i, r_i], "Shear Stress (Pa)": shear[t_i, r_i], "Sedimentation Veloicty (m/s)": v_sedimentation[t_i], "Particle State": particle_state})

	particle_rotating_data_frame= pd.DataFrame(results)

	return particle_state, particle_rotating_data_frame


