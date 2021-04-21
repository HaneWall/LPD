from .utils import _create_array_from_slice

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

    def step_P(self):
        '''
        polarization
        :return:
        '''
        pass

    def step_J_p(self):
        '''
        polarization current
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
