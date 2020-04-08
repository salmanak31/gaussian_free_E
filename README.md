# Calculating free energies of constrained species in Gaussian
scripts to perform frequency analysis and compute free energy of surface species (species with constrained atoms) in Gaussian






## Introduction

Gaussian09 has inbuilt features to calculate the free energies (translational, rotational, and vibrational) of gas phase species. However, it does not readily calculate the free energies of species with constrained atoms. An example of this can be when we are trying to calculate the free energy of surface species. The surface is at times represented by a small cluster, where the cluster is capped by terminating atoms and some peripheral atoms of the cluster are held fixed to mimic the rigidity of the surface. The figure below shows a vicinal silanol cluster used to represent a vicinal silanol site on the surface of silica.




<img src="images/silica_site.png" width=400>

Here, the cluster is capped by hydrogen atoms. And the peripheral OH groups (shown in red) are held fixed. To calculate the vibrational free energy we expand the enregy around the minimum (structure corresponding to a local minima) as follows:


<img src="images/E_expansion.png" width=300>

Here, ∆<strong>x</strong> is the deviation from the minima, <strong>H</strong> is the hessian computed at the minima, and <em>E</em><sub>0</sub> is the energy of the minima. H is written as follows:

<img src="images/hessian.png" width=500>.


Here, <em>x</em><sub>i</sub> is the ith coordinate. A molecule with N atoms has a total of 3N coordinates. Now, if we divide the hessian matrix into coordinates of peripheral (fixed) and non-peripheral (free) atoms, we can represent it as follows:

<img src="images/hessian_carving.png" width=500>.



Here, the red portion refers to peripheral atoms (fixed) and blue section refers to non-peripheral atoms (free). To eliminate the effects of the peripheral atoms only the blue sub-matrix is considered and is hence referred to as the reduced hessian represented as <strong>H</strong><sub>red</sub>.

The reduced hessian is mass weighted and diagonalized as follows:


<img src="images/mw_hessian.png" width=200>.


Here, <strong>H</strong><sub>MW</sub> is the reduced mass-weighted hessian and <strong>M</strong> is the mass matrix represented as

<img src="images/mass_matrix.png" width=500>.

Here, <em>M</em><sub>i</sub> is the mass of the atom corresponding to coordinate <em>x</em><sub>i</sub>. Following this the normal vibrational frequencies can be calculated using the eigenvalues of <strong>H</strong><sub>MW</sub> 


<img src="images/vib_eigen.png" width=150>.


Here ν<sub>i</sub> is the freq1uency of vibration of the ith normal mode and ε<sub>i</sub> is the ith eigenvalue of <strong>H</strong><sub>MW</sub>


The vibrational frequencies can be used to compute the ith vibrational partition function as follows:


<img src="images/q_vib.png" width=200>.

The total vibrational partition function is written as the product of the individual partition functions


<img src="images/total_vib.png" width=200>.


The vibrational partition function can then be used to calculate the vibrational contribution to the free energy


<img src="images/vib_free_e.png" width=200>.


## Usage

\g_free_e contains the code and an example Gaussian output file (vicinal silica site in Fig. 1).

Place all the atoms to be fixed at the end in the Guassian input file (opt.gjf).

When running a gaussian calculation generate a checkpoint file and convert it to a formatted checkpoint file using the following:

`<checkpoint filename> formchk <formatted checkpoint filename>`


The formatted checkpoint file contains the second order derivatives (Hessian). Following this run the generete_report.py as follows:

`python .\free_e_module.py <number of fixed atoms> <temperature> <output gaussian filename> <report filename>`

For example, 

`python .\free_e_module.py 8 298.15 opt.log Report.txt`

The output file reports to total free energy, enthalpy, entropy and normal vibrational frequencies.


## References

[1] F. Jensen. Introduction to Computational Chemistry. Wiley (1999)

