# processing gaussian frequency output
import numpy as np
from itertools import chain
outputfile = "opt.log"
N_fixed =  8
T = 298.15
def getZPE():
    lookup ="Zero-point correction="
    ZPE = []
    f = open(outputfile,"r")
    for line in f:
        if lookup in line:
            ZPE.append(line.split())
            break
    ZPE = float(ZPE[0][2])
    f.close()
    return ZPE

def getElectronic_E():
# function to get hartree fock energy, which value to get? scf done or hf value in the end
    lookup = "SCF Done"   
    # count = 0
    EE = []
    f = open(outputfile,"r")
    for line in f:
        if lookup in line:
            EE.append(line.split())
            # break
    EE = float(EE[-1][4])
    f.close()
    return EE


def getNum_atoms():
# function to get number of atoms
    lookup = "Charge ="   
    count = 0
    f = open(outputfile,"r")
    for line in f:
        if lookup in line:
            for i in range(0,1000000):
                line = next(f)
                if len(line.strip()) == 0:
                    break
                count = count + 1
        if count > 0:
            break
    Num_atoms = count
    f.close()
    return Num_atoms


def getMasses():
# function to  get masses
    lookup = "- Thermochemistry -"   
    Masses = []
    f = open(outputfile,"r")
    for line in f:
        if lookup in line:
            line = next(f)
            line = next(f)
            line = next(f)
            for i in range (0,getNum_atoms()):
                if "mass**********" in line.split()[-1]:
                    Masses.append("100000000")
                else:
                    Masses.append(line.split()[-1])
                line = next(f)
            break
    f.close()
    return Masses

def getHessian():
# function to get hessian from stuff.fchk file
    data = []
    breakcount = 0
    with open('stuff.fchk','r') as f:
	    for line in f:
		    if "Cartesian Force Constants" in line:
			    line=next(f)
			    for i in range(0,100000):
				    data.append(line.split())
				    line = next(f)
				    if "Dipole Moment" in line:
					    breakcount = 1
					    break
		    if breakcount == 1:
			    break	

    data = list(chain.from_iterable(data))

    hessian = np.zeros(shape=(3*getNum_atoms(),3*getNum_atoms()))
    m = 0 
    for i in range (0,3*getNum_atoms()):
        for j in range(0,i+1):
            hessian[i][j] = float(data[m])  
            m = m + 1
    hessian = np.triu(hessian.T,1) + hessian
    return hessian

def get_MWhess():
# function to mass weight hessian
    M = getMasses()[0:getNum_atoms() - N_fixed]
    M = np.asarray(M,dtype=np.float32)
    M = np.repeat(M, 3)
    convFactor = 4.3597439e-18 / (0.5291772086e-10) ** 2 / 1.66053878e-27
    carved_hess =  getHessian()[0:3*getNum_atoms()-3*N_fixed,0:3*getNum_atoms()-3*N_fixed]*convFactor
    # carved_hess = getHessian()
    MW_hess = np.dot(np.dot((np.diag(np.power(M,-0.5))),(carved_hess)),(np.diag(np.power(M,-0.5))))
    return MW_hess


def get_freq():
    # function to diagonalize hessian and get frequencies but removes negative frequencies
    eig = np.linalg.eigvals(get_MWhess())
    if N_fixed == 0:
        eig = np.sort(eig)[6:len(eig)]
        
    #eig = [(np.power(w,0.5)*219474.6*(2.99792458e10))/(2*3.14159) for w in eig]
    #eig = [(np.power(w,0.5))/(2*3.14159*(2.99792458e10)) for w in eig]
    # eig = [(np.power(np.abs(w),0.5))/(2*3.14159*(2.99792458e10)) for w in eig]
    neg_freq_index = [i for i, e in enumerate(eig) if e <0 ]
    eig = np.delete(eig,neg_freq_index)
    eig = [(np.power(np.abs(w),0.5))/(2*3.14159*(2.99792458e10)) for w in eig]
    return eig

def get_vibFreeE():
    kBT = T * 1.38064852E-23 / 4.35974465E-18
    kB = 1.38064852E-23 / 4.35974465E-18
    freq  = get_freq()
    # print(len(freq))
    # num_neg = sum(w < 0 for w in get_freq())
