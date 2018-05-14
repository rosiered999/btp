import cv2
import numpy as np
import sys
from scipy import ndimage
import imutils
import matplotlib.pyplot as plt
NUM = 1
#https://stackoverflow.com/questions/46282691/opencv-cropping-handwritten-lines-line-segmentation
def findConts(filename,kern):
    image = cv2.imread(filename)
    global NUM
    NUM = 0
    if image==None:
        print "ERROR"
        return
    #cv2.imshow('orig',image)
    #cv2.waitKey(0)
    file_list = []
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    #cv2.waitKey(0)

    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('second',thresh)
    #cv2.waitKey(0)

    #dilation
    kernel = np.ones(kern, np.uint8) #145
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    cv2.imshow('dilated'+filename,img_dilation)
    cv2.waitKey(0)

    #find contours
    im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    roi_list = []
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    print filename
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        if h<20:
            continue
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        roi_list.append(roi)
        # show ROI
        print "h",h,"w",w
        name = "roi_"+str(NUM)+str(i)+filename
        NUM += 1
        file_list.append(name)
        #roi_temp = imutils.rotate_bound(roi,90)
        cv2.imwrite(name,roi)#_temp)
        #cv2.imshow('segment no:'+str(i),roi)
        cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        cv2.waitKey(0)

    cv2.imshow('marked areas '+filename,image)
    cv2.waitKey(0)
    return file_list

if __name__=='__main__':
    NUM = 0
    filename = sys.argv[1]
    print filename
    file_list = findConts(filename, (5,145))
    k = []
    for i in file_list:
        print "in loop"
        s = findConts(i,(5,5))
        k.append(s)
