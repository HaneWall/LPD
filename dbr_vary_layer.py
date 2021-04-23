import LPD_FP3 as LPD
import numpy as np
import matplotlib.pyplot as plt

def guided_wavelength_to_d(wavelength, n):
    return wavelength / (4*n)

def theory_reflectivity(number_of_pairs, n_l, n_h):
    a = ( n_l ** (2*number_of_pairs) - n_h ** (2*number_of_pairs) )**2
    b = ( n_l ** (2*number_of_pairs) + n_h ** (2*number_of_pairs) )**2
    return a / b


def plot_reflectivity(amplitudes, arr_pairs, n_l, n_h):
    x = np.linspace(0, arr_pairs[-1], 100)
    theory_refl = [theory_reflectivity(elem, n_l, n_h) for elem in x]
    fig, axes = plt.subplots(figsize=(6, 5))
    plt.rcParams.update({
                "text.usetex": True,
                "font.family": "serif",
                "font.serif": ["Times"],
            })
    axes.tick_params(direction='in', bottom=True, left=True, right=True, top=True)
    axes.grid(True, alpha=0.5, linestyle=':', color='k')
    axes.set_xticks(arr_pairs[::2])
    axes.plot(x, theory_refl, linestyle='-', color='k',
                    label=r'Theory of reflectivity')
    axes.plot(arr_pairs, amplitudes, linestyle='None', marker='o', mfc='None', color='blue',
                    label=r'Reflectivity over layer pairs')
    axes.set_xlabel('Layer pairs')
    axes.set_ylabel(r'$R$')
    axes.legend(ncol=2, fancybox=False, edgecolor='k', bbox_to_anchor=(0, 1), loc=3)
    plt.show()


def run_setup(wavelength, dz, grid_cells, n_l, n_h, d_l_idx, d_h_idx, number_of_pairs, timesteps=15000):
    start_media = 5
    grid = LPD.Grid(dz=dz, Nz=grid_cells)
    grid[0] = LPD.LeftSideGridBoundary()
    grid[int(grid_cells)-1] = LPD.RightSideGridBoundary()
    if number_of_pairs != 0:
        for n in range(1, number_of_pairs + 1):
            grid[start_media:start_media+d_l_idx] = LPD.NonDispersive(name='low', permittivity=n_l ** 2)
            grid[start_media+d_l_idx: start_media+d_l_idx+d_h_idx] = LPD.NonDispersive(name='high', permittivity=n_h ** 2)
            start_media += d_l_idx + d_h_idx
    grid[3] = LPD.Ramped_Sin(wavelength=wavelength, carrier_wavelength=10*wavelength, amplitude=1)
    grid[int(grid_cells)-3] = LPD.Point_Observer(name='transmittance', first_timestep=timesteps-15)
    grid.run_timesteps(timesteps=timesteps, vis=False, ani=False)
    exp_amplitudes = grid.observers[0].amplitude
    return exp_amplitudes


# parameter
dz = 1e-9
n_l = 1.453
n_h = 2.519
wavelength_guided = 800e-09
length_l = guided_wavelength_to_d(wavelength_guided, n_l)
length_h = guided_wavelength_to_d(wavelength_guided, n_h)
d_l_idx = int(np.floor(length_l / dz))
d_h_idx = int(np.floor(length_h / dz))
arr_number_of_pairs = np.arange(0, 21, 1)
grid_cells = (1 + arr_number_of_pairs)*(d_l_idx + d_h_idx)
print(grid_cells)
timesteps = 300000


amplitudes = np.load(file='./LPD_FP3/saved_data/vary_layers_dbr/1em9.npy')
'''amplitudes = np.zeros(len(arr_number_of_pairs))
for number_of_pair, idx in zip(arr_number_of_pairs, range(len(arr_number_of_pairs))):
    amplitudes[idx] = run_setup(wavelength_guided, dz, grid_cells[idx], n_l, n_h, d_l_idx, d_h_idx,
                                number_of_pair, timesteps=timesteps)

amplitudes = 1 - amplitudes ** 2'''

plot_reflectivity(amplitudes, arr_number_of_pairs, n_l, n_h)