# add warning or abort command if more than one negative frequencies
    # neg_freq_index = [i for i, e in enumerate(get_freq()) if e <0 ]
    # freq = np.delete(freq,neg_freq_index)
    # print(len(freq))
    vibTemp = [1.98644568E-25 * 100 / 1.38064852E-23 * w for w in freq]
    # q_vib bot
    q_vib = [np.exp(-theta/(2*T))/(1-np.exp(-theta/T)) for theta in vibTemp]
    # q_vib zero
    q_vib_zero = [1/(1-np.exp(-theta/T)) for theta in vibTemp]
    q_vib_zero = np.prod(q_vib_zero) 
    # print(np.sort(np.log(q_vib)),len(q_vib))
    Gv_zero = -kBT*(np.log(q_vib_zero))
    q_vib = np.prod(q_vib) 
    Gv = -kBT*(np.log(q_vib))
    Sv = (kBT/T)*(np.sum([(theta/T)/(np.exp(theta/T)-1)-np.log(1-np.exp(-theta/T)) for theta in vibTemp]))
    Ev = (kBT/T)*(np.sum([theta*(0.5+1/(np.exp(theta/T)-1)) for theta in vibTemp]))  
    # print (np.sum([theta*(0.5+1./(np.exp(theta/T)-1)) for theta in vibTemp]))  
    return Ev, Sv, Gv, Gv_zero

def get_log_electronic_part():
    lookup1 = "Total Bot"
    lookup2 = "Electronic"
    log_electronic_p_func = []
    f = open(outputfile,"r")
    for line in f:
        if lookup1 in line:
            for i in range(0,1000000):
                line = next(f)
                if lookup2 in line:
                    log_electronic_p_func.append(line.split())
                    break
    log_electronic_p_func = float(log_electronic_p_func[0][3])
    f.close()
    return log_electronic_p_func

def get_transFreeE():
    lookup1 = "Total Bot"
    lookup2 = "Translational"
    log_trans_p_func = []
    f = open(outputfile,"r")
    for line in f:
        if lookup1 in line:
            for i in range(0,1000000):
                line = next(f)
                if lookup2 in line:
                    log_trans_p_func.append(line.split())
                    break
    log_trans_p_func = float(log_trans_p_func[0][3])
    Strans = kB*(log_trans_p_func+5./2.)
    Etrans = 1.5*kBT
    f.close()
    return log_trans_p_func, Strans, Etrans

def get_rotFreeE():
    lookup1 = "Total Bot"
    lookup2 = "Rotational"
    log_rot_p_func = []
    f = open(outputfile,"r")
    for line in f:
        if lookup1 in line:
            for i in range(0,1000000):
                line = next(f)
                if lookup2 in line:
                    log_rot_p_func.append(line.split())
                    break
    log_rot_p_func = float(log_rot_p_func[0][3])
    Srot = kB*( log_rot_p_func + 3./2. )
    Erot = kBT
    f.close()
    return log_rot_p_func, Srot, Erot

#print getNum_atoms()
#print getMasses()
#print get_freq()
#print get_vibFreeE()[3]+getElectronic_E()
#print get_vibFreeE()[1]
#print getElectronic_E()
#print get_vibFreeE()[0]
kBT = T * 1.38064852E-23 / 4.35974465E-18
kB = 1.38064852E-23 / 4.35974465E-18


# ADSORBED SPECIES
Free_E = get_vibFreeE()[2]  + getElectronic_E() - kBT*get_log_electronic_part()
Enthalpy = get_vibFreeE()[0]  + getElectronic_E() + kBT
# there is an extra ln(e) term in total entropy. Therefore have to add kBT. Check Gaussian's thermochem page.
Entropy = (T*get_vibFreeE()[1] + kBT*get_log_electronic_part()) + kBT

# Printing thermal energy
# print(2625.5*(get_vibFreeE()[0] + get_rotFreeE()[2] + get_transFreeE()[2] + kBT))
#FREE SPECIES

# Free_E = get_vibFreeE()[2]  + getElectronic_E() - kBT*(get_log_electronic_part()+ get_rotFreeE()[0]+get_transFreeE()[0])
# Entropy = (T*get_vibFreeE()[1] + kBT*get_log_electronic_part() + T*get_rotFreeE()[1] + T*get_transFreeE()[1]) 
# Enthalpy = Free_E + Entropy 

# print(2625.5*0.239006*1000*(Entropy/T), Free_E)

#print getElectronic_E()
f = open("Report_ZPE.txt","w")

f.write("Free energy: " + str(Free_E) + "\n")
f.write("Enthalpy: " + str(Enthalpy) + "\n")
f.write("Entropy: " +  str(Entropy))

f.close()

# f = open("Report_ZPE_vib.txt","w")

# f.write("Vibrational free energy(kJ/mol): " + str(2625.5*get_vibFreeE()[3]) + "\n")
# f.close()
