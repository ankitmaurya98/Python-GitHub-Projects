# Created 8/25/2021

# This is a simple orbit that is propagated by 24 hours



import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


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
    ## Problem 3 Curtis 2.4
    ## Modify Problem so that using the given state vector, find position, position magnitude, velocity, and speed after 24 hours.
    ## Plot the orbit from t = 0 to t = 24 hrs
    
    # constants
    rearth = 6378 # km
    muearth = 398600 # km^3/s^2
    
    # Initial state vectors
    r = [3207.0, 5459.0, 2714.0]   # Initial Position Vector
    v = [-6.532, 0.7835, 6.142]    # Initial Velocity Vector
    state = np.concatenate((r, v))   # Combining state into 1 big array
    
    # time steps
    tf = 24*60*60 # sec
    t = np.linspace(0, tf, 2000)   # With specified number of steps
    
    # solve ode
    propstate = odeint(two_body_motion, state, t, args = (muearth,))
    endstate = propstate[len(propstate) - 1] # Getting last line of propagated state values
    
    # Results
    position = endstate[0:3]
    location = np.linalg.norm(position)  # Calculating magnitude of position vector
    velocity  = endstate[3:6]
    speed = np.linalg.norm(velocity)     # Calculating magnitude of velocity to get speed
    
    print("The position vector after 24 hours is: {} (km)".format(position))
    print("The position is after 24 hours is {} km".format(location))
    print("The velocity after 24 hours is: {} (km/s)".format(velocity))
    print("The speed is after 24 hours is {} km/s".format(speed))


    # Plotting of Orbit
    positionXarray = []
    positionYarray = []
    positionZarray = []
    for i in range(len(propstate)):
        statevect = propstate[i]
        positionvect = statevect[0:3]
        
        positionXarray.append(positionvect[0])
        positionYarray.append(positionvect[1])
        positionZarray.append(positionvect[2])
    
    
    # From https://www.geeksforgeeks.org/three-dimensional-plotting-in-python-using-matplotlib/
    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
        
    ax.plot3D(positionXarray, positionYarray, positionZarray, 'green')  # 3D plot
    ax.set_title('24 Hour Orbit')
    plt.show()
    
    
    plt.plot(positionXarray, positionYarray)  #2D Plot
    plt.xlabel('km')
    plt.ylabel('km')
    plt.title('24 Hour Orbit')
    plt.show()


if __name__ == '__main__': main()
