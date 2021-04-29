import LPD_FP3 as LPD
import numpy as np
import matplotlib.pyplot as plt
from LPD_FP3.constants import c0, me, eps0, q
from LPD_FP3.utils import theory_dielectric_slab

colors = ['k', 'red', 'blue']
lamb = [160e-09, 800e-09]
N_lambda = 100
dz = lamb[0] / N_lambda
Nz = 250
src_ind = 3
obs_ind = 2
timesteps = 15000


varying_d = np.arange(2, 145, 1)
amplitudes = np.zeros((len(lamb), len(varying_d)))
phases = np.zeros((len(lamb), len(varying_d)))
theo_amplitudes = np.zeros((len(lamb), len(varying_d)))
theo_phases = np.zeros((len(lamb), len(varying_d)))

# silver_params
plasma_freq = 2*np.pi * 2.321e15
n_silver = plasma_freq ** 2 * eps0 * me / (q ** 2)
print(n_silver)
gamma_silver = 2*np.pi * 5.513e13

def run_setup(thickness_in_dz, lamb):
    s_grid = LPD.Grid(Nz=Nz, dz=dz)
    s_grid[0] = LPD.LeftSideGridBoundary()
    s_grid[Nz-1] = LPD.RightSideGridBoundary()
    s_grid[src_ind] = LPD.Ramped_Sin(amplitude=0.5, wavelength=lamb, carrier_wavelength=lamb*15, tfsf=True)
    if thickness_in_dz != 0:
        s_grid[4:thickness_in_dz+4] = LPD.DrudeMaterial(name='silver', eps_inf=1, number_density=n_silver, gamma=gamma_silver)
    s_grid[obs_ind] = LPD.Point_Observer(first_timestep=timesteps-15, name='getting reflectivity')
    s_grid.run_timesteps(timesteps=timesteps, vis=False, ani=False)
    if thickness_in_dz == 0:
        theo_ampl, theo_phase = 1, 0
    else:
        theo_ampl, theo_phase = theory_dielectric_slab(s_grid)
    return s_grid.observers[0].amplitude, s_grid.observers[0].phase, theo_ampl, theo_phase


def plot_results(lambdas, varying_d, dz):
    fig, axes = plt.subplots(figsize=(6, 5))
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Times"],
    })
    z = varying_d * dz
    axes.tick_params(direction='in', bottom=True, left=True, right=True, top=True)
    axes.grid(True, alpha=0.5, linestyle=':', color='k')
    for lambda_idx in range(len(lambdas)):
            axes.plot(z, amplitudes[lambda_idx, :] ** 2, markersize=3, color=colors[lambda_idx], marker='o', mfc='None', ls='None', label=r'$\lambda$='+'${:.2E}$'.format(lambdas[lambda_idx]))
    axes.set_xlabel('$z$ in m')
    axes.set_ylabel('$R$')
    axes.legend(ncol=1, fancybox=False, edgecolor='k', bbox_to_anchor=(0.5, 0.1), loc=3)
    plt.show()


for lamb_idx, s_lamb in zip(range(len(lamb)), lamb):
    for d_idx, d in zip(range(len(varying_d)), varying_d):
        amplitudes[lamb_idx, d_idx], phases[lamb_idx, d_idx], theo_amplitudes[lamb_idx, d_idx], theo_phases[lamb_idx, d_idx] = run_setup(d, s_lamb)

plot_results(lamb, varying_d, dz)