import cv2
import os, os.path
import sys
from numpy import *
from matplotlib import *
from pylab import *
import py_stringmatching

def image_similarity(A, B, alpha, beta):
    # https://stackoverflow.com/questions/43719451/python-convert-image-to-a-string-of-pixel-values
    # variant 4 ^^^^
    #result = cv2.matchTemplate(A, B, cv2.TM_CCORR_NORMED)
    #since i wanted to do tversky similarity and there is already a fn for that
    #i am converting the image to string
    str_repA = str(A.flatten().tolist())
    img_strA = str_repA.strip('[]').replace(',','')

    str_repB = str(A.flatten().tolist())
    img_strB = str_repB.strip('[]').replace(',','')
    #print A
    #what if i use number of black pixels in bitwise union, intersection, sub
    #print result'''
    if not isinstance(img_strA, set):
        img_strA = set(img_strA)
    if not isinstance(img_strB, set):
        img_strB = set(img_strB)
    print img_strA, img_strB
    intersection = float(len(img_strA & img_strB))
    return 1.0 * intersection / (intersection + (alpha * len(img_strA - img_strB)) + (beta * len(img_strB - img_strA)))



def find_answer(question_images):
    for i in question_images:
        for j in question_images:
            if i[0]!=j[0]:
                print i[0],j[0],image_similarity(i[1],j[1],0,0)
                print i[0],j[0],image_similarity(i[1],j[1],1,0)
                print i[0],j[0],image_similarity(i[1],j[1],0,1)
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
