import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

dt_freq = np.array([10, 20, 25, 30, 40, 50, 60, 73, 80, 90, 112, 139, 236, 300, 400, 600, 800, 1300, 1500, 2000, 3000, 3500, 4000, 6000, 8000, 10000, 12500, 16400, 18600, 22050])
dt_db = np.array([6, 9, 9.5, 10.5, 11, 10.8, 9, 5, 6.2, 10, 8.6, 11, 2.5, 4, 4.5, 4, 3, 3.3, 3, 5.7, 1.5, 1.8, 1, 11.2, 6.3, 10, 11.5, 1.4, 1, 1.6])

dt_spline = make_interp_spline(dt_freq, dt_db)

dt_freq_ = np.linspace(1, 22050, 22050)
dt_db_ = dt_spline(dt_freq_)

dt_matrix = np.array([dt_freq_, dt_db_])

spm_freq = np.array([20, 25, 30, 40, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 10000, 12000, 15000, 17000, 20000])
spm_db = np.array([-4.5, -6.5, -7.5, -9, -9, -8, -8, -7, -6, -4.5, -3, -2, 0, 0, -0.5, -1.5, -4.5, -3, 1, 0, -6, -7, -5, -7, -14, -5, -6, -3, -4, 2])

spm_spline = make_interp_spline(spm_freq, spm_db)

spm_freq_ = np.linspace(1, 22050, 22050)
spm_db_ = spm_spline(spm_freq_)

spm_matrix = np.array([spm_freq_, spm_db_])

edit = spm_db_ + dt_db_

matrix = [spm_freq_.tolist(), edit.tolist()]

default_freq = [20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

dict_f = {}

for x, y in zip(matrix[0], matrix[1]):
    if x in default_freq:
        dict_f[x] = round(y, 1)