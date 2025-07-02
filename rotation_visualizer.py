import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math


def get_rotation_matrix(pitch, roll, yaw):
    """ pitch (x축), roll (z축), yaw (y축) 순서로 회전 행렬 생성 """
    rx = math.radians(pitch)
    ry = math.radians(yaw)
    rz = math.radians(roll)

    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)

    Rx = np.array([[1, 0, 0],
                   [0, cx, -sx],
                   [0, sx, cx]])

    Ry = np.array([[cy, 0, sy],
                   [0, 1, 0],
                   [-sy, 0, cy]])

    Rz = np.array([[cz, -sz, 0],
                   [sz, cz, 0],
                   [0, 0, 1]])

    return Rz @ Ry @ Rx


def draw_rotation(pitch, roll, yaw):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 원래 축 (빨-파-초)
    origin = np.zeros((3,))
    axes = np.eye(3)

    # 회전 후 축
    R = get_rotation_matrix(pitch, roll, yaw)
    rotated_axes = R @ axes

    colors = ['r', 'g', 'b']
    labels = ['X', 'Y', 'Z']

    for i in range(3):
        ax.quiver(*origin, *axes[:, i], color=colors[i], linewidth=2, label=f'{labels[i]} (original)')
        ax.quiver(*origin, *rotated_axes[:, i], color=colors[i], linestyle='dashed', label=f'{labels[i]} (rotated)', alpha=0.5)

    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Rotation: Pitch={pitch}°, Roll={roll}°, Yaw={yaw}°')
    ax.legend()
    plt.tight_layout()
    plt.show()


# 테스트: pitch=30°, roll=0°, yaw=90°
draw_rotation(pitch=0, roll=0, yaw=-180)
