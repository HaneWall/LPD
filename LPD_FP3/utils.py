'''
Funktionenspielkasten

Ein paar nette Funktionen, die immer mal wieder zu gebrauchen sind
'''
import numpy as np
from .constants import c0


def _create_array_from_slice(slice):
    arr = []
    for cell in range(slice.start, slice.stop):
        arr.append(cell)
    return arr

def get_phase(timestep1, timestep2, y1, y2, omega, dt):
    return (
            np.arctan2((y2 * np.sin(omega * timestep1 * dt) - y1 * np.sin(omega * timestep2 * dt)),
                   - (y1 * np.cos(omega * timestep2 * dt) - y2 * np.cos(omega * timestep1 * dt)))
    )


def get_amplitude(timestep1, timestep2, y1, y2, omega, dt):
    a = np.sqrt(y1 ** 2 + y2 ** 2 - 2 * y1 * y2*np.cos(omega * dt * (timestep2 - timestep1)))
    b = np.sin(omega*dt*(timestep2 - timestep1))
    return a / b

def theory_dielectric_slab(grid):
    d = ((grid.materials[0].position[-1] - grid.materials[0].position[0] + 1)) * grid.dz
    omega = grid.sources[0].omega
    n_real = np.sqrt((np.abs(grid.materials[0].epsilon_complex(omega)) + grid.materials[0].epsilon_real(omega)) / 2)
    kappa = np.sqrt((np.abs(grid.materials[0].epsilon_complex(omega)) - grid.materials[0].epsilon_real(omega)) / 2)
    n = n_real + 1j*kappa
    k0 = grid.sources[0].omega / c0
    k = n*k0
    q = ((n - 1) ** 2) / ((n + 1) ** 2) * np.exp(2j * k * d)
    e_inc = grid.sources[0].ampl
    e_tr = e_inc * (2 / (n + 1)) * (2 * n / (n + 1)) * (1 / (1 - q)) * np.exp(1j * (k - k0) * d)
    theo_amplitude = np.abs(e_tr)
    theo_phasenunterschied = np.angle(e_tr)
    return theo_amplitude, theo_phasenunterschied


