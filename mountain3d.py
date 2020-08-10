#code: utf-8
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 領域サイズは漸化式の関係から 2**nn + 1 と導ける
# nn は自然数でサイズレベルと呼ぶことにする

# 左上を基準として、左上、右上、左下、右下の方向ベクトルを定義
di = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.uint8)  # dx, dy

# 山の生成関数
def mountain(si, nn=3, alpha=0.1):
    """
    si: 生成する領域の左上の座標
    nn: 生成するサイズレベル (サイズは 2**nn + 1)
    """

    # サイズレベルが1未満なら何もしない
    if nn < 1:
        return

    # 生成する領域サイズ
    ss = 2 ** nn + 1

    # 中心の値を代入、領域の4隅の値の平均＋noise
    val = np.zeros(4)
    for i in range(4):
        ci = si + di[i] * (ss - 1) # y, x
        val[i] = ff[ci[1], ci[0]] # ff[y, x]
    center_val = np.mean(val) + np.random.rand() * ss * alpha
    cx = int(si[0] + 0.5 * (ss - 1)) 
    cy = int(si[1] + 0.5 * (ss - 1))
    ff[cy, cx] = center_val
    
    # ４辺の中点の値を代入、隣接の2隅と中央の値の平均+noise
    p0 = [0, 0, 1, 2]
    p1 = [1, 2, 3, 3]
    m0 = [0.5, 0, 1, 0.5]
    m1 = [0, 0.5, 0.5, 1]
    for i in range(4):
        # 中点の座標
        cx = int(si[0] + m0[i] * (ss - 1)) 
        cy = int(si[1] + m1[i] * (ss - 1))
        # 代入する値は対応する両端と中心の値+noise
        edge_val = (val[p0[i]] + val[p1[i]] +center_val) / 3 + np.random.randn() * ss * alpha
        if ff[cy, cx] == 0:
            ff[cy, cx] = edge_val
    
    # 4つの小領域（左上、右上、左下、右下）で山を生成
    for i in range(4):
        ssi = si + di[i] * (ss - 1) * 0.5
        ssi = ssi.astype(np.int)
        mountain(ssi, nn - 1, alpha=alpha)

# ------- main 

# サイズ
nn = 6
ss = 2 ** nn + 1 

# フィールド
ff = np.zeros((ss, ss))

# 基準座標
si = np.array([0, 0], dtype=np.uint8)

# 山の生成
mountain(si, nn, alpha=0.15)

# 描画
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 4, 1)
ax.imshow(ff, cmap='gist_earth')
ax2 = fig.add_subplot(1, 4, (2, 4), projection='3d')
x = np.linspace(-10, 10, ss)
y = np.linspace(-10, 10, ss)
xx, yy = np.meshgrid(x, y)
ax2.plot_surface(xx, yy, ff, cmap='gist_earth')
ax2.set_zlim(-20, 20)
ax2.set_ylim(10, -10)
ax2.view_init(40 ,-80)
ax2.axis("off")
plt.show()
