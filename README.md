# gaussian_free_E
scripts to perform frequency analysis and compute free energy of surface species (species with constrained atoms) in Gaussian


Gaussian09 has inbuilt features to calculate the free energies (translational, rotational, and vibrational) of gas phase species. However, it does not readily calculate the free energies of species with constrained atoms. An example of this can be when we are trying to calculate the free energy of surface species. The surface is at times represented by a small cluster, where the cluster is capped by terminating atoms and some peripheral atoms of the cluster are held fixed to mimic the rigidity of the surface. Fig. 1 shows a vicinal silica site used to represent a vicinal silanol site on the surface of silica.


![](images/silica_site.png)

Here, the cluster is capped by hydrogen atoms. And the peripheral OH groups (shown in red) are held fixed. To calculate the vibrational free energy we expand the enregy around the minimum (structure corresponding to a local minima) as follows:


![](images/silica_site.png)

Here, \delta x

$\delta$

$-b \pm \sqrt{b^2 - 4ac} \over 2a$
$x = a_0 + \frac{1}{a_1 + \frac{1}{a_2 + \frac{1}{a_3 + a_4}}}$
$\forall x \in X, \quad \exists y \leq \epsilon$



# This is an <h1> tag
## This is an <h2> tag
###### This is an <h6> tag

