__author__ = 'zimolenr'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(True, which='both')
ax.plot([1],[1],[1],'o', markersize=50)
ax.plot([1],[2],[1],'o', markersize=50)
ax.plot([1],[1],[2],'o', markersize=50)
ax.plot([1],[2],[2],'o', markersize=50)
ax.plot([2],[1],[1],'o', markersize=50)
ax.plot([2],[2],[1],'o', markersize=50)
ax.plot([2],[1],[2],'o', markersize=50)
ax.plot([2],[2],[2],'o', markersize=50)
ax.set_title('grid on')
plt.show()


