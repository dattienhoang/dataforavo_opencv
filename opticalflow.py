# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 16:29:52 2016

@author: Dat Tien Hoang
"""
# Notes:
# For me on Windows 7 + Python:
# to use DLLs inside installation package: sources/3rdparty/ffmpeg 
# (opencv_ffmpeg.dll and opencv, _ffmpeg_64.dll)
# copy them to C:\Python27 directory and rename them accordingly to openCV version used.
# for openCV 2.4.10
#   opencv_ffmpeg2410.dll
#   opencv_ffmpeg2410_64.dll
# for openCV 3.0.0 beta
#   opencv_ffmpeg300.dll
#   opencv_ffmpeg300_64.dll
#
# Another useful resource: http://cbarker.net/opencv/

import cv2
import numpy as np

nfr = 25
sav = 1

#cap = cv2.VideoCapture(0) # the web cam
cap = cv2.VideoCapture('video_1.mov')

#if not cap.isOpened(): 
#    print "could not open :",cap
#    return
#print cap.get(CV_CAP_PROP_FRAME_COUNT)
#length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
#width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
#fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

i = 0
#while(1):
while i <= nfr-1:
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    
    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    # Create a window that displays an image, and saves the image when the 
    # 's' key is pressed.
    cv2.imshow('frame2',bgr)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',bgr)
    prvs = next
    i += 1
    
    #do some video writing if desired
    if sav == 1:
        cv2.imwrite('opticalfb_' + str(i) + '.png',frame2)
        cv2.imwrite('opticalhsv_' + str(i) + '.png',bgr)

cap.release()
#out.release()
cv2.destroyAllWindows()
