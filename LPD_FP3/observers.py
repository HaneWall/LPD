from .utils import _create_array_from_slice, get_phase, get_amplitude
import numpy as np


class ParentObserver:
    '''
    Grundlegender Beobachter von dem nur Platzierungsmethoden vererbt werden
    '''
    def __init__(self):
        self.position = None
        self.grid = None
        self.observer_name = None

    def _place_into_grid(self, grid, index):
        if isinstance(index, int):
            self.grid = grid
            self.grid.observers.append(self)
            self.position = index
        elif isinstance(index, slice):
            self.grid = grid
            self.grid.observers.append(self)
            arr = _create_array_from_slice(index)
            self.position = arr

    def save_Ex(self):
        pass

class Point_Observer(ParentObserver):

    def __init__(self, name, first_timestep):
        super().__init__()
        self.observer_name = name
        self.first_timestep = first_timestep
        self.observedE = []

    @property
    def second_timestep(self):
        return self.first_timestep + 10

    @property
    def phase(self):
        return get_phase(timestep1=self.first_timestep, timestep2=self.second_timestep, y1=self.observedE[0],
                         y2=self.observedE[1], omega=self.grid.sources[0].omega, dt=self.grid.dt)

    @property
    def amplitude(self):
        return get_amplitude(timestep1=self.first_timestep, timestep2=self.second_timestep,
                             y1=self.observedE[0], y2=self.observedE[1], omega=self.grid.sources[0].omega, dt=self.grid.dt)

    
    def save_Ex(self):
        if self.grid.timesteps_passed == self.first_timestep:
            self.observedE.append(self.grid.Ex[self.position])

        elif self.grid.timesteps_passed == self.second_timestep:
            self.observedE.append(self.grid.Ex[self.position])