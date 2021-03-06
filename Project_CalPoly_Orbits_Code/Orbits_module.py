# This module contains relevant functions that can be used for orbital mechanics problems

# Functions defined in this module:
#  Dealing with Time Calculations:
#       JulianDateCalc(): This function outputs the Julian Date from a given time
#       Local_Sidereal_Time_Calc(): This function calculates the Local Sidereal time based on the given date and time

#  2 Body Orbit Propagation:
#       two_body_motion(): This function is 2 body equations of motion which can then be used in the ODE calculator
#       ODE_two_body_motion():

#  Converting between R and V vectors and their COEs
#       COEsFunction(): This function converts R and V vectors into their Classical Orbital Elements
#       COEs_to_RV(): This function converts a given set of Classical Orbital Elements into the respective R and V vectors

#  Universal Variable Orbit Propagation
#       StumC(): Stumpff function used for Universal Variable Calculations
#       StumS(): Stumpff function used for Universal Variable Calculations
#       Universal_Variable_Prop(): Universal Variable Function

#  Orbit Determination Functions
#       R_site_calc(): This function calculates the site vector in ECI as it uses Local Sidereal Time
#       UniversalVariable_GaussExtended(): Variation of the Universal Variable method, just returns Lagrange coefficients to be used with Gauss method



# Importing additional modules
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math

# DEALING WITH TIME CALCULATIONS
# Julian Date Function
def JulianDateCalc(month, day, year, hour, minute, second):
   # This function outputs the Julian Date from a given time
   # Inputs:
   #       month - Month (1-12)
   #       day - Day
   #       year - Year
   #       hour - Hour (24 hour clock) and in UTC
   #       minute - Minutes and in UTC
   #       second - Seconds and in UTC
   # Outputs:
   #       JD - Julian Date
   #       UT - Universal Time (time fractions of the day)
   
   M = month
   D = day
   Y = year
   H = hour
   Min = minute
   S = second
   
   UT = H + Min/60+ S/3600
   
   J0 = 367*Y - math.floor((7*(Y+math.floor((M+9)/12)))/4) + math.floor((275*M)/9) + D + 1721013.5
   JD = J0 + (UT/24)
   
   return [JD, UT]

# Local Sidereal Time Function
def Local_Sidereal_Time_Calc(month, day, year, hour, minute, second, lam, direction):
    # This function calculates the Local Sidereal time based on the given date and time
    # Inputs:
    #       month - Month (1-12)
    #       day - Day
    #       year - Year
    #       hour - Hour (24 hour clock) and in UTC
    #       minute - Minutes and in UTC
    #       second - Seconds and in UTC
    #       lam - lambda value (represents east longitude)
    #       direction - string value of either east or west for longitude direction
    # Outputs:
    #       LST - Local Sidereal Time in Degrees
    
    M = month
    D = day
    Y = year
    H = hour
    Min = minute
    S = second
    
    J2000 = 2451545.0     # The Julian Date of Jan 1 2000 at noon
    juliancentury = 36525 # Sets the value of a Julian Century
    
    UT = JulianDateCalc(month, day, year, hour, minute, second)[1]  # Get just the UT at the current time
    # Calculating Julian Date at the beginning of the given day (not at current given time) so at 00:00:00
    JD = 367*Y - math.floor((7*(Y+math.floor((M+9)/12)))/4) + math.floor((275*M)/9) + D + 1721013.5
    
    T0 = (JD-J2000)/juliancentury
    thetaG0 = 100.4606184 + 36000.77004*T0 + .000387933*((T0)**2) - (2.583*(10**-8))*((T0)**3)
    
    while thetaG0 > 360 or thetaG0 < 0:
      if thetaG0 > 360:
         thetaG0 = thetaG0 - 360
      else:
         thetaG0 = thetaG0 + 360
         
    theta = thetaG0 + 360.98564724*(UT/24) # Greenwich Sidereal Time
    
    # Local Sidereal Time in degrees
    if direction == 'east':
      # Need to add lamda value
      LST = theta + lam
    else:
      # Subtract lamda value
      LST = theta + (360-lam)
    
    while LST >  360 or LST < 0:
      if LST > 360:
         LST = LST - 360
      else:
         LST = LST + 360

    return LST

#-----------------------------------------------------------------------------
# 2 Body Motion Orbit Equation ODE
def two_body_motion(state, t, muearth):
    
    x = state[0]     # x position
    y = state[1]     # y position
    z = state[2]     # z position
    
    dx = state[3]     # x velocity
    dy = state[4]     # y velocity
    dz = state[5]     # z velocity
    
    # Norm of position vector
    r = np.linalg.norm([x, y, z])
    
    # Acceleration and direction
    ddx = (-muearth*x)/(r**3);  # x acceleration
    ddy = (-muearth*y)/(r**3);  # y acceleration
    ddz = (-muearth*z)/(r**3);  # z acceleration
    
    return [dx, dy, dz, ddx, ddy, ddz]


