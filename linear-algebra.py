import numpy as np
def matrix_perspective_left_hand(fovy, aspect_ratio, near_z, far_z):
    ys = 1 / math.tan(fovy / 2)
    xs = ys / aspect_ratio
    zs = far_z / (near_z - far_z)
    return np.array([
        [xs, 0, 0, 0],
        [0, ys, 0, 0],
        [0, 0, -zs, zs * near_z],
        [0, 0, 1, 0]
    ])

# 사용 예시
fovy = np.radians(60)  # 시야각 (라디안으로 변환)
aspect_ratio = 1  # 가로 세로 비율
near_z = 0.1  # 가까운 평면
far_z = 1000  # 먼 평면

proj_matrix = matrix_perspective_left_hand(fovy, aspect_ratio, near_z, far_z)
print(proj_matrix)