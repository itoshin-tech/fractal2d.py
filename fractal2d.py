#code: utf-8
import numpy as np

# 山の生成クラス
class Fractal2d:
    """
    領域サイズは漸化式の関係から 2**nn + 1 と導ける
    nn は自然数でサイズレベルと呼ぶことにする
    """

    def __init__(self):
        # 左上を基準として、左上、右上、左下、右下の方向ベクトルを定義
        self.DI = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.uint8)  # dx, dy
    
    def generate(self, nn=5, height=5):
        # サイズ
        ss = 2 ** nn + 1 
        self.size = ss

        # フィールド
        self.ff = np.zeros((ss, ss))

        # 基準座標
        si = np.array([0, 0], dtype=np.uint8)

        # フラクタル生成
        self._fractal(si, nn, height=height)
        return self.ff

    def _fractal(self, si, nn=3, height=0.1):
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
            ci = si + self.DI[i] * (ss - 1) # y, x
            val[i] = self.ff[ci[1], ci[0]] # self.ff[y, x]
        center_val = np.mean(val) + np.random.rand() * ss / self.size * height
        cx = int(si[0] + 0.5 * (ss - 1)) 
        cy = int(si[1] + 0.5 * (ss - 1))
        self.ff[cy, cx] = center_val
        
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
            edge_val = (val[p0[i]] + val[p1[i]] +center_val) / 3 + np.random.randn() * ss / self.size * height
            if self.ff[cy, cx] == 0:
                self.ff[cy, cx] = edge_val
        
        # 4つの小領域（左上、右上、左下、右下）で山を生成
        for i in range(4):
            ssi = si + self.DI[i] * (ss - 1) * 0.5
            ssi = ssi.astype(np.int)
            self._fractal(ssi, nn - 1, height=height)

# ------- main 

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    ft = Fractal2d()
    size_level = 6
    height = 5
    ff = ft.generate(size_level, height=height)
    ss = ff.shape[0]

    # 描画
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 4, 1)
    ax.imshow(ff, cmap='gist_earth')
    ax.set_title('size = %d x %d' % (ss, ss))

    ax2 = fig.add_subplot(1, 4, (2, 4), projection='3d')
    x = np.linspace(-10, 10, ss)
    y = np.linspace(-10, 10, ss)
    xx, yy = np.meshgrid(x, y)
    ax2.plot_surface(xx, yy, ff, cmap='gist_earth')
    ax2.set_zlim(-20, 20)
    ax2.set_ylim(10, -10)
    ax2.view_init(40 ,-80)
    ax2.axis("off")
    ax.set_title('size = %d x %d, H=%.1f' % (ss, ss, height))
    plt.show()