def ODE_two_body_motion(rvect, vvect, tf, timestep):
    # This function is used to propagate forward the R and V vectors in the specified amount of time
    # Inputs:
    #       rvect - Position vector (km)
    #       vvect - Velocity vector (km/s)
    #       tf - How long to propagte forward (sec)
    #       timestep - How many steps ODE solver will take in that timespan
    # Outputs:
    #       propstate - Entire array of propagated R and V vectors
   
    
    # constants
    muearth = 398600 # km^3/s^2
    
    state = np.concatenate((rvect, vvect))   # Combining state into 1 big array
    
    # time steps
    t = np.linspace(0, tf, timestep)   # With specified number of steps
    
    # solve ode
    propstate = odeint(two_body_motion, state, t, args = (muearth,))
    
    return propstate

#-----------------------------------------------------------------------------
# CONVERTING BETWEEN R and V VECTORS and COEs
# R and V Vectors to COEs
def COEsFunction(rvect, vvect):
    # This function is used to convert the R and V vectors into the respective COEs
    # Inputs:
    #       rvect - Position vector (km)
    #       vvect - Velocity vector (km/s)
    # Outputs:
    #       h - angular momentum [km^2/s]
    #       ecc - eccentricity
    #       a - semi-major axis [km]
    #       inc - inclination [degrees]
    #       RAAN - Right Ascension of Acending Node [degrees]
    #       argumentofperigee - Argument of Perigee [degrees]
    #       trueanomaly - True Anomaly [degrees]
    
    muearth = 398600  # km^3/s^2
    
    # Normalize R and V vectors
    r = np.linalg.norm(rvect)
    v = np.linalg.norm(vvect)
    
    # Angular momentum, km^2/s
    hvect = np.cross(rvect,vvect) 
    h = np.linalg.norm(hvect)
    
    # Eccentricity
    eccvect = (1/muearth)*(np.cross(vvect,hvect)-muearth*(rvect/r))
    ecc = np.linalg.norm(eccvect)
    
    # Semi-major Axis
    a = ((h**2)/muearth)*(1/(1-ecc**2))
    
    # Inclination (degrees)
    inc = np.degrees(np.arccos(hvect[2]/np.linalg.norm(hvect)))
    
    # RAAN
    k = [0, 0, 1]  # k vector
    nodeline = np.cross(k,hvect)
    N = np.linalg.norm(nodeline)
    # Using nodeline to calculate RAAN
    if (nodeline[1] > 0):
        RAAN = np.degrees(np.arccos(nodeline[0]/N))
    else:
        RAAN = 360 - np.degrees(np.arccos(nodeline[0]/N)) 
    
    # Argument of Perigee
    if (eccvect[2] < 0):
    # if (np.dot(nodeline, eccvect) > 0):
        argumentofperigee = 360 - np.degrees(np.arccos(np.dot(nodeline,eccvect)/(N*ecc)))
    else:
        argumentofperigee = np.degrees(np.arccos(np.dot(nodeline,eccvect)/(N*ecc)))
    
    # True Anomaly
    radvelc = (np.dot(rvect,vvect)/np.linalg.norm(rvect)) # Radial velocity
    if (radvelc < 0):
        trueanomaly = 360 - np.degrees(np.arccos(np.dot(eccvect,rvect)/(ecc*np.linalg.norm(rvect))))
    else:
        trueanomaly = np.degrees(np.arccos(np.dot(eccvect,rvect)/(ecc*np.linalg.norm(rvect))))
    
    
    return [h, ecc, a, inc, RAAN, argumentofperigee, trueanomaly]


