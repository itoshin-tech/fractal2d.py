# fractal2d.py

フラクタル構造を持った地形を自動生成します。

# DEMO　

1辺が、$2^n + 1$ ($n$は自然数)となる大きさの2次元配列を生成します。要素は高さに対応します。

size 17x17, H=10.0 Seed=2 で生成した場合

![1](./img/04_10_2.png)


size 65x65, H=10.0 Seed=2 で生成した場合
![2](./img/06_10_2.png)


size 513x513, H=10.0 Seed=2 で生成した場合
![3](./img/09_10_2.png)

自己相似の性質があるので、配列サイズを大きくしても似たような地形となります。


# Requirement

* numpy
* matplotlib (デモ表示用)


# Usage

クローン後、ターミナルから、

```bash
$ python fractal2d.py
```

または、ターミナルから、
```bash
$ python fractal2d.py 5 10 1 # [size_level] [height] [seed]
```

または、pythonのコードで、
```python
import fractal2d 

size_level = 5 # 自然数 size = size_level**2 + 1 となる
height = 10.0 # 正の実数

ft = fractal2d.Fractal2d()
ff = ft.generate(size_level, height=height)
ss = ff.shape[0]

```


# Note

size_level は大きくすると処理が重くなるので、
7ぐらいからは1ずつ増やして試した方がよいです。

# Author

* まこっちノート
* itoshin3141592@gmail.com

