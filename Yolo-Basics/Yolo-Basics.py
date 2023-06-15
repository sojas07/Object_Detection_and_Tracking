from ultralytics import YOLO
import cv2

model = YOLO('./Yolo-Weights/yolov8l.pt')
results = model('pexels-german-korb-3727445-1920x1080-30fps.mp4', show=True)
cv2.waitKey(0)