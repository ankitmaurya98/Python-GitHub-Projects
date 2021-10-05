# Created 10/4/2021

# This is an example of the COEs_to_RV function which takes a given set of COEs and then outputs the respective R and V vectors




import Orbits_module as orbits
import math
import numpy as np

def main():
    rearth = 6378 # km
    muearth = 398600  # km^3/s^2
   
    # Test Case of Orbits 1 HW 3 Problem 4.15
    
    # S/C has the following orbital parameters:
    ecc = 1.5 # eccentricity
    altp = 300 # altitude at perigee, km
    inc = 35 # inclination, degrees
    RAAN = 130 # degrees
    argumentofperigee = 115 # degrees
    # at perigee so true anomaly is 0 degrees
    trueanomaly = 0 # degrees
    
    #Calculating h
    rp = altp + rearth # # radius at perigee, km
    h = math.sqrt(muearth*(1+ecc)*rp) # angular momentum, km^2/s

    statevectors = orbits.COEs_to_RV(h, ecc, inc, RAAN, argumentofperigee, trueanomaly)
    position = statevectors[0:1] # Extracting the position vector that is returned from the function
    position = position[0].tolist() # Converting the numpy array to a list
    velocity = statevectors[1:2] # Extracting the velocity vector that is returned from the function
    velocity = velocity[0].tolist() # Converting the numpy array to a list
    print(position)
    print(velocity)
    
    # Doing a check with COEs_Calculator to see if the same COEs are then returned
    [h_check, ecc_check, a_check, inc_check, RAAN_check, argumentofperigee_check, trueanomaly_check] = orbits.COEsFunction(position, velocity)
    
    print("The COEs:")
    print("Angular momentum (h): {} km^2/s".format(h_check))
    print("Eccentricity (ecc): {} ".format(ecc_check))
    print("Inclination (inc): {} degrees".format(inc_check))
    print("RAAN (omega): {} degrees".format(RAAN_check))
    print("Argument of Perigee: {} degrees".format(argumentofperigee_check))
    print("True Anomaly (theta): {} degrees".format(trueanomaly_check))
    

if __name__ == '__main__': main()