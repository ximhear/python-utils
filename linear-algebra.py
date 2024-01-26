import numpy as np
from scipy.spatial.transform import Rotation as R
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

def matrix4x4_rotation(radians, axis):
    axis = axis / np.linalg.norm(axis)  # 정규화
    ct = np.cos(radians)
    st = np.sin(radians)
    ci = 1 - ct
    x, y, z = axis

    # 회전 행렬 생성
    rotation_matrix = np.array([[ct + x * x * ci, y * x * ci + z * st, z * x * ci - y * st, 0],
                                [x * y * ci - z * st, ct + y * y * ci, z * y * ci + x * st, 0],
                                [x * z * ci + y * st, y * z * ci - x * st, ct + z * z * ci, 0],
                                [0, 0, 0, 1]]).T
    return rotation_matrix


def make_quaternion_rotation_matrix(radians, axis):
    # 축 정규화
    axis = axis / np.linalg.norm(axis)

    # 쿼터니언 생성
    rotation = R.from_rotvec(radians * axis)

    # 쿼터니언을 4x4 회전 행렬로 변환
    rotation_matrix = rotation.as_matrix()

    # 3x3 행렬을 4x4 행렬로 확장
    rotation_matrix_4x4 = np.eye(4)
    rotation_matrix_4x4[:3, :3] = rotation_matrix

    return rotation_matrix_4x4

def apply_projection_matrix(point, matrix):
    x, y, z = point
    point_4d = np.array([x, y, z, 1])  # 3D 점을 4D로 변환 (동차 좌표)
    projected_point = matrix @ point_4d
    return (projected_point, projected_point[:3] / projected_point[3])  # 원근 나눗셈

# 사용 예시
fovy = np.radians(60)  # 시야각 (라디안으로 변환)
aspect_ratio = 1  # 가로 세로 비율
near_z = 0.1  # 가까운 평면
far_z = 1000  # 먼 평면

proj_matrix = matrix_perspective_left_hand(fovy, aspect_ratio, near_z, far_z)
print(proj_matrix)