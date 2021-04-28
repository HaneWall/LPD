import LPD_FP3 as LPD
import numpy as np

'''
Platzhalter für Drude Slab
'''

import LPD_FP3 as LPD

####### Bau dir deinen eigenen Sandkasten!  #######
grid_cells = 500
delta_z = 3e-09

grid = LPD.Grid(Nz=grid_cells, dz=delta_z)
grid[200] = LPD.Ramped_Sin(wavelength=800e-09, carrier_wavelength=10000e-09, amplitude=0.5, tfsf=True)
grid[0] = LPD.LeftSideGridBoundary()
grid[grid_cells-1] = LPD.RightSideGridBoundary()
grid[300:310] = LPD.DrudeMaterial(name='testmaterial', eps_inf=1, number_density=5.86e28, gamma=6e12)
#grid[60] = LPD.Point_Observer(name='test_obsever', first_timestep=1980)
grid.run_timesteps(10000, vis=True, ani=False)

#print(grid.observers[0].amplitude, grid.observers[0].phase)
#print(grid.observers[0].observedE)

