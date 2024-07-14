from PIL import Image
import io
import numpy as np

def size(file):
    img = Image.open(io.BytesIO(file)).convert('RGBA')# 打开图片并转换为RGBA模式
    width, height = img.size# 获取图片宽度和高度
    alpha = [[0 for _ in range(width)] for _ in range(height)]# 初始化二维数组
    # 遍历图片的每个像素,生成alpha通道对应的数组
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            alpha[y][x] = a
    #遍历行，找到滑块的高度
    start,i= 1,1
    for row in alpha:
        i+= 1
        if all(value == 0 for value in row):
            if start == i-1:
                start = i
        else:
            end = i-2
    #print(start,end)
    img.close()
    return start,end
def searchwhite(num):
    #要处理的矩阵，目标是找到左边第一条白色边缘线
    matrix = num
    # 按列计算中位数
    medians = np.median(matrix, axis=0)
    # 找到中位数最大和第二大的列的索引
    max_median_index = np.argmax(medians)
    max2_median_index = np.argsort(medians)[-2]
    if max2_median_index < max_median_index:
       max_median_index = max2_median_index
    # 输出具有最小中位数的列
    return max_median_index
def easyocr(slider,back):
    start,end = size(slider)
    #读取滑块和背景的灰度图
    slider = Image.open(io.BytesIO(slider)).convert('L')
    back = Image.open(io.BytesIO(back)).convert('L')
    #转化为矩阵并按照滑块的高度切割
    nupslide = np.array(slider)[start:end,:]
    nupback = np.array(back)[start:end,:]
    #找白线
    index_s = searchwhite(nupslide)
    index_b = searchwhite(nupback)
    index_sb = index_b-index_s
    return index_sb
    

