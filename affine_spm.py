import cv2
import os, os.path
import sys
import numpy
from PIL import Image
import scipy.misc
import matplotlib.pyplot as plt
from pylab import *
from scipy import ndimage
from operator import itemgetter
from pprint import pprint
from copy import deepcopy
from skimage.measure import structural_similarity as ssim

def image_similarity(A, B, alpha, beta):
    redA = A
    redB = B
    #print redA.shape
    #print redB.shape
    redA = cv2.resize(A, (60,60),interpolation=cv2.INTER_AREA)
    redB = cv2.resize(B, (60,60),interpolation=cv2.INTER_AREA)
    #scipy.misc.imshow(redA)
    #scipy.misc.imshow(redB)
    red_int_fin = numpy.sum(numpy.minimum(redA,redB))
    red_un = numpy.sum(numpy.maximum(redA,redB))
    red_subAB = cv2.subtract(redA,redB)
    red_subAB = numpy.sum(red_subAB)
    red_subBA = cv2.subtract(redB,redA)
    red_subBA = numpy.sum(red_subBA)
    similarity = red_int_fin/(red_un + alpha*red_subAB + beta*red_subBA)*1.0
    return round(similarity,3)

def image_similarity_ssd(A,B,alpha,beta):
    redA = A
    redB = B
    redA = cv2.resize(A, (60,60),interpolation=cv2.INTER_AREA)
    redB = cv2.resize(B, (60,60),interpolation=cv2.INTER_AREA)
    print numpy.sum(cv2.subtract(redA,redB))
    similarity = 100000/(1+numpy.sum(cv2.subtract(redA,redB)**2))
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
    print "ind",ind
    fin_ans = options_images[ind][1]
    return ind,fin_ans


