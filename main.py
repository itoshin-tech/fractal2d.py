# code:utf-8
import sys
import cv2
import numpy as np 
import fractal2d


WIN_W = 640
WIN_H = 480
X_MIN = -2
X_MAX = 2
Y_W = (X_MAX - X_MIN) / WIN_W * WIN_H
Y_MIN = -Y_W / 2
Y_MAX = Y_W / 2
U_MIN = 0
U_MAX = WIN_W
V_MIN = 0
V_MAX = WIN_H
Z_SCR = 2

def x2u(x):
    a = (U_MAX - U_MIN) / (X_MAX - X_MIN)
    b = U_MIN - a * X_MIN
    return a * x + b

def y2v(y):
    a = (V_MAX - V_MIN) / (Y_MIN - Y_MAX)
    b = V_MIN - a * Y_MAX
    return a * y + b

def xyz2xy(x, y, z):
    xx = Z_SCR / z * x
    yy = Z_SCR / z * y
    return xx, yy

def xyz2uv(x, y, z):
    xx, yy = xyz2xy(x, y, z)
    u = x2u(xx)
    v = y2v(yy)
    return u, v, z

def rotpos(pos, rot):
    """
    rotate pos

    parameters
    ----------
    pos: 3 x n ndarray
    rot: 3d ndarray
        [rx, ry, rz]

    Returns
    -------
    pos1: 3 x n ndarray
    """
    rot = rot / 180 * np.pi
    rx, ry, rz = rot

    rotx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])
    roty = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])
    rotz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])
    pos1 = rotz @ roty @ rotx @ pos
    return pos1

def pos2uv_bycam(pos_obj, pos_cam, rot_cam):
    """
    transrate pos to uv
    considering camera pos and camera rotation

    Parameters
    ----------
    pos_obj: 3 x n ndarray
    pos_cam: 3d ndarray
        [x, y, z]
    rot_cam: 3d ndarray
        [rx, ry, rz]

    Returns
    -------
    uv: 2 x n ndarray
    """
    # camera rotation
    pos_obj1 = pos_obj - pos_cam.reshape(3, 1) @ np.ones((1, pos_obj.shape[1]))
    pos_obj2 = rotpos(pos_obj1, rot_cam)
    uu, vv, zz = xyz2uv(pos_obj2[0, :], pos_obj2[1, :], pos_obj2[2, :])
    uu = uu.astype(int)
    vv = vv.astype(int)
    zz = zz.astype(int)
    return uu, vv, zz

def drawTerrain(uu, vv, zz, ffs):
    img = np.zeros((V_MAX, U_MAX, 3), dtype=np.uint8)
    # for i in range(ss - 1):
    for i in range(ss - 2, -1, -1):
        for j in range(ss - 1):
            minffs = max(ffs[i, j], ffs[i, j + 1], ffs[i + 1, j])
            minzz = min(zz[i, j], zz[i, j + 1], zz[i + 1, j])
            if minzz > Z_SCR:
                if minffs <=0:
                    col = (255, 100, 100)
                elif ffs[i, j] > height * 1.5:
                    col = (255, 255, 255)
                elif ffs[i, j] > height * 0.7:
                    col = (200, 200, 210)
                else:
                    col = (0, 255, 0)
                
                if j < ss - 2:
                    cv2.line(img, (uu[i, j], vv[i, j]), (uu[i, j + 1], vv[i, j + 1]), col, 1)
                if i < ss - 2:
                    cv2.line(img, (uu[i, j], vv[i, j]), (uu[i + 1, j], vv[i + 1, j]), col, 1)
    return img

if __name__ == '__main__':

    size_level = 6
    height = 2
    seed = None

    frac= fractal2d.Fractal2d()
    ss = 2 ** size_level + 1
    xs = np.linspace(-10, 10, ss)
    zs = np.linspace(-10, 10, ss)
    xxs, zzs = np.meshgrid(xs, zs)
    xxs = xxs.reshape(-1)
    zzs = zzs.reshape(-1)
    nn = ss * ss

    # px, py, pz = 0, 8.0, -9.2
    # rx, ry, rz = -59, 0, 0
    px, py, pz = 0, 3.4, -9.2
    rx, ry, rz = -11, 0, 0
    pv = 0.2
    rv = 2

    TT = ss
    while True:
        # make terrain
        ffs = frac.generate(size_level, height, pbc='x', seed=seed)
        # make sea
        ffs[np.where(ffs < 0)] = 0

        for tt in range(TT):
            # scroll
            ffs2 = ffs.copy()
            ffs[0:ss-1, :] = ffs2[1:ss, :]
            ffs[ss-1, :] = ffs2[0, :]
            yys = ffs.reshape(-1)

            # get uv from ff
            pos_cam = np.array([px, py, pz])
            rot_cam = np.array([rx, ry, rz])
            pos_obj = np.zeros((3, nn))
            pos_obj[0, :] = xxs
            pos_obj[1, :] = yys
            pos_obj[2, :] = zzs
            uu, vv, zz = pos2uv_bycam(pos_obj, pos_cam, rot_cam)

            # draw terrain
            uu = uu.reshape((ss, -1))
            vv = vv.reshape((ss, -1))
            zz = zz.reshape((ss, -1))
            img = drawTerrain(uu, vv, zz, ffs)

            # show and contrall
            cv2.imshow('img', img)
            INPUT = cv2.waitKey(10) & 0xFF
            if INPUT == ord('q'):
                sys.exit()
            if INPUT == ord('e'):
                pz += pv
            if INPUT == ord('d'):
                pz -= pv
            if INPUT == ord('f'):
                px += pv
            if INPUT == ord('s'):
                px -= pv
            if INPUT == ord('r'):
                py += pv
            if INPUT == ord('v'):
                py -= pv

            if INPUT == ord('i'):
                rx += rv
            if INPUT == ord('k'):
                rx -= rv
            if INPUT == ord('j'):
                ry += rv
            if INPUT == ord('l'):
                ry -= rv
            if INPUT == ord(' '):
                print(px, py, pz, rx, ry, rz)







    


