import numpy as np
import cv2
cap = cv2.VideoCapture('ps3-9.avi')
# take first frame of the video
ret,frame = cap.read()
# setup initial location of window
drawing=False
ix=0
iy=0
h=0
w=0
def draw_rect(event,x,y,flags,param):
    global ix,iy,h,w,drawing
    if event==cv2.EVENT_LBUTTONDOWN:
        ix=x
        iy=y
        drawing=True
    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            #cv2.rectangle(frame,(ix,iy),(x,y),(255,0,0),3)
            h,w =(y-iy),(x-ix)
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.rectangle(frame,(ix,iy),(x,y),(255,0,0),2)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rect)
while(1):
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF==27:
        break
# setup initial location of window
c=ix
r=iy
#c,r,w,h=206,168,87,23
track_window = (c,r,w,h)
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array([[[30., 100.,100.]]]), np.array([[[60.,255.,255.]]]))
roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit= ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 190000)
while(cap.isOpened()):
    ret ,frame = cap.read()
    if ret==True :
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        # Draw it on image
        m,n,w,h = track_window
        img2 = cv2.rectangle(frame, (m,n), (m+w,n+h), (255,0,0),2)
        cv2.imshow('image',img2)
        k = cv2.waitKey(0) & 0xff
        if k == ord('q'):
            break
    else:
        break
cv2.destroyAllWindows()
cap.release()
