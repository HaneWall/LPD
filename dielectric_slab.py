import LPD_FP3 as LPD
from LPD_FP3.utils import theory_dielectric_slab
import numpy as np
import matplotlib.pyplot as plt

'''
Platzhalter für Drude Slab
'''

lamb = 800e-09
k_0 = 2*np.pi / lamb
N_lambda = 100
dz = lamb / N_lambda
eps_si = 1.4533 ** 2
Nz = 250
src_ind = 2
obs_ind = Nz - 3
timesteps = 15000

#number_density=5.86e28
number_density = 1e27
gammas = [0, 2e13, 9e13, 1.6e14]

varying_d = np.arange(2, 200, 2)
amplitudes = np.zeros((len(gammas),len(varying_d)))
phases = np.zeros((len(gammas),len(varying_d)))
theo_amplitudes = np.zeros((len(gammas),len(varying_d)))
theo_phases = np.zeros((len(gammas),len(varying_d)))

def run_setup(thickness_in_dz, gamma):
    s_grid = LPD.Grid(Nz=Nz, dz=dz)
    s_grid[0] = LPD.LeftSideGridBoundary()
    s_grid[Nz-1] = LPD.RightSideGridBoundary()
    s_grid[src_ind] = LPD.Ramped_Sin(amplitude=1, wavelength=lamb, carrier_wavelength=lamb*15)
    if thickness_in_dz != 0:
        s_grid[3:thickness_in_dz+3] = LPD.DrudeMaterial(name='testmaterial', eps_inf=1, number_density=number_density, gamma=gamma)
    s_grid[obs_ind] = LPD.Point_Observer(first_timestep=timesteps-15, name='getting_transmittance')
    s_grid.run_timesteps(timesteps=timesteps, vis=False, ani=False)
    if thickness_in_dz == 0:
        theo_ampl, theo_phase = 1, 0
    else:
        theo_ampl, theo_phase = theory_dielectric_slab(s_grid)
    return s_grid.observers[0].amplitude, s_grid.observers[0].phase, theo_ampl, theo_phase


def plot_results(gammas, varying_d, dz):
    fig, axes = plt.subplots(figsize=(6, 5))
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Times"],
    })
    z = varying_d * dz
    axes.tick_params(direction='in', bottom=True, left=True, right=True, top=True)
    axes.grid(True, alpha=0.5, linestyle=':', color='k')
    for g_idx in range(len(gammas)):
        axes.plot(z, theo_amplitudes[g_idx, :], label=r'Theory, $\gamma$=' + '${:.2E}$'.format(gammas[g_idx]))
        if g_idx == 0:
            axes.plot(z, amplitudes[g_idx, :], markersize=4, marker='o', color='k', mfc='None', ls='None', label=r'FDTD, $N_{\lambda}$='+'${}$'.format(N_lambda))
        else:
            axes.plot(z, amplitudes[g_idx, :], markersize=4, marker='o', color='k', mfc='None', ls='None')
    axes.set_xlabel('$z$ in m')
    axes.set_ylabel('$E_{tr}$')
    axes.legend(ncol=1, fancybox=False, edgecolor='k', bbox_to_anchor=(0, 0.1), loc=3)
    plt.show()

'''for g_idx, gamma in zip(range(len(gammas)), gammas):
    for d_idx, d in zip(range(len(varying_d)), varying_d):
        amplitudes[g_idx, d_idx], phases[g_idx, d_idx], theo_amplitudes[g_idx, d_idx], theo_phases[g_idx, d_idx] = run_setup(d, gamma)
        phases[g_idx, d_idx] += np.angle(np.exp(-1j*k_0 * (obs_ind - src_ind) * dz))
'''
# loading data from computation above
amplitudes = np.load(file='./LPD_FP3/saved_data/dielectric_slab/diel_slab_gamma_variation_fdtd.npy')
theo_amplitudes = np.load(file='./LPD_FP3/saved_data/dielectric_slab/diel_slab_gamma_variation_theo.npy')

plot_results(gammas, varying_d, dz)

