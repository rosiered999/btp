import cv2
import os, os.path
import sys
import numpy
from PIL import Image
import scipy.misc
import matplotlib.pyplot as plt
from pylab import *
import py_stringmatching
from scipy import ndimage
from operator import itemgetter
from pprint import pprint

def image_similarity(A, B, alpha, beta):
    #each feature is a pixel
    # intersection PRODUCT, union MAXIMUM, and subtraction DIFFERENCE operations are
    #defined as the product, maximum, and difference of RGB
    #pixel values, respectively. 0 balck to 255 white
    #reading grayscale images
    #http://www.daylight.com/meetings/mug97/Bradshaw/MUG97/tv_tversky.html
    redA = A
    redB = B
    #redA = where(redA > 127, 1, 0)
    #redB = where(redB > 127, 1 ,0)
    red_int_fin = numpy.sum(cv2.bitwise_and(redA,redB))
    #red_int_fin = numpy.sum(red_int)
    #print "red_int_fin", red_int_fin
    red_un = numpy.sum(cv2.bitwise_or(redA,redB))
    #print "red_un", red_un
    red_subAB = cv2.subtract(redA,redB)
    red_subAB = numpy.sum(red_subAB)
    #print "red_subAB", red_subAB
    red_subBA = cv2.subtract(redB,redA)
    red_subBA = numpy.sum(red_subBA)
    #print "red_subBA", red_subBA
    similarity = red_int_fin/(red_un + alpha*red_subAB + beta*red_subBA)*1.0
    return float(similarity)

def transform(ind, img):
    if ind==0:
        return img
    elif ind==1:
        #mirror flip horz
        return cv2.flip(img,1)
    elif ind==2:
        #flip vertical
        return cv2.flip(img,0)
    elif ind==3:
        #r90
        return ndimage.rotate(img,90)
    elif ind==4:
        return ndimage.rotate(img,180)
    elif ind==5:
        return ndimage.rotate(img,270)

def check_answer_options(ans_img, options_images):
    probs = []
    for i in options_images:
        img = i[1]
        confidence = image_similarity(img,ans_img,0,0)
        probs.append(confidence)
    mx = max(probs)
    ind = probs.index(mx)
    fin_ans = options_images[ind][1]
    #scipy.misc.imshow(fin_ans)
    return fin_ans


def find_answer(question_images):
    affine_trans_list = []
    visited = [0]*6
    for i in question_images:
        for j in question_images:
            img = i[1]
            if i[0]!=j[0] and (visited[ord(i[0])-65]!=1 or visited[ord(j[0])-65]!=1):
                for ind in range(0,6):
                    sub_list = []
                    img_to_trans = transform(ind, j[1])
                    visited[ord(i[0])-65]=1
                    visited[ord(j[0])-65]=1
                    #print ind
                    #print i[0],j[0],ind,"10",image_similarity(img,img_to_trans,1,0)
                    #print i[0],j[0],ind,"01",image_similarity(img,img_to_trans,0,1)
                    #print i[0],j[0],ind,"11",image_similarity(img,img_to_trans,1,1)
                    #MAKE A LIST, FIND MAX

                    affine_trans_list.append((i[0],j[0],ind,"10",image_similarity(img,img_to_trans,1,0)))
                    affine_trans_list.append((i[0],j[0],ind,"01",image_similarity(img,img_to_trans,0,1)))
                    affine_trans_list.append((i[0],j[0],ind,"11",image_similarity(img,img_to_trans,1,1)))
    affine = [x for x in affine_trans_list if x!=[]]
    max_tuple_affine = max(affine,key=itemgetter(4))
    pprint(affine)
    pprint(max_tuple_affine)
    #print max_tuple_affine[0]
    for sublist in question_images:
        if sublist[0]=='A':
            A = sublist[1]
        elif sublist[0]=='B':
            B = sublist[1]
        elif sublist[0]=='C':
            C = sublist[1]
    #print "question_images", question_images
    if(max_tuple_affine[0]=='A' and max_tuple_affine[1]=='B'):
        #do dsomething with C
        search = 'C'
        for sublist in question_images:
            if sublist[0] == search:
                print sublist
                key = sublist
                break
        ans_pre_img = transform(max_tuple_affine[2],key[1])
        if max_tuple_affine[3] =='11':
            #do this X = 0
            ans_img = ans_pre_img
        elif max_tuple_affine[3]=='10':
            #do this X = B-A
            X = cv2.subtract(B,A)
            ans_img = cv2.add(ans_pre_img,X)
        else:
            #do this X = A-B
            X = cv2.subtract(A,B)
            ans_img = cv2.subtract(ans_pre_img,X)
    elif(max_tuple_affine[0]=='A' and max_tuple_affine[1]=='C'):
        #do something with B
        search = 'B'
        for sublist in question_images:
            if sublist[0] == search:
                key = sublist
                break
        print "key", key
        ans_pre_img = transform(max_tuple_affine[2],key[1])

        if max_tuple_affine[3] =='11':
            #do this X = 0
            ans_img = ans_pre_img
        elif max_tuple_affine[3]=='10':
            #do this X = B-A
            X = cv2.subtract(C,A)
            ans_img = cv2.add(ans_pre_img,X)
        else:
            #do this X = A-B
            X = cv2.subtract(A,C)
            ans_img = cv2.subtract(ans_pre_img,X)
    #img = Image.fromarray(ans_img, 'RGB')
    #scipy.misc.imshow(ans_img)
    return ans_img

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
            #img = where(img > 127, 1,0)
            if name.isalpha():
                question_images.append([name,img])
                print 'alpha'
            else:
                options_images.append([name,img])
        #cv2.imshow(imagePath, img)

        #key = cv2.waitKey(0)
        #if key == 27: # escape
            #break
    options_images.sort(key=lambda x: x[0])
    question_images.sort(key=lambda x: x[0])

    img = find_answer(question_images)
    ans_img = check_answer_options(img, options_images)
    scipy.misc.imshow(ans_img)

    cv2.destroyAllWindows()
    #height, width, channels = question_images[1][1].shape
    #print height, width, channels
