import cv2
import numpy as np
img= cv2.imread('edge2.jpg')
rows,cols,channels=img.shape
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edge detection followed by finding the contours in the obtained result
dst=cv2.Canny(img,100,250)
img2, contours, heirarchy = cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#finding the contour of maximum area,which will provide the desired boundary of the document in most cases
c_max=max(contours,key=cv2.contourArea)
perimeter=cv2.arcLength(c_max,True)
#approximating the contour to a rectangle
a=cv2.approxPolyDP(c_max,0.1*perimeter,True)
#sorting the list to get the required boundary points in a cyclic order
a=sorted(a,key=lambda k:[k[0][1],k[0][0]])
if a[0][0][0]>a[1][0][0]:
    a[0],a[1]=swap(a[0],a[1])
if a[2][0][0]>a[3][0][0]:
    a[2],a[3]=swap(a[2],a[3])
a=np.float32(a)
print(a,type(a))
x, y, width, height = cv2.boundingRect(c_max)
pts=np.float32([[0,0],[x+width-1,0],[0,y+height-1],[x+width-1,y+height-1]])
#applying warp perspective and then thresholding
M=cv2.getPerspectiveTransform(a,pts)
res=cv2.warpPerspective(img,M,(width,height))
gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
res2=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,4)
equalize=cv2.equalizeHist(res2)
#filtering for better contrast
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
filter1 = cv2.filter2D(equalize, -1, kernel)
erode
cv2.imshow('img',img)
cv2.imshow('result',filter1)
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
