import numpy as np
import cv2
cap=cv2.VideoCapture('test2.avi')
while(1):
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, mask_white=cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
    low=np.uint8([[[0,230,220]]])
    up=np.uint8([[[20,230,220]]])
    mask_red=cv2.add(cv2.inRange(frame,low,up))
    # Load two images
    img1=mask_white
    img2 = mask_red
    rows,cols= img2.shape
    roi = frame[0:rows, 0:cols ]
    mask_inv = cv2.bitwise_not(img2)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    img2_fg = img2
    dst = cv2.add(img1_bg,img2_fg)
    img1[0:rows, 0:cols ] = dst
    cv2.imshow('frame',frame)
    cv2.imshow('res',dst)
    cv2.imshow('mask',mask_red)
    k=cv2.waitKey(0) & 0xFF
    if k==ord('q'):
        break
cv2.destroyAllWindows()
