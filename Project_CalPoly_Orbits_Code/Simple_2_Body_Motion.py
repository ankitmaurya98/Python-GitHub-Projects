# Created 8/25/2021

# This is a simple orbit that is propagated by one period



import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt



def two_body_motion(state, t, muearth):
    
    x = state[0]
    y = state[1]
    z = state[2]
    
    dx = state[3]
    dy = state[4]
    dz = state[5]
    
    # Norm of position vector
    r = np.linalg.norm([x, y, z])
    
    # Acceleration and direction
    ddx = (-muearth*x)/(r**3);
    ddy = (-muearth*y)/(r**3);
    ddz = (-muearth*z)/(r**3);
    
    return [dx, dy, dz, ddx, ddy, ddz]


def main():
    ## Problem 3 Curtis 2.4
    
    # constants
    rearth = 6378 # km
    muearth = 398600 # km^3/s^2
    
    # Initial state vectors
    r = [3207.0, 5459.0, 2714.0]
    v = [-6.532, 0.7835, 6.142]
    state = np.concatenate((r, v))   # Combining state into 1 big array
    
    # time points
    tf = 24*60*60 # sec
    t = np.linspace(0, tf)
    
    # solve ode
    propstate = odeint(two_body_motion, state, t, args = (muearth,))
    endstate = propstate[len(propstate) - 1] # Getting last line of propogated state values
    print(endstate)
    
    # Results
    position = endstate[0:3]
    print(position)
    location = np.linalg.norm(position)
    velocity  = endstate[3:6]
    print(velocity)
    speed = np.linalg.norm(velocity)
    
    print("The position is after 24 hours is {} km".format(location))
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
        
    ax.plot3D(positionXarray, positionYarray, positionZarray, 'green')
    ax.set_title('24 Hour Orbit')
    plt.show()
    
    
    plt.plot(positionXarray, positionYarray)
    plt.show()


if __name__ == '__main__': main()
