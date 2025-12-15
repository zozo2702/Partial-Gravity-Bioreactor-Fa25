#--- Importing Libraries

import plotly.graph_objects as go #for plot
import numpy as np #for math

#--- Functions

#rotating bioreactor
def rotating_bioreactor(rpm, frame_number, fps, radius):

	layers_z= [0, radius/3, 2* radius/3, radius]
	particle_number= 12 #change if you want 

	wf= 2* np.pi* rpm/ (60* fps)
	
	#making the bioreactor
	theta= np.linspace(0, 2* np.pi, 50)
	rs= np.linspace(0, radius, 30)
	theta, rs= np.meshgrid(theta, rs)
	x_mesh= rs* np.cos(theta)
	z_mesh= rs* np.sin(theta)

	#zones
	colors= ["rgba(0, 150, 255, 0.15)", "rgba(0, 150, 255, 0.25)", "rgba(0, 150, 255, 0.35)"]

	layers= []
	for i in range(3):
		y= np.full_like(x_mesh, layers_z[i])
		layer_surface= go.Surface(x= x_mesh, y= y, z= z_mesh, surfacecolor= y, colorscale= [[0, colors[i]], [1, colors[i]]], showscale= False, opacity= 0.3)
		layers.append(layer_surface)
	
	#particle location
	np.random.seed(42)
	r_particles= np.random.uniform(0.2, radius, particle_number)
	theta_particles= np.random.uniform(0, 2* np.pi, particle_number)
	x_i= r_particles* np.cos(theta_particles)
	z_i= r_particles* np.sin(theta_particles)		
	y_i= np.random.uniform(0, radius, particle_number)
	
	#frames for animation
	frames= []
	for t in range(frame_number):
		angle= wf* t
		x_time= x_i* np.cos(angle)+ z_i* np.sin(angle)
		z_time= -x_i* np.sin(angle)+ z_i* np.cos(angle)
		frames.append(go.Frame(data= [go.Scatter3d(x= x_time, y= y_i, z= z_time, mode= "markers", marker= dict(size= 6, color= "orange", opacity= 0.9))], name= f"frame{t}"))

	
	#initial trace
	particle_trace= go.Scatter3d(x= x_i, y= y_i, z= z_i, mode= "markers", marker= dict(size= 6, color= "orange", opacity= 0.9))
	
	#everything
	fig= go.Figure(data= layers + [particle_trace], frames= frames)

	#layout
	fig.update_layout()
	fig.update_layout(scene= dict(xaxis_title= "X (m)", xaxis= dict(range= [-radius, radius], visible= True), yaxis_title= "Y (m)", yaxis= dict(range= [0, radius], visible= True), zaxis_title= "Z (m)", zaxis= dict(range= [-radius, radius], visible= True), aspectratio= dict(x= 1, y= 0.3, z= 1)), margin= dict(l= 0, r= 0, b= 0, t= 0), updatemenus= [dict(type= "buttons", showactive= False, x= 0.05, y= 0, buttons= [{'label': "Play", 'method': "animate", 'args': [None, {"frame": {"duration": 1000/fps, "redraw": True}, "fromcurrent": True}]}, {'label': "Pause", 'method': "animate", 'args': [None, {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}])])


	return fig