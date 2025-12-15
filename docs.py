full_text = """
# Rotating Wall Vessel Bioreactor Prototype Calculations

To construct the prototype, specific calculations must be performed. These calculations will be utilized for simulation purposes to validate the prototype. 
To generalize the calculation, the specimen will be referred to as a **particle**; however, this term also applies to **cells** and the samples used during validation. 
Due to the numerous considerations involved in the calculation, the process will be divided into five sections: **Inclined Plane, Sedimentation Velocity, Angular Velocity, Revolutions per Minute, and Cellular Portion**.

---

## 1️⃣ Inclined Plane

The inclined plane facilitates the reduction of the gravitational force exerted on a particle by decomposing it into components.  

Referring to Figure 16, the gravitational force is entirely on one axis when:

$$
\\theta = 0^\\circ \\quad \\text{or} \\quad \\theta = 90^\\circ
$$

or decomposed into components. Using trigonometry, the parallel and perpendicular components of gravity relative to the plane are:

**Parallel gravitational component:**

$$
g_{\\parallel y} = g \\cdot \\sin(\\theta)  \quad (1)
$$

**Perpendicular gravitational component:**

$$
g_{\\perp} = g \\cdot \\cos(\\theta)  \quad (2)
$$

Where:  
- $g_{\\parallel y}$ = gravitational component parallel to the plane  
- $g_{\\perp}$ = gravitational component perpendicular to the plane  
- $g$ = gravitational acceleration (9.81 m/s²)  
- $\\theta$ = tilt angle of the plane  

---

## 2️⃣ Sedimentation Velocity

The sedimentation velocity $v_s$ of a particle can be calculated as:

$$
v_s = \\frac{2}{9} \\frac{(\\rho_p - \\rho_f) g r^2}{\\mu}
$$

Where:  
- $\\rho_p$ = particle density  
- $\\rho_f$ = fluid density  
- $r$ = particle radius  
- $\\mu$ = fluid viscosity  

---

## 3️⃣ Angular Velocity

Angular velocity $\\omega$ is related to the rotational speed (RPM):

$$
\\omega = 2 \\pi \\frac{\\text{RPM}}{60}
$$

The centripetal acceleration at a distance $r$ from the center:

$$
a_c = r \\cdot \\omega^2
$$

Where:  
- $r$ = radial distance (m)  
- $a_c$ = centripetal acceleration (m/s²)  

---

## 4️⃣ Revolutions per Minute (RPM)

If the intended gravity $g_{intended}$ is known, the corresponding RPM for a given radius is:

$$
\\text{RPM} = \\frac{60}{2\\pi} \\sqrt{\\frac{g_{intended}}{r}}
$$

Where:  
- $g_{intended}$ = target effective gravity along the plane  

---

## 5️⃣ Cellular / Particle Portion

The cellular fraction $f_c$ can be expressed as:

$$
f_c = \\frac{N_c}{N_{total}}
$$

Where:  
- $N_c$ = number of cells or particles in the sample  
- $N_{total}$ = total number of particles in the zone  

---

**References:**  
- Stokes, G. G., *On the effect of the internal friction of fluids on the motion of pendulums*, 1851  
- Standard bioreactor and fluid dynamics references
"""
