#load liberaries
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

#Load images
img=cv2.imread('F:\\iti\\solidYellowCurve.jpg')

#dinoissing image
blurred= cv2.blur(img, (3,3))

#edge detection with canny
gray= cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
edges=cv2.Canny(gray,75,150)

#mask the image (get region of interset[ROI])
plt.imshow(img)
#observation from plot
points=np.array([[200,500],
           [800,500],
           [460,300]])
mask=np.zeros_like(edges)
color=[255]
cv2.fillPoly(mask, [points], color)
masked_img=cv2.bitwise_and(edges, edges,mask=mask)

#line detection using Hough  transform technique
lines=cv2.HoughLinesP(masked_img, rho=1, theta=np.pi/180,threshold=3,minLineLength=30, maxLineGap=120)



#formulate lines
#LINE DISPLAY PARAMETERS
color = [243, 105, 14]
thickness = 12
    
    #LINE PARAMETERS
SLOPE_THRESHOLD = 0.3
Y_MIN_ADJUST = 15
    
positive_slopes = []
negative_slopes = []
    
positive_intercepts = []
negative_intercepts = []
    
    #named as y_max despte being at the bottom corner of the image due to y axis in reverse direction
y_max = img.shape[0]
y_min = img.shape[0]
    
for line in lines:
    for x1,y1,x2,y2 in line:
            
            #calculate slope for the line
        slope = (y2-y1)/(x2-x1)
        intercept = y2 - (slope*x2)
            
            #for negative slope
        if slope < 0.0 and slope > -math.inf and abs(slope) > SLOPE_THRESHOLD:
                #print('negative slope')
             negative_slopes.append(slope)
             negative_intercepts.append(intercept)
                
            #for positive slope
        elif slope > 0.0 and slope < math.inf and abs(slope) > SLOPE_THRESHOLD:
                #print('positive slope')
            positive_slopes.append(slope)
                
            positive_intercepts.append(intercept)
            
        y_min = min(y_min, y1, y2)
            #cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    
y_min+=Y_MIN_ADJUST
#get averages for positive and negative slopes
positive_slope_mean = np.mean(positive_slopes)
negative_slope_mean = np.mean(negative_slopes)

#get averages for potitive and negative intercepts
positive_intercept_mean = np.mean(positive_intercepts)
negative_intercept_mean = np.mean(negative_intercepts)    

lst = [
        [[0, 0, 0, 0]],
        [[0, 0, 0, 0]]
    ]


#calculation of coordinates for lane for positive slopes
if len(positive_slopes) > 0:
    x_max = int((y_max - positive_intercept_mean)/positive_slope_mean)
    x_min = int((y_min - positive_intercept_mean)/positive_slope_mean)
        #cv2.line(img, (x_min, y_min), (x_max, y_max), color, thickness)
    lst[0][0] = [x_min, y_min, x_max, y_max]
    
    #calculation of coordinates for lane for negative slopes
if len(negative_slopes) > 0:
    x_max = int((y_max - negative_intercept_mean)/negative_slope_mean)
    x_min = int((y_min - negative_intercept_mean)/negative_slope_mean)
        #cv2.line(img, (x_min, y_min), (x_max, y_max), color, thickness)
    lst[1][0] = [x_min, y_min, x_max, y_max]
        #lst.append([x_min, y_min, y_min, y_max])
    
color = [243, 105, 14]
thickness = 12
lines_image = np.zeros((masked_img.shape[0], masked_img.shape[1], 3), dtype=np.uint8)
for line in lst:
    for x1,y1,x2,y2 in line:
        cv2.line(lines_image, (x1, y1), (x2, y2), color, thickness)

final_image = cv2.addWeighted(img, 0.8, lines_image, 1, 0)
cv2.imshow("final_image",final_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