def find_answer(question_images):
    affine_trans_list = []
    if len(question_images)==3:
        print "LEN QIMAGES", len(question_images)
        visited = [0]*6
        for i in question_images:
            for j in question_images:
                img = i[1]
                if i[0]!=j[0] and (visited[ord(i[0])-65]!=1 or visited[ord(j[0])-65]!=1):
                    for ind in range(0,6):
                        img_to_trans = transform(ind, j[1])
                        visited[ord(i[0])-65]=1
                        visited[ord(j[0])-65]=1
                        affine_trans_list.append((i[0],j[0],ind,"10",image_similarity(img,img_to_trans,1,0)))
                        affine_trans_list.append((i[0],j[0],ind,"01",image_similarity(img,img_to_trans,0,1)))
                        affine_trans_list.append((i[0],j[0],ind,"11",image_similarity(img,img_to_trans,1,1)))
        affine = [x for x in affine_trans_list if x!=[]]
        max_tuple_affine = max(affine,key=itemgetter(4))
        maxes = []
        for i in affine:
            if i[4] == max_tuple_affine[4]:
                maxes.append(i)
        print "MAXES",maxes
        pprint(affine)
    else:
        visited = [0]*16
        for i in question_images:
            for j in question_images:
                img = i[1]
                if(i[0]!=j[0]):
                    for ind in range(0,6):
                        #print ind
                        img_to_trans = transform(ind, j[1])
                        visited[ord(i[0])-65]=1
                        visited[ord(j[0])-65]=1
                        affine_trans_list.append((i[0],j[0],ind,"10",image_similarity(img,img_to_trans,1,0)))
                        affine_trans_list.append((i[0],j[0],ind,"01",image_similarity(img,img_to_trans,0,1)))
                        affine_trans_list.append((i[0],j[0],ind,"11",image_similarity(img,img_to_trans,1,1)))
        affine = [x for x in affine_trans_list if x!=[]]
        affine.sort
    #pprint(affine)
    #pprint(max_tuple_affine)
    letter_dict = {}
    for sublist in question_images:
        if sublist[0]=='A':
            A = sublist[1]
            A = cv2.resize(A, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['A'] = A
        elif sublist[0]=='B':
            B = sublist[1]
            B = cv2.resize(B, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['B'] = B
        elif sublist[0]=='C':
            C = sublist[1]
            C = cv2.resize(C, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['C'] = C
        elif sublist[0]=='D':
            D = sublist[1]
            D = cv2.resize(D, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['D'] = D
        elif sublist[0]=='E':
            E = sublist[1]
            E = cv2.resize(E, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['E'] = E
        elif sublist[0]=='F':
            F = sublist[1]
            F = cv2.resize(F, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['F'] = F
        elif sublist[0]=='G':
            G = sublist[1]
            G = cv2.resize(G, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['G'] = G
        elif sublist[0]=='H':
            H = sublist[1]
            H = cv2.resize(H, (60,60),interpolation=cv2.INTER_AREA)
            letter_dict['H'] = H
    if len(question_images)==3:
        if(max_tuple_affine[0]=='A' and max_tuple_affine[1]=='B'):
            search = 'C'
            for sublist in question_images:
                if sublist[0] == search:
                    #print sublist
                    key = sublist
                    break
            ans_pre_img = transform(max_tuple_affine[2],key[1])
            ans_pre_img = cv2.resize(ans_pre_img, (60,60),interpolation=cv2.INTER_AREA)
            scipy.misc.imshow(ans_pre_img)
            '''if max_tuple_affine[3] =='11':
                #do this X = 0
                ans_img = ans_pre_img
            elif max_tuple_affine[3]=='10':
                #do this X = B-A
                X = cv2.subtract(B,A)
                X = cv2.resize(X, (60,60),interpolation=cv2.INTER_AREA)
                ans_img = cv2.add(ans_pre_img,X)
            else:
                #do this X = A-B
                X = cv2.subtract(A,B)
                X = cv2.resize(X, (60,60),interpolation=cv2.INTER_AREA)
                ans_img = cv2.subtract(ans_pre_img,X)'''
            ans_img = ans_pre_img
        elif(max_tuple_affine[0]=='A' and max_tuple_affine[1]=='C'):
            search = 'B'
            for sublist in question_images:
                if sublist[0] == search:
                    key = sublist
                    break
            #print "key", key
            ans_pre_img = transform(max_tuple_affine[2],key[1])
            ans_pre_img = cv2.resize(ans_pre_img, (60,60),interpolation=cv2.INTER_AREA)
            #scipy.misc.imshow(ans_pre_img)
            ans_img = ans_pre_img
            '''if max_tuple_affine[3] =='11':
                #do this X = 0
                ans_img = ans_pre_img
            elif max_tuple_affine[3]=='10':
                #do this X = B-A
                X = cv2.subtract(C,A)
                ans_img = cv2.add(ans_pre_img,X)
            else:
                #do this X = A-B
                X = cv2.subtract(A,C)
                ans_img = cv2.subtract(ans_pre_img,X)'''
    else:
        print "AFFINE"
        #pprint(affine)
        max_tuple_affine = max(affine,key=itemgetter(4))
        print max_tuple_affine
        maxes = []
        for i in affine:
            #print i[4]-max_tuple_affine[4]
            if abs(i[4]- max_tuple_affine[4])<=0.05:
                maxes.append(i)
        print "MAXES"
        pprint(maxes)
        pprint(max_tuple_affine)
        A1 = ['A','B','C']
        B1 = ['D','E','F']
        C1 = ['G','H','X']
        A2 = ['A','D','G']
        B2 = ['B','E','H']
        A3 = ['H','F','A']
        B3 = ['B','G','F']
        flag = 0
        inn = 1
        list_letters = [A1,B1,C1,A2,B2,A3,B3]
        x = max_tuple_affine[0]
        y = max_tuple_affine[1]
        for i in list_letters:
            if x in i and y in i:
                flag = 1
                z = deepcopy(i)
                z.remove(x)
                z.remove(y)
                print 'z',z
                search = z[0]
        while flag==0:
            x = maxes[inn][0]
            y = maxes[inn][1]
            for i in list_letters:
                if x in i and y in i:
                    flag = 1
                    z = deepcopy(i)
                    z.remove(x)
                    z.remove(y)
                    print 'z',z
                    search = z[0]
        #print x,y,search
        for sublist in question_images:
            if sublist[0] == search:
                #print sublist
                key = sublist
                break
        ans_pre_img = transform(max_tuple_affine[2],key[1])
        #print ans_pre_img.shape
        ans_pre_img = cv2.resize(ans_pre_img, (60,60),interpolation=cv2.INTER_AREA)
        #scipy.misc.imshow(ans_pre_img)
        if max_tuple_affine[3] =='11':
            #do this X = 0
            ans_img = ans_pre_img
        elif max_tuple_affine[3]=='10':
            #do this X = B-A
            X = cv2.subtract(letter_dict[y],letter_dict[x])
            ans_img = cv2.add(ans_pre_img,X)
        else:
            #do this X = A-B
            X = cv2.subtract(letter_dict[y],letter_dict[x])
            ans_img = cv2.subtract(ans_pre_img,X)

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
            if name.isalpha():
                question_images.append([name,img])
                #print 'alpha'
            elif name.isdigit():
                options_images.append([name,img])

    options_images.sort(key=lambda x: x[0])
    question_images.sort(key=lambda x: x[0])

    img = find_answer(question_images)
    #if len(question_images)>3:
    ans_option, ans_img = check_answer_options(img, options_images)
    print ans_option+1
    img = ans_img
    scipy.misc.imshow(img)

    cv2.destroyAllWindows()
