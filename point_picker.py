import cv2, numpy as np
from tkinter import filedialog
import tkinter as tk

def pick_points(img_path, screen_width, screen_height):
    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]

    # Calculate scaling factor to fit image to screen, with a 10% margin
    scale = min(screen_width * 0.9 / img_w, screen_height * 0.9 / img_h)
    
    # Don't scale up if the image is smaller than the screen
    if scale > 1.0:
        scale = 1.0

    resized_w = int(img_w * scale)
    resized_h = int(img_h * scale)
    
    resized_img = cv2.resize(img, (resized_w, resized_h))
    
    pts = []
    
    def cb(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Convert coordinates to original image scale
            original_x = int(x / scale)
            original_y = int(y / scale)
            pts.append((original_x, original_y))
            
            # Draw on the resized image for visual feedback
            cv2.circle(resized_img, (x, y), 4, (0, 0, 255), -1)
            cv2.imshow("pick", resized_img)
            print(f"{len(pts)}: ({original_x}, {original_y})")
            
    cv2.imshow("pick", resized_img)
    cv2.setMouseCallback("pick", cb)
    cv2.waitKey(0);  cv2.destroyAllWindows()
    
    return np.array(pts, np.int32)

if __name__ == "__main__":
    # tkinter 루트 윈도우 생성
    root = tk.Tk()
    # 스크린 크기 얻기
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.withdraw() # 메인 윈도우 숨기기
    
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
    pts = pick_points(img_path, screen_width, screen_height)
    print("선택된 점들:", pts)
    np.savetxt("points.txt", pts, fmt="%d")
    print("점들이 'points.txt'에 저장되었습니다.")
