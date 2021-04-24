import numpy as np
from .constants import c0


class ParentSource:
    '''
    Existiert nur zum Vererben der Platzierungseigenschaften im Grid
    '''

    def __init__(self):
        self.position = None
        self.grid = None

    def _place_into_grid(self, grid, index):
        if isinstance(index, int):
            self.grid = grid
            self.grid.sources.append(self)
            self.position = index
        elif isinstance(index, slice):
            raise KeyError('Not supporting slicing for sources!')

class Ramped_Sin(ParentSource):
    '''
    weiches Sinussignal, welches mit sin**2 aktiviert wird
    '''

    def __init__(self, wavelength, carrier_wavelength, amplitude, tfsf=False):
        super().__init__()
        self.lamb = wavelength
        self.carrier_lamb = carrier_wavelength
        self.ampl = amplitude
        self.tfsf = tfsf

    @property
    def carrier_omega(self):
        return 2 * np.pi * c0 / self.carrier_lamb

    @property
    def omega(self):
        return 2 * np.pi * c0 / self.lamb

    @property
    def period(self):
        return self.lamb / c0

    def step_Ex(self):
        if self.carrier_omega * self.grid.timesteps_passed * self.grid.dt < np.pi / 2:
            self.grid.Ex[self.position] += self.ampl * (np.sin(self.carrier_omega * self.grid.timesteps_passed * self.grid.dt))**2 * np.sin(self.omega * self.grid.timesteps_passed * self.grid.dt)

        else:
            self.grid.Ex[self.position] += self.ampl * np.sin(self.omega * self.grid.timesteps_passed * self.grid.dt)

    def step_By(self):
        if self.tfsf == False:
            pass

        else:
            if self.carrier_omega * self.grid.timesteps_passed * self.grid.dt < np.pi / 2:
                self.grid.By[self.position - 1] += 1/c0 * self.ampl * (np.sin(self.carrier_omega * (self.grid.timesteps_passed - 1) * self.grid.dt))**2 * np.sin(self.omega * (self.grid.timesteps_passed - 1) * self.grid.dt)
            else:
                self.grid.By[self.position - 1] += 1/c0 * self.ampl * np.sin(self.omega * (self.grid.timesteps_passed - 1) * self.grid.dt)



