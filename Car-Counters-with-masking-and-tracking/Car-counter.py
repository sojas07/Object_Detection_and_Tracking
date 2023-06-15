from ultralytics import YOLO
import cv2
import cvzone 
import math
from sort import *

#Create webcam object
# cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)

# For video
cap = cv2.VideoCapture("pexels-german-korb-3727445-1920x1080-30fps.mp4")

model = YOLO('./Yolo-Weights/yolov8n.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus","train", "truck", "boat" ,"traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird",
"dog", "horse","sheep", "cat", "cow", "elephant", "bear", "zebra", "giraffe", "backpac","umbrella","handbag", "tie", "sultcase", "frisbee","skis", "snowboard", "sports ball", "kite", "baseball bat",
"baseball glove", "skateboard", "surfboard", "tennis racket" , "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
"sofa", "pottedplant", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "bed", "microwave", "remote", "keyboard", "cell phone" , "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
"toothbrush"]

mask = cv2.imread("mask.jpg")

# max_age = limit of number of frames it is gone and we still recognize in that region.
# for exampe if id number 20 is lossed how many frames we wait until we detect it back

tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

limits = [456,781,1488,786]
totalCount = []

while True:
    success, img = cap.read()
    imgRegion = cv2.bitwise_and(img,mask)
    results = model(imgRegion,stream=True)

    detections = np.empty((0,5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            #Bounding Box
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            w,h = x2-x1,y2-y1
            

            # Confidence
            conf = math.ceil((box.conf[0]*100))/100

            # Class Name
            clss = int(box.cls[0])
            currClass = classNames[clss]

            if currClass == 'car' and conf > 0.3:
                # cvzone.cornerRect(img,(x1,y1,w,h),l=9,rt=5)
                # cvzone.putTextRect(img,f'{classNames[clss]} {conf}',(max(0,x1),max(35,y1)),scale = 0.6, thickness=1, offset=3)
                currentArray =  np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections,currentArray))
            
    resultsTracker = tracker.update(detections)
    cv2.line(img,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),5)

    for result in resultsTracker:
        x1,y1,x2,y2,Id = result
        x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
        w,h = x2-x1,y2-y1
        cvzone.cornerRect(img,(x1,y1,w,h),l=9,rt=2,colorR=(255,0,0))
        cvzone.putTextRect(img,f'{int(Id)}',(max(0,x1),max(35,y1)),scale = 2, thickness=3, offset=10)

        cx,cy = x1+w//2, y1+h//2
        cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        if limits[0] < cx < limits[2] and limits[1] - 20 < cy < limits[1] + 20:
            if totalCount.count(Id) == 0:
                totalCount.append(Id)
            
    cvzone.putTextRect(img, f'Count: {len(totalCount)}',(50,50))


    cv2.imshow("Image",img)
    cv2.waitKey(0)