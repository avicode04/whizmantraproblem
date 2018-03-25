import cv2
import numpy as np

from matplotlib import pyplot as plt
#import matplotlib.image as mpimg
print("1")
img = cv2.imread('Original-2-1.jpg')


y0=0;x0=0;

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

Horizontal_lines=[]
Vertical_lines=[]

print("Plot Show")
#imgplot = plt.imshow(lines)
#plt.show()

img_crop_Horizontal=img[0:2000,2299:2500]
img_crop_Horizontal2=img[0:2000,1500:1700]
gray_crop = cv2.cvtColor(img_crop_Horizontal,cv2.COLOR_BGR2GRAY)


edges_crop = cv2.Canny(gray_crop,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines_crop = cv2.HoughLinesP(edges_crop,1,np.pi/180,100,minLineLength,maxLineGap)

gray_crop2 = cv2.cvtColor(img_crop_Horizontal2,cv2.COLOR_BGR2GRAY)
edges_crop2 = cv2.Canny(gray_crop2,50,150,apertureSize = 3)

minLineLength = 100
maxLineGap = 10
lines_crop2 = cv2.HoughLinesP(edges_crop2,1,np.pi/180,100,minLineLength,maxLineGap)

i=0
while i<len(lines):
    for x1,y1,x2,y2 in lines[i]:
        if abs(x1-x2)<3:
            b=[x1]
            Vertical_lines.append(b)
            i=i+1
        else:
            i=i+1




i=0
while i<len(lines_crop):
    for x1,y1,x2,y2 in lines_crop[i]:
        if abs(y1-y2)<10:
            b=[y1]
            Horizontal_lines.append(b)
            i=i+1
        else:
            i=i+1


Horizontal_lines2=[]
i=0
while i<len(lines_crop2):
    for x1,y1,x2,y2 in lines_crop2[i]:
        if abs(y1-y2)<10:
            b=[y1]
            Horizontal_lines2.append(b)
            i=i+1
        else:
            i=i+1



horizontal_lines=Horizontal_lines+Horizontal_lines2



horizontal_lines.sort()



Vertical_lines.sort()


horizontal_level=[]

j=0
while j<len(horizontal_lines)-1:
    a=horizontal_lines[j+1]
    b=horizontal_lines[j]
    d=np.array(a)-np.array(b)
    if abs(d)>30:
        horizontal_level.append(a)
        j=j+1
    else:
        j=j+1





Vertical_level=[]

j=0
while j<len(Vertical_lines)-1:
    a=Vertical_lines[j+1]
    b=Vertical_lines[j]
    d=np.array(a)-np.array(b)
    if abs(d)>25:
        Vertical_level.append(a)
        j=j+1
    else:
        j=j+1



#question selection from matching point of tamplete (x0,y0)
y0=[y0]#assuming point is integer neither numpy or list convt here to list
question=[]
m=0
while m<len(horizontal_level)-1:
    if horizontal_level[m]<y0<horizontal_level[m+1]:
        qn=m+1+Which_side_paper_is_tested #here we dont know which is our question paper
        question.append(qn)
        m=m+1
    else:
        m=m+1



#point we get from template matching is (x0,y0)
x0=[x0]
answer=[]
if x0<Vertical_level[2]:
    answer.append('A')
else:
    x0=x0
if Vertical_level[3]>x0>Vertical_level[2]:
    answer.append('B')
else:
    x0=x0
if Vertical_level[4]>x0>Vertical_level[3]:
    answer.append('C')
else:
    answer.append('D')


#path = "E:\Hackfest\EU flag horizontal mono.jpg"


img2 = lines_crop2

t = "C:\\Users\\Avi\\PycharmProjects\\text5\\test.jpg"
template = cv2.imread(t,0)

w, h = template.shape[::-1]


#compare all 3 methods of comparisons possible in the

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()

