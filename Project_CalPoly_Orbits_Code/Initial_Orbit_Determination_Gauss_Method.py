# Created 1/20/2022

# This program shows a working example of how the Gauss Method of Initial Orbit Determination can be used
# to predict R and V vectors from 3 observations
# The Gauss Extended method can only be used when the observations are separated by a small amount of time



import Orbits_module as orbits
import math
import numpy as np




def main():
   # Example problem taken from Cal Poly Aero 557 HW 1 Problem 1
   muearth = 398600 # km^3/s^2
   
   # Given:
   # Observations taken at 40 degs N, 110 degs W, alt = 2000 m, on August 20, 2010
   # Observation Time (hh:mm:ss) Rt Ascension (degs) Declination (degs)
   # 1           11:30:00        -33.0588410         -7.2056382
   # 2           11:50:00         55.0931551          36.5731946
   # 3           12:00:00         98.7739537          31.1314513
   
   
   lat = 40   # deg north
   long = 110 # deg west
   alt = 2000 # meters
   
   month = 8
   day = 20
   year = 2010

   
   # Defining right ascension and declination values for each observation
   # Converting degree values to radians
   RA1 = np.radians(-33.0588410)
   DEC1 = np.radians(-7.2056382)
   RA2 = np.radians(55.0931551)
   DEC2 = np.radians(36.5731946)
   RA3 = np.radians(98.7739537)
   DEC3 = np.radians(31.1314513)
   
   # Site vectors for each observation
   Rsite1 = orbits.R_site_calc(40,110,'west',2000, month, day, year, 11, 30, 0)
   Rsite2 = orbits.R_site_calc(40,110,'west',2000, month, day, year, 11, 50, 0)
   Rsite3 = orbits.R_site_calc(40,110,'west',2000, month, day, year, 12, 00, 0)
   
   # Gauss Method Non-Extended----------------------------------------------
   # Finding slant range direction
   rhohat1 = np.array([math.cos(DEC1)*math.cos(RA1), math.cos(DEC1)*math.sin(RA1), math.sin(DEC1)])
   rhohat2 = np.array([math.cos(DEC2)*math.cos(RA2), math.cos(DEC2)*math.sin(RA2), math.sin(DEC2)])
   rhohat3 = np.array([math.cos(DEC3)*math.cos(RA3), math.cos(DEC3)*math.sin(RA3), math.sin(DEC3)])
   
   # Tau
   Tau1 = (30-50)*60   # Time1-Time2 converted to seconds
   Tau3 = (60-50)*60   # Time3-Time2 converted to seconds
   Tau = Tau3 - Tau1
   
   # a values
   a1 = Tau3/Tau
   a1u = (Tau3*((Tau**2) - (Tau3**2)))/(Tau*6)
   a3 = -Tau1/Tau
   a3u = (-Tau1*((Tau**2) - (Tau1**2)))/(Tau*6)
   
   # Vallado Method beginning to set up eqn to solve for r2
   L = np.transpose([rhohat1, rhohat2, rhohat3])
   M = np.dot(np.linalg.inv(L), np.transpose([Rsite1, Rsite2, Rsite3]))   # taking inverse of L matrix and multiply with transpose of Rsite vectors
   d1 = M[1,0]*a1-M[1,1]+M[1,2]*a3
   d2 = M[1,0]*a1u+M[1,2]*a3u
   C = np.dot(rhohat2, np.transpose(Rsite2))
   
   # Solving for R2
   S = [1, 0, -((d1**2)+2*C*d1+(np.linalg.norm(Rsite2)**2)), 0, 0, -2*muearth*(C*d2+d1*d2), 0, 0, -(muearth**2)*(d2**2)]   # Coefficients of R2 eqn
   r2 = np.roots(S)   # finds all real and complex roots
   R2 = (r2[2]).real         # hardcoded to get the real root of r2
   
   # Getting u, c1, c3 based on R2
   u = muearth/(R2**3)
   c1 = a1+a1u*u
   c3 = a3+a3u*u
   c2 = -1
   
   # Getting rhos based on c-values
   rho2 = d1+d2*u
   RHS = np.dot(M, [[-c1], [-c2], [-c3]])  # Right hand side of matrix equation at beginning of Vallado Method
   rho1 = RHS[0,:]/c1
   rho3 = RHS[2,:]/c3
   
   # Solving for r vectors [km]
   rvect1 = rho1*rhohat1 + Rsite1
   rvect2 = rho2*rhohat2 + Rsite2
   rvect3 = rho3*rhohat3 + Rsite3
   
   # Getting Lagrange coefficients (to solve for V2)
   f1 = 1-(u/2)*(Tau1**2)
   g1 = Tau1-(u/6)*(Tau1**3)
   f3 = 1-(u/2)*(Tau3**2)
   g3 = Tau3-(u/6)*(Tau3**3)
   
   # Solving for V2 [km/s]
   vvect2 = (1/(f1*g3-f3*g1))*(-f3*rvect1+f1*rvect3)
   
   # Getting COEs
   [h, ecc, a, inc, RAAN, argumentofperigee, trueanomaly] = orbits.COEsFunction(rvect2, vvect2)
   
   print("Gauss Method Non-Extended--------------------------")
   print("The position vector is {} km".format(rvect2))
   print("The velocity vector is {} km/s".format(vvect2))
   print("The Resulting COEs are: ")
   print("ecc = {}".format(ecc))
   print("a = {} km".format(a))
   print("inc = {} deg".format(inc))
   print("RAAN = {} deg".format(RAAN))
   print("Argument of Perigee = {} deg".format(argumentofperigee))
   print("True Anomaly = {} deg".format(trueanomaly))
   print("h = {} km^2/s".format(h))
   print(" ")
   
   
   # Gauss Method Extended----------------------------------------------
   # FOR USE ONLY WHEN OBSERVATIONS ARE SEPARATED BY A SMALL AMOUNT OF TIME
   # Initialize before starting loop
   f1avg = []   # Creating the empty arrays
   g1avg = []
   f3avg = []
   g3avg = []
   rho1extend = []
   rho2extend = []
   rho3extend = []
   f1avg.append(f1)  # adding in the first elements
   g1avg.append(g1)
   f3avg.append(f3)
   g3avg.append(g3)
   rho1extend.append(rho1)
   rho2extend.append(rho2)
   rho3extend.append(rho3)
   
   tol = 1
   i = 1
   
   while tol > 1e-8:
      # Get new f and g values
      [f1extend,g1extend] = orbits.UniversalVariable_GaussExtended(muearth,rvect2,vvect2,Tau1)
      [f3extend,g3extend] = orbits.UniversalVariable_GaussExtended(muearth,rvect2,vvect2,Tau3)
      
      # Calculate average of f and g values
      f1avg.append((f1extend + f1avg[i-1])/2)
      g1avg.append((g1extend + g1avg[i-1])/2)
      f3avg.append((f3extend + f3avg[i-1])/2)
      g3avg.append((g3extend + g3avg[i-1])/2)
      
      # Calculate new c values
      c1extend = g3avg[i]/(f1avg[i]*g3avg[i]-f3avg[i]*g1avg[i])
      c3extend = -g1avg[i]/(f1avg[i]*g3avg[i]-f3avg[i]*g1avg[i])
      c2extend = -1
      
      # Calculate new rho values
      RHSextend = np.dot(M, [[-c1extend], [-c2extend], [-c3extend]]) # Right hand side of matrix equation at beginning of Vallado Method
      rho1extend.append(RHSextend[0,:]/c1extend)   # Calculate new rho values
      rho2extend.append(RHSextend[1,:]/c2extend)
      rho3extend.append(RHSextend[2,:]/c3extend)
      
      # Calculate new r vectors
      rvect1extend = rho1extend[i]*rhohat1 + Rsite1   # Calculate new r vectors
      rvect2extend = rho2extend[i]*rhohat2 + Rsite2
      rvect3extend = rho3extend[i]*rhohat3 + Rsite3
      
      # New velocity vector
      vvect2extend = (1/(f1avg[i]*g3avg[i]-f3avg[i]*g1avg[i]))*(-f3avg[i]*rvect1extend+f1avg[i]*rvect3extend)
      rvect2 = rvect2extend
      vvect2 = vvect2extend
      tol = abs(rho2extend[i] - rho2extend[i-1])  # Calculate tolerance
      
      i = i+1
   
   # Getting COEs
   [h, ecc, a, inc, RAAN, argumentofperigee, trueanomaly] = orbits.COEsFunction(rvect2, vvect2)
   
   print("Gauss Method Extended--------------------------")
   print("The position vector is {} km".format(rvect2))
   print("The velocity vector is {} km/s".format(vvect2))
   print("The Resulting COEs are: ")
   print("ecc = {}".format(ecc))
   print("a = {} km".format(a))
   print("inc = {} deg".format(inc))
   print("RAAN = {} deg".format(RAAN))
   print("Argument of Perigee = {} deg".format(argumentofperigee))
   print("True Anomaly = {} deg".format(trueanomaly))
   print("h = {} km^2/s".format(h))
      
   


if __name__ == '__main__': main()