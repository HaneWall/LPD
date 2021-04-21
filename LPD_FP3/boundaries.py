import numpy as np


class Boundary:

    def __init__(self):
        self.position = None
        self.grid = None

    def _place_into_grid(self, grid, index):
        if isinstance(index, int):
            self.grid = grid
            self.grid.boundaries.append(self)
            self.position = index
        elif isinstance(index, slice):
            raise KeyError('Not supporting slicing for boundaries!')


class LeftSideGridBoundary(Boundary):
    '''
    Perfekt absorbierender linker 1D-Rand, funktioniert nur für S_c = 0.5
    '''

    def __init__(self):
        super().__init__()
        self.arr_Ex = np.zeros(2)

    def save_Ex(self):
        self.arr_Ex[1] = (self.grid.Ex[self.position + 1])     # 1st : [0] -> [0, Ez[pos+1]]

    def save_By(self):
        pass

    def step_Ex(self):
        self.grid.Ex[self.position] = self.arr_Ex[0]          # 2nd : [0, Ez[pos+1]] -> [Ez[pos+1]]
        self.arr_Ex = self.arr_Ex[::-1]

    def step_By(self):
        pass


class RightSideGridBoundary(Boundary):
    '''
    Perfekt absorbierender rechter 1D-Rand, funktioniert nur für S_c = 0.5
    '''

    def __init__(self):
        super().__init__()
        self.arr_Ex = np.zeros(2)

    def save_Ex(self):
        self.arr_Ex[1] = (self.grid.Ex[self.position - 1])

    def save_Hy(self):
        pass

    def step_Ex(self):
        self.grid.Ex[self.position] = self.arr_Ex[0]
        self.arr_Ex = self.arr_Ex[::-1]

    def step_Hy(self):
        pass