def COEs_to_RV(h, ecc, inc, RAAN, argumentofperigee, trueanomaly):
    # This function is used to convert COEs into the respective R and V vectors in the ECI frame
    # Inputs:
    #       h - angular momentum [km^2/s]
    #       ecc - eccentricity
    #       a - semi-major axis [km]
    #       inc - inclination [degrees]
    #       RAAN - Right Ascension of Acending Node [degrees]
    #       argumentofperigee - Argument of Perigee [degrees]
    #       trueanomaly - True Anomaly [degrees]
    # Outputs:
    #       r_eci - Position vector (km)
    #       v_eci - Velocity vector (km/s)
    
    muearth = 398600  # km^3/s^2
    
    # Initial Vectors in Perifocal Frame
    r = ((h**2)/muearth)*(1/(1 + ecc*math.cos(math.radians(trueanomaly))))*(np.array([math.cos(math.radians(trueanomaly)), math.sin(math.radians(trueanomaly)), 0]))
    v = (muearth/h)*(np.array([-math.sin(math.radians(trueanomaly)), ecc + math.cos(math.radians(trueanomaly)), 0]))
    
    # Perifocal Frame to ECI Frame Rotation Matrix
    # Principal Rotation about x-axis
    R1 = np.array([[1, 0, 0],
        [0, math.cos(math.radians(inc)), math.sin(math.radians(inc))],
        [0, -math.sin(math.radians(inc)), math.cos(math.radians(inc))]])
    # Principal Rotation about z-axis
    R3 = np.array([[math.cos(math.radians(argumentofperigee)), math.sin(math.radians(argumentofperigee)), 0],
        [-math.sin(math.radians(argumentofperigee)), math.cos(math.radians(argumentofperigee)), 0],
        [0, 0, 1]])
    # Principal Rotation about z-axis
    R3_2 = np.array([[math.cos(math.radians(RAAN)), math.sin(math.radians(RAAN)), 0],
        [-math.sin(math.radians(RAAN)), math.cos(math.radians(RAAN)), 0],
        [0, 0, 1]])
    # 3-1-3 Rotation Matrix
    Qperi2eci= np.transpose(R3 @ R1 @ R3_2) # matrix multiplication performed using @ operator instead of using np.matmul()
    
    # R and V vectors in ECI Frame
    r_eci = Qperi2eci @ r # matrix multiplication performed using @ operator instead of using np.matmul()
    v_eci = Qperi2eci @ v # matrix multiplication performed using @ operator instead of using np.matmul()
    
    return [r_eci, v_eci]

#-----------------------------------------------------------------------------
# UNIVERSAL VARIABLE PROPOGATION
# Stumpff Functions
def StumC(Z):
    if (Z > 0):
        C = (1-math.cos(math.sqrt(Z)))/Z     # cos calculated in radians
    elif (Z < 0):
        C = (math.cosh(math.sqrt(-Z))-1)/(-Z)
    elif(Z == 0):
        C = 1/2
    return C

def StumS(Z):
    if (Z > 0):
        S = (math.sqrt(Z) - math.sin(math.sqrt(Z)))/(Z**1.5)     # sin calculated in radians
    elif (Z < 0):
        S = (math.sinh(math.sqrt(-Z))-math.sqrt(-Z))/((-Z)**1.5)
    elif(Z == 0):
        S = 1/6
    return S


def Universal_Variable_Prop(muearth, rvect, vvect, initialdt):
    # This is the function for the Universal Variable Method that can be used to
    # find R and V vectors in an orbit after a specified amount of time
    # Inputs:
    #       muearth - Standard Gravitational Parameter (km^3/s^2)
    #       rvect - Position vector (km)
    #       vvect - Velocity vector (km/s)
    #       initialdt - Time step that will be used for the calculations, in units of seconds
    # Outputs:
    #       rvect_new - New calculated position vector based on the time step (km)
    #       vvect_new - New calculated velocity vector based on the time step (km/s)

    
    # Code for function based on code from Curtis
    dt = initialdt   # in units of seconds
    
    R = np.linalg.norm(rvect)
    V = np.linalg.norm(vvect)
    Vr = np.dot(rvect,vvect)/R
    alpha = (2/R) - ((V**2)/muearth)  # Reciprocal of semimajor axis (1/km) 
    
    # Error tolerance and limit on iterations
    e_tol = 1.0e-8
    n_max = 1000
    
    # Setup for loop 
    n = 0       # Iteration counter
    ratio = 1   # ratio that will represent the error
    x = math.sqrt(muearth)*abs(alpha)*dt # Initial Guess
    
    # Loop
    while abs(ratio) > e_tol and n <= n_max:
        z = alpha * (x**2)
        
        # Stumpff Functions
        C = StumC(z)
        S = StumS(z)
        
        F = R*Vr/math.sqrt(muearth)*x**2*C + (1-alpha*R)*(x**3)*S + R*x - math.sqrt(muearth)*dt
        dFdx = R*Vr/math.sqrt(muearth)*x*(1-alpha*(x**2)*S) + (1-alpha*R)*(x**2)*C + R
        ratio = F/dFdx
        
        x = x - ratio  # Recalculate x
        n += 1         # Increment n to keep track of number of iterations
    
    # Recalculate with finalized value
    z = alpha * (x**2)
    C = StumC(z)
    S = StumS(z)
    
    # Converting inputted r and v vectors into numpy arrays so that they can be multiplied by float values
    rvect_array = np.array(rvect)
    vvect_array = np.array(vvect)
    
    # Lagrange Coefficients and solving for new r and v vectors
    f = 1 - ((x**2)/R)*C
    g = dt - (1/math.sqrt(muearth))*(x**3)*S
    rvect_new = f*rvect_array + g*vvect_array
    R_new = np.linalg.norm(rvect_new)
    fdot = (math.sqrt(muearth)/(R_new*R))*x*(S*z-1)
    gdot = 1 - ((x**2)/R_new)*C
    vvect_new = fdot*rvect_array +  gdot*vvect_array
    
    return[rvect_new, vvect_new]

