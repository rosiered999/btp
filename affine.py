import cv2
import os, os.path
import sys
from numpy import *
from matplotlib import *
from pylab import *
import py_stringmatching

def image_similarity(A, B):
    result = cv2.matchTemplate(A, B, cv2.TM_CCORR_NORMED)

def transform(index, img):
    '''2*2 identity mirror flip r90 r180 r270'''
    '''3*3 union intersection xor'''
    if ind==0:
        return img
    elif ind==1:
        horizontal_img = img.copy()
        horizontal_img = cv2.flip( img, 0 )
        return horizontal_img
    elif ind==2:


def find_answer(question_images):
    for i in question_images:
        for j in question_images:
            for ind in range(0,6):
                j[1] = transform(ind, j[1])
                if i[0]!=j[0]:
                    print i[0],j[0],image_similarity(i[1],j[1])



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
