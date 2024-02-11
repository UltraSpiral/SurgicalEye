from ultralytics import YOLO
import cv2
import math

model = YOLO("best.pt")
# classNames = ['0', '1', '2', '3']
classNames = ['forceps', 'forceps', 'mayo scissors', 'straight scissors']
cap = cv2.VideoCapture("exVid2.mp4")


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            #bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence: ", confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name: ", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()