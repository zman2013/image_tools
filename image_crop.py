#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from PIL import Image
import os
import sys


def crop_images(extension, srcDir, dstDir):
    if not os.path.exists(dstDir):
        print("creating dir: " + dstDir)
        os.mkdir(dstDir)

    for root, dirs, files in os.walk(srcDir):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if root.startswith(dstDir):
                continue

            if f.endswith(extension):
                print("src: " + os.path.join(root, f))
                relativeDir = root.replace(srcDir, "")
                if relativeDir.startswith("/"):
                    relativeDir = relativeDir[1:]
                print("relativeDir: " + relativeDir)
                print("dstDir: " + dstDir)
                targetDir = os.path.join(dstDir, relativeDir)
                print("targetDir: " + targetDir)
                srcImagePath = os.path.join(root, f)
                crop_image(srcImagePath, targetDir)


def crop_image(srcImagePath, dstDir):
    if not os.path.exists(dstDir):
        print("creating dir: " + dstDir)
        os.mkdir(dstDir)

    im = Image.open(srcImagePath)



    print("imageWidth:", im.width, "imageHeight:", im.height )

    # 计算图片大小
    # 找到图片顶点
    y = 0
    while y < im.height:
        x = 0
        while x < im.width:
            pixel = im.getpixel((x, y))
            if pixel.__len__() == 3 or pixel[3] != 0:
                topY = y
                break
            x += 1
        y += 1
    # 找到图片X最大点
    x = 0
    while x < im.width:
        y = 0
        while y < im.height:
            pixel = im.getpixel((x, y))
            if pixel.__len__() == 3 or pixel[3] != 0:
                topX = x
                break
            y += 1
        x += 1
    # 找到最下面的点
    y = im.height - 1
    while y > -1:
        x = 0
        while x < im.width:
            pixel = im.getpixel((x, y))
            if pixel.__len__() == 3 or pixel[3] != 0:
                bottomY = y
                break
            x += 1
        y -= 1
    # 找到X最小点
    x = im.width - 1
    while x > -1:
        y = 0
        while y < im.height:
            pixel = im.getpixel((x, y))
            if pixel.__len__() == 3 or pixel[3] != 0:
                bottomX = x
                break
            y += 1
        x -= 1

    print(topX, topY, bottomX, bottomY)

    width = topX - bottomX + 1
    height = topY - bottomY + 1

    print("width: ", width, "height: ", height)

    # 剪切图片
    box = (bottomX, bottomY, topX, topY)
    region = im.crop(box)

    # 生成新图片
    newImage = Image.new("RGBA", (width, height))
    newImage.paste(region)

    # 调整图像大小
    newImage = newImage.resize((128, 128))

    # 保存新图片
    imagePath, imageFileName = os.path.split(srcImagePath)
    newImagePath = os.path.join(dstDir, imageFileName)
    newImage.save(newImagePath, "PNG")


print("裁剪PNG图片周边的空像素")

if sys.argv.__len__() == 1:
    print("没有参数，默认为当前目录")
    srcPath = os.getcwd()
else:
    srcPath = sys.argv[1]

if os.path.isfile(srcPath):
    print("参数为单个文件，进行转换")
    imageDir, imageFileName = os.path.split(srcPath)
    dstDir = os.path.join(imageDir, "_cropped")
    print("裁剪后图片目录：", dstDir)
    crop_image(srcPath, dstDir)

elif os.path.isdir(srcPath):
    print("参数为文件夹，对文件夹内所有PNG文件进行转换")
    dstDir = os.path.join(srcPath, "_cropped")
    print("裁剪后图片目录：", dstDir)
    crop_images(".png", srcPath, dstDir)
