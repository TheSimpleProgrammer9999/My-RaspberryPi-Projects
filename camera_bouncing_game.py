import cv2
from picamera2 import Picamera2
import time

dispW = 672
dispH = 520
score = 0

picam = Picamera2()
picam.preview_configuration.main.size = (dispW, dispH)
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.controls.FrameRate = 60
picam.preview_configuration.align()
picam.configure("preview")
picam.start()
fps = 0
pos = (5, 40)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 1.5
myColor = (0, 255, 0)
weight = 2

boxW, boxH = 150, 100
tlC = 50
tlR = 74
lrC = tlC + boxW
lrR = tlR + boxH

deltaC, deltaR = 2, 2
thickness = -1
Rcolor = (0, 100, 0)

while True:
    tstart = time.time()
    frame = picam.capture_array()
    cv2.putText(frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)
    if tlC + deltaC < 0 or lrC + deltaC > dispW - 1:
        deltaC = deltaC * (-1)
    if tlR + deltaR < 0:
        deltaR = deltaR * (-1)
    if lrR + deltaR > dispH - 1:
        score += 1
        deltaR = deltaR * (-1)
        
    tlC = tlC + deltaC
    tlR = tlR + deltaR
    lrC = lrC + deltaC
    lrR = lrR + deltaR
    cv2.rectangle(frame, (tlC, tlR), (lrC, lrR), Rcolor, thickness)
    cv2.rectangle(frame, (0, 500), (672, 515), (0, 255, 245), 5)
    cv2.putText(frame, 'Score: ' + str(int(score)), (300, 40), font, height, (255, 0, 0), weight)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    tEnd = time.time()
    looptime = tEnd - tstart
    fps = 1/looptime
    
    
cv2.destroyAllWindows()
