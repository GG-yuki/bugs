import numpy as np

import matplotlib.pyplot as plt

X = np.linspace(0, 10,150)
plt.plot(X, (X/np.exp(X)))
plt.show()
