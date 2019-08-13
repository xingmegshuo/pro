# coding:utf-8
"""
使用 Python 创建照片马赛克

输入一张目标照片和多张替换照片，将目标照片按网格划分为许多小方块，然后将每个小方块替换为颜色值最
接近的那张替换照片，就形成了马赛克效果。
"""

import argparse
import os

import numpy as np
from PIL import Image


def splitImage(image, size):
    """
    将图像按网格划分成多个小图像

    @param {Image} image PIL Image 对象
    @param {Tuple[int, int]} size 网格的行数和列数
    @return {List[Image]} 小图像列表
    """

    W, H = image.size[0], image.size[1]
    m, n = size
    w, h = int(W / n), int(H / m)
    imgs = []
    # 先按行再按列裁剪出 m * n 个小图像
    for j in range(m):
        for i in range(n):
            # 坐标原点在图像左上角
            imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
    return imgs


def getImages(imageDir):
    """
    从给定目录里加载所有替换图像

    @param {str} imageDir 目录路径
    @return {List[Image]} 替换图像列表
    """

    files = os.listdir(imageDir)
    images = []
    for file in files:
        # 得到文件绝对路径
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            fp = open(filePath, "rb")
            im = Image.open(fp)
            images.append(im)
            # 确定了图像信息，但没有加载全部图像数据，用到时才会
            im.load()
            # 用完关闭文件，防止资源泄露
            fp.close()
        except:
            # 加载某个图像识别，直接跳过
            print("Invalid image: %s" % (filePath,))
    return images


def getAverageRGB(image):
    """
    计算图像的平均 RGB 值

    将图像包含的每个像素点的 R、G、B 值分别累加，然后除以像素点数，就得到图像的平均 R、G、B
    值

    @param {Image} image PIL Image 对象
    @return {Tuple[int, int, int]} 平均 RGB 值
    """

    # 计算像素点数
    npixels = image.size[0] * image.size[1]
    # 获得图像包含的每种颜色及其计数，结果类似 [(cnt1, (r1, g1, b1)), ...]
    cols = image.getcolors(npixels)
    # 获得每种颜色的 R、G、B 累加值，结果类似 [(c1 * r1, c1 * g1, c1 * g2), ...]
    sumRGB = [(x[0] * x[1][0], x[0] * x[1][1], x[0] * x[1][2]) for x in cols]
    # 分别计算所有颜色的 R、G、B 平均值，算法类似(sum(ci * ri)/np, sum(ci * gi)/np,
    # sum(ci * bi)/np)
    # zip 的结果类似[(c1 * r1, c2 * r2, ..), (c1 * g1, c1 * g2, ...), (c1 * b1,
    # c1 * b2, ...)]
    avg = tuple([int(sum(x) / npixels) for x in zip(*sumRGB)])
    return avg


def getAverageRGBNumpy(image):
    """
    计算图像的平均 RGB 值，使用 numpy 来计算以提升性能

    @param {Image} image PIL Image 对象
    @return {Tuple[int, int, int]} 平均 RGB 值
    """

    # 将 PIL Image 对象转换为 numpy 数据数组
    im = np.array(image)
    # 获得图像的宽、高和深度
    w, h, d = im.shape
    # 将数据数组变形并计算平均值
    return tuple(np.average(im.reshape(w * h, d), axis=0))


