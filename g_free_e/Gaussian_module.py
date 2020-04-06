# processing gaussian frequency output
import numpy as np
from itertools import chain
outputfile = "freq.log"
N_fixed =  8
T = 298.15

class Gaussian_module:
    def __init__(self, Temperature, Pressure):
        self.Temperature = Temperature
        self.Pressure = Pressure
        # self.data = open(str(self), “r”)

    def getElectronic_E():
        # get electronic energy
        lookup = "SCF Done"   
        EE = []
        f = open(outputfile,"r")
        for line in f:
            if lookup in line:
                EE.append(line.split())
                break
        EE = float(EE[0][4])
        f.close()
        return EE