#-----------------------------------------------------------------------------
# ORBIT DETERMINATION FUNCTIONS

# R site vector calculation   
def R_site_calc(lat, long, direction, alt, month, day, year, hour, minute, second):
   # This function calculates the site vector in ECI as it uses local sidereal time
   # Inputs:
   #       lat - latitude [deg]
   #       long - longitude [deg]
   #       direction - string value of either east or west for longitude direction
   #       alt - Altitude [m]
   #       month - Month (1-12)
   #       day - Day
   #       year - Year
   #       hour - Hour (24 hour clock) and in UTC
   #       minute - Minutes and in UTC
   #       second - Seconds and in UTC
   # Outputs:
   #       Rsite - R site vector in ECI frame [km]
   
   
   H = alt/1000        # Convert altitude to km
   phi = np.radians(lat)  # Latitude converted to radians
   
   lam = long
   LST = Local_Sidereal_Time_Calc(month, day, year, hour, minute, second, lam, direction) # Local Sidereal Time calc
   theta = np.radians(LST)  # Converts LST to radians
   
   Re = 6378     # radius of Earth [km]
   f = 0.003353  # Oblateness factor
   
   # If use local sidereal time then Rsite is in ECI
   Rsite = np.array((((Re/math.sqrt(1-(2*f-(f**2))*(math.sin(phi))**2))+H)*math.cos(phi))*np.array([math.cos(theta), math.sin(theta), 0])+
      (((Re*(1-f)**2)/(math.sqrt(1-(2*f-(f**2))*(math.sin(phi))**2)))+H)*np.array([0, 0, math.sin(phi)]))
   
   return Rsite

# Universal Variable Function to be used with the Gauss Extended Method of Orbit Determination
def UniversalVariable_GaussExtended(muearth,rvect,vvect,initialdt):
   # Universal Variable method to get new Lagrange coefficients for Gauss Extended method
   # Inputs:
   #       muearth - Standard Gravitational Parameter (km^3/s^2)
   #       rvect - Position vector (km)
   #       vvect - Velocity vector (km/s)
   #       initialdt - Time step that will be used for the calculations, in units of seconds
   # Outputs:
   #       f - Lagrange coefficients
   #       g - Lagrange coefficients
   
   
   # Code for function based on code from Curtis
   dt = initialdt   # in units of seconds
    
   R = np.linalg.norm(rvect)
   V = np.linalg.norm(vvect)
   Vr = np.dot(rvect,vvect)/R
   alpha = (2/R) - ((V**2)/muearth)  # Reciprocal of semimajor axis (1/km) 
    
   # Error tolerance and limit on iterations
   e_tol = 1.0e-8
   n_max = 1000
   
   # Setup for loop 
   n = 0       # Iteration counter
   ratio = 1   # ratio that will represent the error
   x = math.sqrt(muearth)*abs(alpha)*dt # Initial Guess
   
   # Loop
   while abs(ratio) > e_tol and n <= n_max:
      z = alpha * (x**2)
        
      # Stumpff Functions
      C = StumC(z)
      S = StumS(z)
        
      F = R*Vr/math.sqrt(muearth)*x**2*C + (1-alpha*R)*(x**3)*S + R*x - math.sqrt(muearth)*dt
      dFdx = R*Vr/math.sqrt(muearth)*x*(1-alpha*(x**2)*S) + (1-alpha*R)*(x**2)*C + R
      ratio = F/dFdx
        
      x = x - ratio  # Recalculate x
      n += 1         # Increment n to keep track of number of iterations
    
   # Recalculate with finalized value
   z = alpha * (x**2)
   C = StumC(z)
   S = StumS(z)
    
   # Lagrange Coefficients and solving for new r and v vectors
   f = 1 - ((x**2)/R)*C
   g = dt - (1/math.sqrt(muearth))*(x**3)*S
   
   return [f,g]