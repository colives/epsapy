import numpy as np

Ybus = np.array([[15-35*1j, -10+20*1j, -5+15*1j, 0],
                 [-10+20*1j, 30-60*1j, -20+40*1j, 0],
                 [-5+15*1j, -20+40*1j, 25-65*1j, 10*1j],
                 [0, 0, 10*1j, -10*1j]])
p = np.array([1.02, 1.02, 0, -0.60, 0.50, 0, -1.00])
pv = np.array([True, True, False, False])

tol = 1e-4
maxIter = 20
