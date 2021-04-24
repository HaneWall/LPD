import LPD_FP3 as LPD

####### Bau dir deinen eigenen Sandkasten!  #######
grid_cells = 100
delta_z = 5e-09

grid = LPD.Grid(Nz=grid_cells, dz=delta_z)
grid[3] = LPD.Ramped_Sin(wavelength=800e-09, carrier_wavelength=10000e-09, amplitude=1, tfsf=True)
grid[0] = LPD.LeftSideGridBoundary()
grid[grid_cells-1] = LPD.RightSideGridBoundary()
#grid[20:74] = LPD.NonDispersive(name='testmaterial', permittivity=1.33)
#grid[60] = LPD.Point_Observer(name='test_obsever', first_timestep=1980)
grid.run_timesteps(2000, vis=True, ani=True)

#print(grid.observers[0].amplitude, grid.observers[0].phase)
#print(grid.observers[0].observedE)

