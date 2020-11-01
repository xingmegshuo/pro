
from PIL import Image
import hashlib
import time
import os
import math


class VectorCompare:


    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count**2
        return math.sqrt(total)


    def relation(self,concordance1,concordance2):
        relevacne = 0
        topvalue = 0
        for word,count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))



def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


v = VectorCompare()
iconset = [i for i in range(0,9)] + [chr(i) for i in range(97,123)]
# print(iconset)
imggeset = []
for letter in iconset:
    for img in os.listdir('./python_captcha/iconset/{}/'.format(letter)):
        temp = []
        if img != 'Thumbs.db' and img != '.DS_Store':
            temp.append(buildvector(Image.open('./python_captcha/iconset/{}/{}'.format(letter,img))))
        imggeset.append({letter:temp})

#print(imggeset)
im = Image.open('./python_captcha/captcha.gif')
im2 = Image.new('P',im.size,255)
im.convert('P')
temp = {}

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        temp[pix] = pix
        if pix == 220 or pix == 227:
            im2.putpixel((y,x),0)


inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter = False

count = 0

for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))
    guess = []
    for image in imggeset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0],buildvector(im3)),x))
    #print()
    result = sorted(guess,key=lambda x:x[0],reverse=True)
    print(result[0])
    count += 1



