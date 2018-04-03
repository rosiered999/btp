import cv2
import os, os.path
import sys
from numpy import *
from matplotlib import *
from pylab import *
import py_stringmatching

def image_similarity(A, B, alpha, beta):
    #each feature is a pixel
    # intersection PRODUCT, union MAXIMUM, and subtraction DIFFERENCE operations are
    #defined as the product, maximum, and difference of RGB
    #pixel values, respectively. 0 balck to 255 white
    #reading grayscale images
    redA = A
    redB = B
    where(redA > 127, 1, 0)
    where(redB > 127, 1 ,0)
    red_int = redA*redB
    red_int_fin = numpy.sum(red_int)
    #print "red_int_fin", red_int_fin
    red_un = numpy.sum(maximum(redA,redB))
    #print "red_un", red_un
    red_subAB = cv2.subtract(redA,redB)
    red_subAB = numpy.sum(where(red_subAB > 127,1,0))
    #print "red_subAB", red_subAB
    red_subBA = cv2.subtract(redB,redA)
    red_subBA = numpy.sum(where(red_subBA > 127,1,0))
    #print "red_subBA", red_subBA
    similarity = red_int_fin/(red_int_fin + alpha*red_subAB + beta*red_subBA)*1.0
    return float(similarity)

def transform(ind, img):
    if ind==0:
        return img
    elif ind==1:
        #mirror
        return cv2.flip(img,1)
    elif ind==2:
        #flip vertical
        return cv2.flip(img,0)
    #elif ind==3:
        #r90


def find_answer(question_images):
    for i in question_images:
        for j in question_images:
            #for ind in range(0,6):
            #j[1] = transform(ind, j[1])
            if i[0]!=j[0]:
                print i[0],j[0],image_similarity(i[1],j[1],1,1)



if __name__=='__main__':
    imageDir = sys.argv[1] #specify your path here
    image_path_list = []
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff"] #specify your vald extensions here
    valid_image_extensions = [item.lower() for item in valid_image_extensions]

    for file in os.listdir(imageDir):
        extension = os.path.splitext(file)[1]
        if extension.lower() not in valid_image_extensions:
            continue
        image_path_list.append(os.path.join(imageDir, file))

    question_images = []
    options_images = []

    for imagePath in image_path_list:
        img = cv2.imread(imagePath,0)
        if img is None:
            continue
        else:
            name = imagePath.split('/')[-1].split('.')[0]
            if name.isalpha():
                question_images.append([name,img])
                print 'alpha'
            else:
                options_images.append([name,img])

        cv2.imshow(imagePath, img)

        key = cv2.waitKey(0)
        if key == 27: # escape
            break
    options_images.sort(key=lambda x: x[0])
    question_images.sort(key=lambda x: x[0])

    find_answer(question_images)

    cv2.destroyAllWindows()
    #height, width, channels = question_images[1][1].shape
    #print height, width, channels
