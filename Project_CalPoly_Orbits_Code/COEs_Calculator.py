# Created 9/17/2021

# Given position and velocity vector, this will then output the equivalent Classical Orbital Elements
# Inputs: R and V vector
# Output: COEs values in degrees and km
# Output order from first value to last:
#        h - angular momentum [km^2/s]
#        ecc - eccentricity
#        a - semi-major axis [km]
#        inc - inclination [degrees]
#        RAAN - Right Ascension of Acending Node [degrees]
#        argumentofperigee - Argument of Perigee [degrees]
#        trueanomaly - True Anomaly [degrees]


import numpy as np


def COEsFunction(rvect, vvect):
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

def main():
    
    # Test Case of Orbits 1 HW 2 Problem 4.5
    rvect = [6500, -7500, -2500] # Radius, km
    vvect = [4, 3, -3]
    
    [h, ecc, a, inc, RAAN, argumentofperigee, trueanomaly] = COEsFunction(rvect, vvect)
    
    print("The COEs:")
    print("Angular momentum (h): {} km^2/s".format(h))
    print("Eccentricity (ecc): {} ".format(ecc))
    print("Inclination (inc): {} degrees".format(inc))
    print("RAAN (omega): {} degrees".format(RAAN))
    print("Argument of Perigee: {} degrees".format(argumentofperigee))
    print("True Anomaly (theta): {} degrees".format(trueanomaly))
    


if __name__ == '__main__': main()

