from ultralytics import YOLO
import cv2
import cvzone 
import math

#Create webcam object
# cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)

# For video
cap = cv2.VideoCapture("1.mp4")

model = YOLO('ppe.pt')

classNames = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery', 'mini-van', 'sedan', 'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']

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