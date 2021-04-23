import LPD_FP3 as LPD
import numpy as np
import matplotlib.pyplot as plt

def guided_wavelength_to_d(wavelength, n):
    return wavelength / (4*n)

def run_setup(wavelengths, dz, grid_cells, n_l, n_h, d_l_idx, d_h_idx, number_of_pairs, timesteps=15000):
    exp_amplitudes = np.zeros(len(wavelengths))
    start_media = 5
    for wavelength, idx_loop in zip(wavelengths, range(len(wavelengths))):
        grid = LPD.Grid(dz=dz, Nz=grid_cells)
        grid[0] = LPD.LeftSideGridBoundary()
        grid[int(grid_cells)-1] = LPD.RightSideGridBoundary()
        for n in range(1, number_of_pairs + 1):
            grid[start_media:start_media+d_l_idx] = LPD.NonDispersive(name='low', permittivity=n_l ** 2)
            grid[start_media+d_l_idx: start_media+d_l_idx+d_h_idx] = LPD.NonDispersive(name='high', permittivity=n_h ** 2)
            start_media += d_l_idx + d_h_idx
        grid[2] = LPD.Ramped_Sin(wavelength=wavelength, carrier_wavelength=10*wavelength, amplitude=1)
        grid[int(grid_cells)-3] = LPD.Point_Observer(name='transmittance', first_timestep=timesteps-15)
        grid.run_timesteps(timesteps=timesteps, vis=False, ani=False)
        exp_amplitudes[idx_loop] = grid.observers[0].amplitude
        start_media = 5
    return exp_amplitudes


def plot_reflectivity(amplitude_matrix, wavelengths):
        fig, axes = plt.subplots(figsize=(6, 5))
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Times"],
        })
        axes.tick_params(direction='in', bottom=True, left=True, right=True, top=True)
        axes.grid(True, alpha=0.5, linestyle=':', color='k')
        axes.plot(wavelengths*10**9, 1 - amplitude_matrix[0]**2, linestyle='-', linewidth=0.3, marker='o', markersize=0.5, mfc='None', color='red',
                  label='2 layer pairs')
        axes.plot(wavelengths*10**9, 1 - amplitude_matrix[1]**2, linestyle='-', linewidth=0.3, marker='o', markersize=0.5, mfc='None', color='k',
                  label='10 layer pairs')
        axes.set_xlabel(r'$\lambda$'+' in nm')
        axes.set_ylabel(r'$R$')
        axes.legend(ncol=3, fancybox=False, edgecolor='k', bbox_to_anchor=(0, 1), loc=3)
        plt.show()

# parameters
dz = 1e-9
n_l = 1.453
n_h = 2.519
wavelength_guided = 800e-09
length_l = guided_wavelength_to_d(wavelength_guided, n_l)
length_h = guided_wavelength_to_d(wavelength_guided, n_h)
d_l_idx = int(np.floor(length_l / dz))
d_h_idx = int(np.floor(length_h / dz))
arr_number_of_pairs = np.array([2, 10])
grid_cells = (1 + arr_number_of_pairs)*(d_l_idx + d_h_idx)
wavelengths = np.arange(400e-09, 1204e-09, 1e-09)


# calculate
'''amplitude_matrix = np.zeros((len(arr_number_of_pairs), len(wavelengths)))

for idx in range(len(arr_number_of_pairs)):
    if idx == 0:
        amplitude_matrix[idx][:] = run_setup(wavelengths, dz, grid_cells[idx], n_l, n_h, d_l_idx, d_h_idx, arr_number_of_pairs[idx], timesteps=40000)
    else:
        amplitude_matrix[idx][:] = run_setup(wavelengths, dz, grid_cells[idx], n_l, n_h, d_l_idx, d_h_idx,
                                             arr_number_of_pairs[idx], timesteps=180000)
'''

# load data
file_name = '1em09_180000ts.npy'
amplitude_matrix = np.load('./LPD_FP3/saved_data/vary_wave_dbr/' + file_name)

plot_reflectivity(amplitude_matrix, wavelengths)

