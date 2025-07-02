import cv2, sys

cap = cv2.VideoCapture("D:\data\여주시험도로_20250610\카메라1_202506101340.mp4", cv2.CAP_FFMPEG)
prev_idx, lost_total = -1, 0

while True:
    ok, _ = cap.read()
    if not ok:
        break

    idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1  # 현재 프레임 번호(0-base)
    print(f"프레임 {idx} 읽음")

    pos_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
    print(f"현재 재생 시간: {pos_msec:.2f} ms")

    if prev_idx >= 0 and idx - prev_idx != 1:
        lost = idx - prev_idx - 1
        lost_total += lost
        print(f"🔻 DROP {lost}장 → {prev_idx}→{idx-1}")

    prev_idx = idx

cap.release()
print("=== 요약 ===")
print("누락 프레임:", lost_total)
