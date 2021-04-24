import numpy as np
from .constants import c0, mu0, eps0
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tqdm import tqdm

class Grid:
    '''
    Klasse welches ein Gridobjekt erstellt.
    Das eindimensionale Grid besteht dabei aus Nz Zellen mit jeweils einer Breite von dz.
    '''

    def __init__(self, Nz, dz):
        '''
        :param N_z: number of cells in z-direction
        :param dz: width of cell in m
        '''

        self.Nz = Nz
        self.dz = dz
        self.dt = dz/(2*c0)

        self.mu = np.ones(Nz)
        self.eps = np.ones(Nz)
        self.sigma = np.zeros(Nz)
        self.Ex = np.zeros(Nz)
        self.By = np.zeros(Nz)
        self.Px = np.zeros(Nz)

        self.timesteps = None
        self.timesteps_passed = 0

        # memory for objects
        self.sources = []
        self.materials = []
        self.boundaries = []
        self.observers = []

    def __setitem__(self, key, placing_obj):
        '''
        Hier überschreibe bzw. definiere ich den "grid[key] = placing_obj..." Aufruf.
        :param key: Position als index oder slice
        :param placing_obj: repräsentiert Material, Beobachter, Quellen oder Ränder
        :return:
        '''
        placing_obj._place_into_grid(grid=self, index=key)

    @property
    def ca(self):
        return (1 - (self.sigma * self.dt) / (2 * eps0 * self.eps)) / (1 + (self.sigma * self.dt) / (2 * eps0 * self.eps))

    @property
    def cb(self):
        return (c0 ** 2 * self.dt) / (self.eps * self.dz) / (1 + (self.sigma * self.dt) / (2 * eps0 * self.eps))

    def curl_By(self):
        return (self.By[1:self.Nz] - self.By[0:self.Nz - 1])

    def curl_Ex(self):
        return (self.Ex[1:self.Nz] - self.Ex[0:self.Nz-1])

    def step_Ex(self):
        self.Ex[1:self.Nz] = self.ca[1:self.Nz] * self.Ex[1:self.Nz] - self.cb[1:self.Nz] * self.curl_By()

    def step_By(self):
        self.By[0:self.Nz-1] = self.By[0:self.Nz-1] - self.dt / self.dz * self.curl_Ex()

    def run_timesteps(self, timesteps, vis=True, ani=False):
        '''
        :param timesteps: Anzahl der Zeitschritte, über die ich integrieren möchte
        :param vis: True/False parameter, welcher darüber entscheidet ob Plot am Ende der Simulation angezeigt wird
        :param ani: True/False parameter, welcher darüber entscheidet ob eine Live-Animation während der Simulation angezeigt wird
        :return:
        '''
        if vis or ani:
            fig, axes = plt.subplots(dpi=75)
        self.timesteps = timesteps

        for timestep in tqdm(range(1, self.timesteps + 1)):
            self.update()
            self.timesteps_passed += 1
            if ani and (self.timesteps_passed%5==0):
                axes.cla()

                for src in self.sources:
                    src_repr = Rectangle(xy=(src.position - 0.5, -src.ampl), height=2 * src.ampl, width=1, color='red',
                                         alpha=0.3)
                    axes.add_patch(src_repr)

                for obs in self.observers:
                    obs_repr = Rectangle(xy=(obs.position - 0.5, -1.4), height=2.8, width=1, color='green', alpha=0.3)
                    axes.add_patch(obs_repr)

                for mat in self.materials:
                    media_repr_0 = Rectangle(xy=(mat.position[0] - 0.5, -1.4), height=2.8,
                                             width=(mat.position[-1] - mat.position[0] + 1),
                                             color='grey', fill=True, alpha=mat.eps * 0.12)
                    axes.add_patch(media_repr_0)
                axes.set_ylim([-1.5, 1.5])
                axes.plot(self.Ex)
                axes.set_title('{}'.format(self.timesteps_passed))
                plt.pause(0.05)
        if vis:
            for src in self.sources:
                src_repr = Rectangle(xy=(src.position - 0.5, -src.ampl), height=2 * src.ampl, width=1, color='red',
                                     alpha=0.3)
                axes.add_patch(src_repr)

            for obs in self.observers:
                obs_repr = Rectangle(xy=(obs.position - 0.5, -1.4), height=2.8, width=1, color='green', alpha=0.3)
                axes.add_patch(obs_repr)

            for mat in self.materials:
                media_repr_0 = Rectangle(xy=(mat.position[0] - 0.5, -1.4), height=2.8,
                                         width=(mat.position[-1] - mat.position[0] + 1),
                                         color='grey', fill=True, alpha=mat.eps * 0.12)
                axes.add_patch(media_repr_0)
            axes.set_ylim([-2, 2])
            axes.plot(self.Ex)
            plt.show()

    def update(self):
        #for mat in self.materials:
        #   mat.step_P()

        self.step_Ex()
        #print(self.Ex)

        for src in self.sources:
            src.step_Ex()
            src.step_By()

        for bound in self.boundaries:
            bound.step_Ex()
            bound.save_Ex()

        self.step_By()

        for obs in self.observers:
            obs.save_Ex()
