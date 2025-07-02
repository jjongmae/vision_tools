import cv2, numpy as np

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
    img_path = "D:\\temp\\123.png"
    pts = pick_points(img_path)
    print("선택된 점들:", pts)
    np.savetxt("points.txt", pts, fmt="%d")
    print("점들이 'points.txt'에 저장되었습니다.")