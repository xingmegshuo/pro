#!/usr/bin/env python
# coding=utf-8




from PIL import Image
import argparse


#命令行输入参数

parser = argparse.ArgumentParser()

# 输入文件
parser.add_argument('file')
# 输出文件
parser.add_argument('-o','--output')
# 宽
parser.add_argument('--width',type=int,default=80) 
# 高
parser.add_argument('--height',type=int,default=80)


# 获取参数

args = parser.parse_args()

img = args.file
width = args.width
height = args.height
output = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!1I;:.\‘’^``.")
print(ascii_char)

def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

# print('ok')



if __name__ == '__main__':
    print('ok')
    im = Image.open(img)
    im = im.resize((width,height),Image.NEAREST)
#    print(im)
    txt = ''
    for i in range(height):
        for j in range(width):
            txt += get_char(*im.getpixel((j,i)))
 #           print(txt,'1')
        txt += '\n'
    print(txt)
    if output:
        with open(output,'w') as f:
            f.write(txt)

    else:
        with open('output.txt','w') as f:
            f.write(txt)


