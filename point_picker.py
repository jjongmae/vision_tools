import cv2, numpy as np
from tkinter import filedialog
import tkinter as tk

def pick_points(img_path):
    img = cv2.imread(img_path)
    pts = []
    def cb(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(pts) < 4:
            pts.append((x, y))
            cv2.circle(img, (x,y), 4, (0,0,255), -1)
            cv2.imshow("pick", img)
            print(f"{len(pts)}: ({x}, {y})")
    cv2.imshow("pick", img)
    cv2.setMouseCallback("pick", cb)
    cv2.waitKey(0);  cv2.destroyAllWindows()
    return np.array(pts, np.int32)

if __name__ == "__main__":
    # tkinter 루트 윈도우 생성 (숨김)
    root = tk.Tk()
    root.withdraw()
    
    # 이미지 파일 선택 대화상자
    img_path = filedialog.askopenfilename(
        title="이미지 파일 선택",
        filetypes=[
            ("이미지 파일", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
            ("PNG 파일", "*.png"),
            ("JPEG 파일", "*.jpg *.jpeg"),
            ("모든 파일", "*.*")
        ]
    )
    
    if not img_path:
        print("파일이 선택되지 않았습니다.")
        exit()
    
    print(f"선택된 파일: {img_path}")
    pts = pick_points(img_path)
    print("선택된 점들:", pts)
    np.savetxt("points.txt", pts, fmt="%d")
    print("점들이 'points.txt'에 저장되었습니다.")