def getBestMatchIndex(input_avg, avgs):
    """
    找出颜色值最接近的索引

    把颜色值看做三维空间里的一个点，依次计算目标点跟列表里每个点在三维空间里的距离，从而得到距
    离最近的那个点的索引。

    @param {Tuple[int, int, int]} input_avg 目标颜色值
    @param {List[Tuple[int, int, int]]} avgs 要搜索的颜色值列表
    @return {int} 命中元素的索引
    """

    index = 0
    min_index = 0
    min_dist = float("inf")
    for val in avgs:
        # 三维空间两点距离计算公式 (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        # + (z1 - z2) * (z1 - z2)，这里只需要比较大小，所以无需求平方根值
        dist = ((val[0] - input_avg[0]) * (val[0] - input_avg[0]) +
                (val[1] - input_avg[1]) * (val[1] - input_avg[1]) +
                (val[2] - input_avg[2]) * (val[2] - input_avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1

    return min_index


def createImageGrid(images, dims):
    """
    将图像列表里的小图像按先行后列的顺序拼接为一个大图像

    @param {List[Image]} images 小图像列表
    @param {Tuple[int, int]} dims 大图像的行数和列数
    @return Image 拼接得到的大图像
    """

    m, n = dims

    # 确保小图像个数满足要求
    assert m * n == len(images)

    # 计算所有小图像的最大宽度和高度
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    # 创建大图像对象
    grid_img = Image.new('RGB', (n * width, m * height))

    # 依次将每个小图像粘贴到大图像里
    for index in range(len(images)):
        # 计算要粘贴到网格的哪行
        row = int(index / n)
        # 计算要粘贴到网格的哪列
        col = index - n * row
        # 根据行列数以及网格的大小得到网格的左上角坐标，把小图像粘贴到这里
        grid_img.paste(images[index], (col * width, row * height))

    return grid_img


def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images=True):
    """
    图片马赛克生成

    @param {Image} target_image 目标图像
    @param {List[Image]} input_images 替换图像列表
    @param {Tuple[int, int]} grid_size 网格行数和列数
    @param {bool} reuse_images 是否允许重复使用替换图像
    @return {Image} 马赛克图像
    """

    # 将目标图像切成网格小图像
    print('splitting input image...')
    target_images = splitImage(target_image, grid_size)

    # 为每个网格小图像在替换图像列表里找到颜色最相似的替换图像
    print('finding image matches...')
    output_images = []
    # 分 10 组进行，每组完成后打印进度信息，避免用户长时间等待
    count = 0
    batch_size = int(len(target_images) / 10)

    # 计算替换图像列表里每个图像的颜色平均值
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))

    # 对每个网格小图像，从替换图像列表找到颜色最相似的那个，添加到 output_images 里
    for img in target_images:
        # 计算颜色平均值
        avg = getAverageRGB(img)
        # 找到最匹配的那个小图像，添加到 output_images 里
        match_index = getBestMatchIndex(avg, avgs)
        output_images.append(input_images[match_index])
        # 如果完成了一组，打印进度信息
        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print('processed %d of %d...' % (count, len(target_images)))
        count += 1
        # 如果不允许重用替换图像，则用过后就从列表里移除
        if not reuse_images:
            input_images.remove(match)

    # 将 output_images 里的图像按网格大小拼接成一个大图像
    print('creating mosaic...')
    mosaic_image = createImageGrid(output_images, grid_size)

    return mosaic_image


def main():
    # 定义程序接收的命令行参数
    parser = argparse.ArgumentParser(
        description='Creates a photomosaic from input images')
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-size', nargs=2,
                        dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)

    # 解析命令行参数
    args = parser.parse_args()

    # 网格大小
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

    # 马赛克图像保存路径，默认为 mosaic.png
    output_filename = 'mosaic.png'
    if args.outfile:
        output_filename = args.outfile

    # 打开目标图像
    print('reading targe image...')
    target_image = Image.open(args.target_image)

    # 从指定文件夹下加载所有替换图像
    print('reading input images...')
    input_images = getImages(args.input_folder)
    # 如果替换图像列表为空则退出程序
    if input_images == []:
        print('No input images found in %s. Exiting.' % (args.input_folder, ))
        exit()

    # 将所有替换图像缩放到指定的网格大小
    print('resizing images...')
    dims = (int(target_image.size[0] / grid_size[1]),
            int(target_image.size[1] / grid_size[0]))
    for img in input_images:
        img.thumbnail(dims)

    # 生成马赛克图像
    print('starting photomosaic creation...')
    mosaic_image = createPhotomosaic(target_image, input_images, grid_size)

    # 保存马赛克图像
    mosaic_image.save(output_filename, 'PNG')
    print("saved output to %s" % (output_filename,))

    print('done.')


if __name__ == '__main__':
    main()
