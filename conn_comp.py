import scipy
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import sys
import cv2
from pprint import pprint
#https://stackoverflow.com/questions/16937158/extracting-connected-objects-from-an-image-in-python
#http://pythonvision.org/basic-tutorial/
fname=sys.argv[1]
blur_radius = 0.76

img = cv2.imread(fname,0) # gray-scale image
ret,thresh_img = cv2.threshold(img,25,255,cv2.THRESH_BINARY)
img = thresh_img
img = 255 - img
threshold = 90
print(img.shape)

# smooth the image (to remove small objects)
imgf = ndimage.gaussian_filter(img, blur_radius)
threshold = 0
struct=np.ones((3,3), dtype="bool8") #connnectivity struct
# find connected components
labeled, nr_objects = ndimage.label(imgf > threshold, structure=struct)
print "Number of objects is %d " % nr_objects

plt.imsave('/tmp/out.png', labeled)
plt.imshow(labeled)

plt.show()
