#code: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pdb

# サイズは漸化式で求まる
# a1 = 3
# a2 = 2 * a1 - 1
# an = 2**n + 1
di = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.uint8)  # dx, dy

def update(si, nn=3, alpha=0.1):
    if nn < 1:
        return
    ss = 2 ** nn + 1
    # 中心の値を入力
    val = np.zeros(4)
    for i in range(4):
        ci = si + di[i] * (ss - 1) # y, x
        val[i] = ff[ci[1], ci[0]] # ff[y, x]
    center_val = np.mean(val) + np.random.rand() * ss * alpha
    cx = int(si[0] + 0.5 * (ss - 1)) 
    cy = int(si[1] + 0.5 * (ss - 1))
    ff[cy, cx] = center_val
    
    # 辺の中点の値を入力
    # up
    edge_val = (val[0] + val[1] +center_val) / 3 + np.random.randn() * ss * alpha
    cx = int(si[0] + 0.5 * (ss - 1)) 
    cy = int(si[1])
    if ff[cy, cx] == 0:
        ff[cy, cx] = edge_val
    # left
    edge_val = (val[0] + val[2] +center_val) / 3 + np.random.randn() * ss * alpha
    cx = int(si[0]) 
    cy = int(si[1] + 0.5 * (ss - 1))
    if ff[cy, cx] == 0:
        ff[cy, cx] = edge_val
    # right
    edge_val = (val[1] + val[3] +center_val) / 3 + np.random.randn() * ss * alpha
    cx = int(si[0] + (ss - 1)) 
    cy = int(si[1] + 0.5 * (ss - 1))
    if ff[cy, cx] == 0:
        ff[cy, cx] = edge_val
    # down
    edge_val = (val[2] + val[3] +center_val) / 3 + np.random.randn() * ss * alpha
    cx = int(si[0] + 0.5 * (ss - 1)) 
    cy = int(si[1] + (ss - 1))
    if ff[cy, cx] == 0:
        ff[cy, cx] = edge_val
    
    # 4つの領域

    for i in range(4):
        ssi = si + di[i] * (ss - 1) * 0.5
        ssi = ssi.astype(np.int)
        update(ssi, nn - 1, alpha=alpha)

# test         
from mpl_toolkits.mplot3d import Axes3D

nn = 7
ss = 2 ** nn + 1
ff = np.zeros((ss, ss))
si = np.array([0, 0], dtype=np.uint8)
update(si, nn, alpha=0.1)
fig = plt.figure(figsize=(12, 6))

ax = fig.add_subplot(1, 3, 1)
ax.imshow(ff, cmap='gist_earth')

ax2 = fig.add_subplot(1, 3, (2, 3), projection='3d')
# ax2.set_aspect('equal')
x = np.linspace(-10, 10, ss)
y = np.linspace(-10, 10, ss)
xx, yy = np.meshgrid(x, y)
ax2.plot_surface(xx, yy, ff, cmap='gist_earth')
ax2.set_zlim(-20, 20)
plt.show()
