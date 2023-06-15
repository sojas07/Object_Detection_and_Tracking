from ultralytics import YOLO
import cv2
import cvzone 
import math

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

print(len(classNames))

while True:
    success, img = cap.read()
    results = model(img,stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            #Bounding Box
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            w,h = x2-x1,y2-y1
            cvzone.cornerRect(img,(x1,y1,w,h))

            # Confidence
            conf = math.ceil((box.conf[0]*100))/100

            # Class Name
            clss = int(box.cls[0])
            cvzone.putTextRect(img,f'{classNames[clss]} {conf}',(max(0,x1),max(35,y1)))


    cv2.imshow("Image",img)
    cv2.waitKey(1)