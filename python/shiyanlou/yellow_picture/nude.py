#!/usr/bin/env python
# coding=utf-8


import sys
import os
import _io
from collections import namedtuple
from PIL import Image


class Nude(object):
    Skin = namedtuple('Skin','id skin region x y')

    def __init__(self,path_or_image):
        # 若path_or_image 为Image.Image 类型的实例，直接赋值
        if isinstance(path_or_image,Image.Image):
            self.image = path_or_image
        elif isinstance(path_or_image,str):
            self.image = Image.open(path_or_image)
        
        # 获取图片所有颜色通道
        bands = self.image.getbands()
        # 判断是否为单通道图片
        if len(bands) == 1:
            # 新建大小相同的RGB图像
            new_img = Image.new('RGB',self.image.size)
            new_img.paste(self.image)
            f = self.image.filename 
            self.image = new_img
            self.image.filename = f


        self.skin_map = []
        self.detected_regions = []
        self.merge_regions = []
        self.skin_regions = []
        self.last_from,self.last_to = -1,-1
        self.result = None
        self.message = None
        self.width,self.height = self.image.size
        self.total_pixels = self.width * self.height


    def resize(self,maxwidth=1000,maxheight=1000):
        ret = 0
        if maxwidth:
            if self.width > maxwidth:
                wpercent = (maxwidth/self.width)
                hsize = int(self.height*wpercent)
                fname = self.image.filename
                self.image = self.image.resize((maxwidth,hsize),Image.LANCZOS)
                self.image.filename = fname
                self.width,self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 1

        if maxheight:
            if self.height > maxheight:
                hpercent = (maxheight/float(self.height))
                wsize = int(float(self.width)*float(hpercent))
                fname = self.image.filename
                self.image = self.image.resize((wsize,maxheight),Image.LANCZOS)
                self.image.filename = fname
                self.width,self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 2

        return ret


    def parse(self):
        if self.result is not None:
            return self

        pixels = self.image.load()
        for y in range(self.height):
            for x in range(self.width):
                r = pixels[x,y][0]
                g = pixels[x,y][1]
                b = pixels[x,y][2]
                isSkin = True if self._classify_skin(r,g,b) else False
                _id = x+y * self.width +1
                self.skin_map.append(self.Skin(_id,isSkin,None,x,y))
                if not isSkin:
                    continue

                check_indexes = [_id-2,_id-self.width-2,_id-self.width-1,_id-self.width]
                region = -1
                for index in check_indexes:
                    try:
                        self.skin_map[index]
                    except IndexError:
                        break
                    if self.skin_map[index].skin:
                        if (self.skin_map[index].region != None and region != None and region != -1 and self.skin_map[index].region != region and self.last_from != region and self.last_to != self.skin_map[index].region):
                            self._add_merge(region,self.skin_map[index].region)
                        region = self.skin_map[index].region
                if region == -1:
                    _skin = self.skin_map[_id - 1]._replace(region=region)
                    self.skin_map[_id-1] = _skin
                    self.detected_regions.append(self.skin_map[_id-1])
                elif region != None:
                    _skin = self.skin_map[_id - 1]._replace(region=region)
                    self.skin_map[_id - 1] = _skin
                    self.detected_regions[region].append(self.skin_map[_id - 1])
        self._merge(self.detected_regions,self.merge_regions)
        self._analyse_regions()
        return self


    def _add_merge(self,_from,_to):
        self.last_from = _from
        self.last_to = _to

        from_index = -1
        to_index = -1

        for index,region in enumerate(self.merge_regions):
            for r_index in region:
                if r_index == _from:
                    from_index = index
                if r_index == _to:
                    to_index = index
        if from_index != -1 and to_index != -1:
            if from_index != to_index:
                self.merge_regions[from_index].extend(self.merge_regions[to_index])
                del(self.merge_regions[to_index])
            return
        if from_index == -1 and to_index == -1:
            self.merge_regions.append([_from,_to])
            return
        if from_index != -1 and to_index == -1:
            self.merge_regions[from_index].append(_to)
            return
        if from_index == -1 and to_index != -1:
            self.merge_regions[to_index].append(_from)
            return


    def _merge(self,detected_regions,merge_regions):
        new_detected_regions = []
        for index,region in enumerate(merge_regions):
            try:
                new_detected_regions[index]
            except IndexError:
                new_detected_regions.append([])
            for r_index in region:
                new_detected_regions[index].extend(detected_regions[r_index])
                detected_regions[r_index] = []
        for region in detected_regions:
            if len(region) > 0:
                new_detected_regions.append(region)
        self._clear_regions(new_detected_regions)


    def _clear_regions(self,detected_regions):
        for region in detected_regions:
            if len(region) > 0:
                self.skin_regions.append(region)


    def _analyse_regions(self):
        if len(self.skin_regions) < 3:
            self.message = "Less than 3 skin regions({_skin_regions_size})".format(_skin_regions_size=len(self.skin_regions))
            self.result = False
            return self.result

        self.skin_regions = sorted(self.skin_regions,key=lambda s:len(s),reverse=True)
        total_skin = float(sum([len(skin_region) for skin_region in self.skin_regions]))
        if total_skin/self.total_pixels*100 < 15:
            slef.message = "Total skin percentages lower than 15 ({:2f})".format(total_skin/self.total_pixels * 100)
            self.result = False
            return self.result
        if len(self.skin_regions[0])/total_skin *100 < 45:
            self.message = "The biggest region contains less than 45 ({:2f})".format(len(self.skin_regions[0])/total_skin*100)
            self.result = False
            return self.result
        if len(self.skin_regions) > 60:
            self.message = "More than 60 skin regions ({})".format(len(self.skin_regions))
            self.result = False
            return self.result
        self.message = 'Nude!'
        self.result = True
        return self.result


    def _classify_skin(self,r,g,b):
        rgb_classifier = r>95 and\
             g>40 and g<100 and\
                  b>20 and \
                      max([r,g,b])-min([r,g,b]) >15 and\
                           abs(r-g) >15 and\
                                r>g and\
                                     r>b
        nr,ng,nb = self._to_normalized(r,g,b)
        norm_rgb_classifier = nr/ng >1.185 and float(r*b)/((r+g+b)**2) >0.107 and float(r*g)/((r+g+b)**2) > 0.112
        h,s,v = self._to_hsv(r,g,b)
        hsv_classifier = h>0 and h<35 and s>0.23 and s<0.68
        y,cb,cr = self._to_ycbcr(r,g,b)
        ycbcr_classifier= 97.5 <= cb <= 142.5 and 134 <= cr <= 176
        return ycbcr_classifier


    def _to_normalized(self,r,g,b):
        if r == 0:
            r = 0.0001
        if g == 0:
            g = 0.0001
        if b == 0:
            b = 0.0001

        _sum = float(r+g+b)
        return [r/_sum ,g/_sum, b/_sum]


    def _to_ycbcr(self,r,g,b):
        y = .299*r+.587*g+.114*b
        cb = 128-0.168736*r-0.331364*g+0.5*b
        cr = 128+0.5*r -0.418688*g - 0.081312*b
        return y,cb,cr


    def _to_hsv(self,r,g,b):
        h = 0
        _sum = float(r+g+b)
        _max = float(max([r,g,b]))
        _min = float(min([r,g,b]))
        diff = float(_max-_min)
        if _sum == 0:
            _sum = 0.0001
        if _max ==r:
            if diff == 0:
                h = sys.maxsize

            else:
                h = (g-b)/diff
        elif _max == g:
            h = 2+((g-r)/diff)
        else:
            h = 4+((r-g)/diff)
        h *= 60
        if h < 0:
            h += 360
        return [h,1.0-(3.0*(_min/_sum)),(1.0/3.0)*_max]


    def insepect(self):
        _image = '{}{}{}*{}'.format(self.image.filename,self.image.format,self.width,self.height)
        return "{_image}:result = {_result} message = '{_message}'".format(_image=_image,_result=self.result,_message=self.message)


    def showSkinRegions(self):
        if self.result is None:
            return
        skinIdSet = set()
        simage = self.image
        simageData = simage.load()
        for sr in self.skin_regions:
            for pixel in sr:
                skinIdSet.add(pixel.id)
        for pixel in self.skin_map:
            if pixel.id not in skinIdSet:
                simageData[pixel.x,pixel.y]=0,0,0
            else:
                simageData[pixel.x,pixel.y]=255,255,255

        filePath = os.path.abspath(self.image.filename)
        fileDirectory = os.path.dirname(filePath)+'/'
        fileFullName = os.path.basename(filePath)
        fileName, fileExtName = os.path.splitext(fileFullName)
        simage.save('{}{}_{}{}'.format(fileDirectory,fileName,'Nude' if self.result else 'Normal',fileExtName))





if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Detect nudity in images.')
    parser.add_argument('files',metavar='image',nargs='+',help='Images you wish to test')
    parser.add_argument('-r','--resize',action='store_true',help='Reduce image size to increase speed of scanning')
    parser.add_argument('-v','--visualization',action='store_true',help='Generating areas of skin image')
    args = parser.parse_args()
    for fname in args.files:
        if os.path.isfile(fname):
            n = Nude(fname)
            if args.resize:
                n.resize(maxheight=800,maxwidth=600)
            n.parse()
            if args.visualization:
                n.showSkinRegions()
            print(n.result,n.insepect())
        else:
            print(fname,'is not a file')


