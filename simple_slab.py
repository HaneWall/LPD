import LPD_FP3 as LPD
import numpy as np
from LPD_FP3.utils import theory_dielectric_slab
import matplotlib.pyplot as plt

# parameter
lamb = 800e-09
k_0 = 2*np.pi / lamb
N_lambda = 60
dz = lamb / N_lambda
eps_si = 1.4533 ** 2
Nz = 110
src_ind = 2
obs_ind = Nz - 3
timesteps = 15000

# init arrays
varying_d = np.arange(0, 40, 1)
amplitudes = np.zeros(len(varying_d))
phases = np.zeros(len(varying_d))
theo_amplitudes = np.zeros(len(varying_d))
theo_phases = np.zeros(len(varying_d))


def run_setup(thickness_in_dz):
    s_grid = LPD.Grid(Nz=Nz, dz=dz)
    s_grid[0] = LPD.LeftSideGridBoundary()
    s_grid[Nz-1] = LPD.RightSideGridBoundary()
    s_grid[src_ind] = LPD.Ramped_Sin(amplitude=1, wavelength=lamb, carrier_wavelength=lamb*15)
    s_grid[3:thickness_in_dz+3] = LPD.NonDispersive(permittivity=eps_si, name='Si02')
    s_grid[obs_ind] = LPD.Point_Observer(first_timestep=timesteps-15, name='getting_transmittance')
    s_grid.run_timesteps(timesteps=timesteps, vis=False, ani=False)
    if thickness_in_dz == 0:
        theo_ampl, theo_phase = 1, 0
    else:
        theo_ampl, theo_phase = theory_dielectric_slab(s_grid)
    return s_grid.observers[0].amplitude, s_grid.observers[0].phase, theo_ampl, theo_phase

def plot_results(varying_d, dz):
    fig, axes = plt.subplots(2)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Times"],
    })
    z = varying_d * dz
    axes[0].tick_params(direction='in', bottom=True, left=True, right=True, top=True)
    axes[0].grid(True, alpha=0.5, linestyle=':', color='k')
    axes[0].plot(z, theo_amplitudes, color='red', label=r'Theory')
    axes[0].plot(z, amplitudes, marker='o', color='k', mfc='None', ls='None', label=r'FDTD, $N_{\lambda}$='+'${}$'.format(N_lambda))
    axes[0].set_xlabel('$z$ in m')
    axes[0].set_ylabel('$E_{tr}$')
    axes[0].legend(ncol=2, fancybox=False, edgecolor='k', bbox_to_anchor=(0, 1), loc=3)

    axes[1].tick_params(direction='in', bottom=True, left=True, right=True, top=True)
    axes[1].grid(True, alpha=0.5, linestyle=':', color='k')
    axes[1].plot(z, theo_phases, color='red')
    axes[1].plot(z, phases, marker='o', color='k', mfc='None', ls='None')
    axes[1].set_xlabel('$z$ in m')
    axes[1].set_ylabel('$\phi$')
    plt.subplots_adjust(hspace=0)
    plt.show()

#  main script
for d in varying_d:
    amplitudes[d], phases[d], theo_amplitudes[d], theo_phases[d] = run_setup(d)
    phases[d] += np.angle(np.exp(-1j*k_0 * (obs_ind - src_ind) * dz))

plot_results(varying_d, dz)


