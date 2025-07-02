import numpy as np
import cv2

# — 사용자 입력 부분 — 
# 각도를 degree 로 입력하세요.
yaw_deg   = float(input("Yaw (degrees): "))     # Y축 회전
pitch_deg = float(input("Pitch (degrees): "))   # X축 회전
roll_deg  = float(input("Roll (degrees): "))    # Z축 회전

# 라디안으로 변환
yaw   = np.deg2rad(yaw_deg)
pitch = np.deg2rad(pitch_deg)
roll  = np.deg2rad(roll_deg)

# — 1) 카메라 기준 순수 회전행렬 R_cv 생성 (roll→pitch→yaw 순서) —
R_roll = np.array([
    [ np.cos(roll), -np.sin(roll), 0],
    [ np.sin(roll),  np.cos(roll), 0],
    [           0,             0, 1]
])
R_pitch = np.array([
    [1,            0,             0],
    [0, np.cos(pitch), -np.sin(pitch)],
    [0, np.sin(pitch),  np.cos(pitch)]
])
R_yaw = np.array([
    [ np.cos(yaw),  0, np.sin(yaw)],
    [           0,  1,          0],
    [-np.sin(yaw),  0, np.cos(yaw)]
])
# OpenCV 관례에 맞춰 순서: roll → pitch → yaw
R_cv = R_yaw @ R_pitch @ R_roll

# — 2) 월드→카메라 기저 재배열 행렬 B 정의 —
B = np.array([
    [1,  0,  0],   # 동 → 오른쪽
    [0,  0, -1],   # 위 → 아래
    [0,  1,  0]    # 북 → 정면
], dtype=np.float64)

# — 3) 최종 변환행렬 계산 —
R_world2cam = R_cv @ B           # 월드 → 카메라
R_cam2world = R_world2cam.T      # 카메라 → 월드 (전치)

# — 결과 출력 —
print("\n--- 결과 ---")
print(f"입력 각 (deg): yaw={yaw_deg}, pitch={pitch_deg}, roll={roll_deg}\n")
print("R_cv (순수 회전행렬) =\n", R_cv, "\n")
print("R_world2cam (월드→카메라) =\n", R_world2cam, "\n")
print("R_cam2world (카메라→월드) =\n", R_cam2world)
