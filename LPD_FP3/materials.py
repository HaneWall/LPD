import numpy as np
from cached_property import cached_property
from .utils import _create_array_from_slice
from .constants import c0, mu0, eps0, me, q

class Vacuum:
    '''
    Vakuum Material von dem nur Platzierungsmethoden vererbt werden
    '''
    def __init__(self):
        self.eps = 1                    # permittivity
        self.mu = 1                     # permeability
        self.grid = None
        self.position = None
        self.material_name = 'vacuum'
        self.sigma = 0           # sigma
        self.model = None

    def _place_into_grid(self, grid, index):
        if isinstance(index, int):
            self.grid = grid
            self.grid.materials.append(self)
            self.position = index
            self.grid.eps[index] = self.eps
            self.grid.mu[index] = self.mu
            self.grid.sigma[index] = self.sigma

        elif isinstance(index, slice):          # note that [1:5] means cell INDICES 1, 2, 3, 4 are getting manipulated
            self.grid = grid
            self.grid.materials.append(self)
            arr = _create_array_from_slice(index)
            self.position = arr
            for cell in arr:
                self.grid.eps[cell] = self.eps
                self.grid.mu[cell] = self.mu
                self.grid.sigma[cell] = self.sigma

        else:
            raise KeyError('Currently not supporting these kind of keys! Use slice or simple index.')

    def step_Px(self):
        '''
        polarization
        :return:
        '''
        pass


class NonDispersive(Vacuum):
    '''
    Material welches konstantes reales n aufweist
    '''

    def __init__(self, name, permittivity):
        super().__init__()
        self.material_name = name
        self.eps = permittivity

    def epsilon_real(self, omega):
        return self.eps

    def epsilon_imag(self, omega):
        return 0

    def epsilon_complex(self, omega):
        return self.eps

class DrudeMaterial(Vacuum):
    '''
    Material welches dispersives Verhalten aufweist, -> complex epsilon
    '''

    def __init__(self, name, eps_inf, gamma, number_density):
        super().__init__()
        self.material_name = name
        self.eps = 1
        self.eps_inf = eps_inf
        self.gamma = gamma
        self.plasma_freq = np.sqrt((number_density * q ** 2) / (eps0 * me))
        print(self.plasma_freq)
        self.P_memory = None

    def _allocate_Px(self):
        self.Px = np.zeros(len(self.position), len(self.position)) # Speicher für timestep [n-1/2, n-3/2]

    def epsilon_comlex(self, omega):
        return self.eps_inf - self.plasma_freq ** 2 / (omega ** 2 + 1j * omega * self.gamma)

    def epsilon_real(self, omega):
        return np.real(self.epsilon_comlex(omega))

    def epsilon_imag(self, omega):
        return np.imag(self.epsilon_comlex(omega))


    # folgende Werte werden nur einmal berechnet (kann nicht in init durchgeführt werden, da dort Objekt noch nicht
    # vollständig in grid platziert -> keine Kenntnis über dt)
    @cached_property
    def da(self):
        da = (1/(self.grid.dt ** 2) + self.gamma/(2 * self.grid.dt))
        return da

    @cached_property
    def db(self):
        db = (1/(self.grid.dt ** 2) - self.gamma/(2 * self.grid.dt))
        return db

    def step_Px(self):
        if self.P_memory is None:
            self.P_memory = np.zeros((len(self.position), len(self.position)))
        self.grid.Px_mem[self.position[0]:(self.position[-1] + 1)] = self.grid.Px[self.position[0]:(self.position[-1] + 1)]
        self.grid.Px[self.position[0]:(self.position[-1] + 1)] = (eps0 * self.plasma_freq ** 2)/self.da * self.grid.Ex[self.position[0]:(self.position[-1] + 1)] \
                                                                 + 2/(self.grid.dt ** 2 * self.da) * self.grid.Px[self.position[0]:(self.position[-1] + 1)] \
                                                                 - self.db/self.da * self.P_memory[1]

        self.P_memory[1] = self.P_memory[0]
        self.P_memory[0] = self.grid.Px[self.position[0]:(self.position[-1] + 1)]
