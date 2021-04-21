import LPD_FP3 as LPD
import os
import numpy as np
from .utils import theory_dielectric_slab, get_phase, get_amplitude

class benchmark:
    '''
    Parent class for all benchmarks. Declares path/directory to store data
    '''


    def __init__(self, name, benchmark_type):
        self.name = name
        self.benchmark_type = benchmark_type
        self.dir_path = None
        self.grids = []

    def allocate_directory(self):
        self.dir_path = os.path.join(os.path.dirname(__file__), 'saved_data/'+self.benchmark_type+'/'+self.name)
        os.mkdir(path=self.dir_path)

    def store_obs_data(self):
        self.allocate_directory()
        for grid in self.grids:
            grid.store_obs_data(benchmark=True, benchmark_name=self.name)

class SimpleSlab(benchmark):
    '''
    Transmittance of monochromatic light through a non dispersive slab
    '''

    def __init__(self, name, dz, Nz, length_media_in_dz, start_index_media, wavelength, ampl, timesteps):
        super().__init__(name=name, benchmark_type='simple_slab')
        self.start_media = start_index_media
        self.dz = dz
        self.indices = []
        self.grids = []

        for grid in range(len(self.dz)):
            self.indices.append([start_index_media + 2 + i for i in np.arange(0, Nz[grid] - 1)])
            self.grids.append('grid_' + str(grid))
