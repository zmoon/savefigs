"""
Sample script that creates figure(s) but doesn't save them.
"""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

x = np.arange(11)
y = x**2

ax.plot(x, y, "o-")

ax.set(xlabel="$x$", ylabel="$y$")

fig.tight_layout()
