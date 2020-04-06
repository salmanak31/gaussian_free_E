import sys
import tamkin as tk

fixed = (12,13,14,15,16,17,18,19)
mobile = range(0, 9)

mol_both = tk.load_molecule_g03fchk('stuff.fchk')
nma_both = tk.NMA(mol_both, tk.PHVA(fixed))

from molmod import centimeter, lightspeed
invcm = lightspeed/centimeter
pf_both = tk.PartFun(nma_both, [])

print pf_both.free_energy(298.15)
print pf_both.free_enerngy(298.15)