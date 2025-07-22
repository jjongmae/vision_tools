import cv2
import numpy as np
from PIL import Image
from pathlib import Path

# ───── 설정부 ───── #
INPUT_PATH  = "image/1.jpg"              # 처리할 입력 이미지 경로
OUTPUT_PATH = "debris_extracted.png"     # 저장할 출력 PNG 경로

# 마스크 생성에 필요한 파라미터 (하드코딩)
THRESH       = 120       # 밝기 임계값 (낮을수록 어두운 부분만 남김)
MORPH_OPEN_K = 3         # 노이즈 제거용 커널 크기 (Morphology Open)
DILATE_ITER  = 1         # 마스크 팽창 반복 횟수 (구멍 메우기용)
BLUR_K       = 5         # 블러 적용 커널 크기 (가장자리를 부드럽게)
USE_HSV      = False     # True면 HSV 색 공간 기반 분리 사용

# ───── 마스크 생성 함수 ───── #
def build_mask(img_bgr):
    """
    입력: 원본 BGR 이미지
    출력: 파편만 남기고 배경은 제거한 마스크 (0=투명, 255=보임)
    """

    if USE_HSV:
        # ① HSV 색 공간으로 변환 (색상 분리 기준으로 사용 가능할 때)
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        # ② 밝고 회색에 가까운 도로 배경 추정 범위 정의
        bg_lower = np.array([0, 0, 80],  dtype=np.uint8)     # H=전체, S=낮음, V=밝음
        bg_upper = np.array([180, 60, 255], dtype=np.uint8)

        # ③ inRange로 도로 배경만 마스크로 추출 (255=배경, 0=나머지)
        bg_mask = cv2.inRange(hsv, bg_lower, bg_upper)

        # ④ 배경 마스크를 반전 → 파편 부분만 255 (보이고), 배경은 0 (투명)
        mask = cv2.bitwise_not(bg_mask)

    else:
        # ① BGR을 흑백(Grayscale)으로 변환 → 밝기 기반 분리
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # ② 임계값(THRESH) 기반 이진화 → 배경 제거
        # 밝은 도로는 0 (투명), 어두운 파편은 255 (보이게)
        _, mask = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY_INV)

    # ───── 후처리: 마스크 다듬기 ───── #

    if MORPH_OPEN_K > 1:
        # 작은 노이즈 제거 (열림 연산: 침식 후 팽창)
        k = np.ones((MORPH_OPEN_K, MORPH_OPEN_K), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)

    if DILATE_ITER > 0:
        # 팽창 연산으로 경계 확장 (구멍 메우기, 약한 연결 부위 붙이기)
        k = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, k, iterations=DILATE_ITER)

    if BLUR_K > 0 and BLUR_K % 2 == 1:
        # 가장자리를 부드럽게 처리 (자연스러운 알파 전환)
        mask = cv2.GaussianBlur(mask, (BLUR_K, BLUR_K), 0)

    return mask  # 최종 마스크 반환 (0=투명, 255=보임)

# ───── RGBA 저장 함수 ───── #
def save_rgba(img_bgr, mask, out_path):
    """
    BGR 이미지와 알파 마스크를 합쳐 RGBA 이미지로 저장
    """
    b, g, r = cv2.split(img_bgr)               # B, G, R 채널 분리
    rgba = cv2.merge((b, g, r, mask))          # 알파 채널을 마지막에 붙여서 RGBA 생성
    Image.fromarray(rgba).save(out_path)       # PIL을 사용해서 PNG로 저장 (OpenCV보다 안정적)

# ───── 메인 실행 블록 ───── #
if __name__ == "__main__":
    # 이미지 읽기 (컬러 모드)
    img = cv2.imread(INPUT_PATH, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"이미지를 읽을 수 없습니다: {INPUT_PATH}")

    # 마스크 생성 (배경 제거용)
    mask = build_mask(img)

    # RGBA 이미지로 저장
    save_rgba(img, mask, OUTPUT_PATH)

    print(f"완료: {OUTPUT_PATH}")

    # (선택) 마스크 결과 미리보기
    cv2.imshow("mask", mask)
    cv2.waitKey(0)
