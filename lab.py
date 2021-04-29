import LPD_FP3 as LPD
import numpy as np
from LPD_FP3.constants import c0, me, eps0, q

lamb = 800e-09
N_lambda = 100
dz = lamb / N_lambda
Nz = 250
src_ind = 30
obs_ind = 10
timesteps = 15000

plasma_freq = 2*np.pi * 2.321e15
n_silver = plasma_freq ** 2 * eps0 * me / (q ** 2)
print(n_silver)
gamma_silver = 2*np.pi * 5.513e13

####### Bau dir deinen eigenen Sandkasten!  #######
'''grid_cells = 100
delta_z = 5e-09

grid = LPD.Grid(Nz=grid_cells, dz=delta_z)
grid[3] = LPD.Ramped_Sin(wavelength=800e-09, carrier_wavelength=10000e-09, amplitude=1, tfsf=True)
grid[0] = LPD.LeftSideGridBoundary()
grid[grid_cells-1] = LPD.RightSideGridBoundary()
#grid[20:74] = LPD.NonDispersive(name='testmaterial', permittivity=1.33)
#grid[60] = LPD.Point_Observer(name='test_obsever', first_timestep=1980)
grid.run_timesteps(2000, vis=True, ani=True)'''

s_grid = LPD.Grid(Nz=Nz, dz=dz)
s_grid[0] = LPD.LeftSideGridBoundary()
s_grid[Nz - 1] = LPD.RightSideGridBoundary()
s_grid[src_ind] = LPD.Ramped_Sin(amplitude=0.5, wavelength=lamb, carrier_wavelength=lamb * 15, tfsf=True)
s_grid[55: 120] = LPD.DrudeMaterial(name='silver', eps_inf=1, number_density=n_silver, gamma=gamma_silver)
s_grid[obs_ind] = LPD.Point_Observer(first_timestep=timesteps - 15, name='getting reflectivity')
s_grid.run_timesteps(timesteps=timesteps, vis=True, ani=False)
#print(grid.observers[0].amplitude, grid.observers[0].phase)
#print(grid.observers[0].observedE)

