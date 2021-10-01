# Created 9/28/2021


# This is an example of propagating an orbit using the Universal Variable Method
# Problem 3.20 from Curtis is used as an example problem

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math


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
    

def main():
    # constants
    rearth = 6378 # km
    muearth = 398600 # km^3/s^2
    
    # Curtis Problem 3.20
    # Problem Statement: Given initial R and V vectors, find the R and V vectors 2 hours later
    
    # Inital Conditions
    rvect_initial = [20000, -105000, -19000]  # (km)
    vvect_initial = [.9000, -3.4000, -1.5000] # (km/s)
    initialdt = 2*3600                # hours converted to seconds
    
    # Universal Variable Function
    [rvect_new, vvect_new] = Universal_Variable_Prop(muearth, rvect_initial, vvect_initial, initialdt)
    
    print("The position vector 2 hours later is {} km".format(rvect_new))
    print("The magnitude of position is {} km".format(np.linalg.norm(rvect_new)))
    print("The velocity vector 2 hours later is {} km/s".format(vvect_new))
    print("The magnitude of velocity is {} km/s".format(np.linalg.norm(vvect_new)))
    
    
    
    print(" ")
    print("Check with 2 Body Motion ODE")
    # Check performed with 2 body motion propagator ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      # Initial state vectors
    r = rvect_initial   # Initial Position Vector
    v = vvect_initial    # Initial Velocity Vector
    state = np.concatenate((r, v))   # Combining state into 1 big array
    
    # time steps
    tf = 2*3600 # sec
    t = np.linspace(0, tf, 2000)   # With specified number of steps
    
    # solve ode
    propstate = odeint(two_body_motion, state, t, args = (muearth,))
    endstate = propstate[len(propstate) - 1] # Getting last line of propagated state values
    
    # Results
    position = endstate[0:3]
    location = np.linalg.norm(position)  # Calculating magnitude of position vector
    velocity  = endstate[3:6]
    speed = np.linalg.norm(velocity)     # Calculating magnitude of velocity to get speed
    
    print("The position vector after 2 hours is: {} (km)".format(position))
    print("The position is after 2 hours is {} km".format(location))
    print("The velocity after 2 hours is: {} (km/s)".format(velocity))
    print("The speed is after 2 hours is {} km/s".format(speed))



if __name__ == '__main__': main()
