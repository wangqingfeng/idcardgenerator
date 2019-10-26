# coding:utf-8
import os
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw
import cv2
import numpy as np
try:
    from Tkinter import *
    from ttk import *
    from tkFileDialog import *
    from tkMessageBox import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.filedialog import *
    from tkinter.messagebox import *

g_num_saved = 0
if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'usedres')
else:
    base_dir = os.path.join(os.path.dirname(__file__), 'usedres')


def changeBackground(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    #lower_blue = np.array([78, 43, 46])
    #upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back

def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg

def generator():
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn, eorg, elife, ebgvar
    name = ename.get()
    sex = esex.get()
    nation = enation.get()
    year = eyear.get()
    mon = emon.get()
    day = eday.get()
    org = eorg.get()
    life = elife.get()
    addr = eaddr.get()
    idn = eidn.get()

    global g_num_saved
    g_num_saved += 1

    # fname = askopenfilename(parent=root, initialdir=os.getcwd(), title=u'选择头像')
    # print fname
    im = PImage.open(os.path.join(base_dir, 'empty.png'))
    # avatar = PImage.open(fname)  # 500x670

    name_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 72)
    other_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 60)
    bdate_font = ImageFont.truetype(os.path.join(base_dir, 'fzhei.ttf'), 60)
    id_font = ImageFont.truetype(os.path.join(base_dir, 'ocrb10bt.ttf'), 72)

    draw = ImageDraw.Draw(im)
    draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
    draw.text((630, 840), sex, fill=(0, 0, 0), font=other_font)
    draw.text((1030, 840), nation, fill=(0, 0, 0), font=other_font)
    draw.text((630, 980), year, fill=(0, 0, 0), font=bdate_font)
    draw.text((950, 980), mon, fill=(0, 0, 0), font=bdate_font)
    draw.text((1150, 980), day, fill=(0, 0, 0), font=bdate_font)
    start = 0
    loc = 1120
    while start + 11 < len(addr):
        draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
        start += 11
        loc += 100
    draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
    draw.text((950, 1475), idn, fill=(0, 0, 0), font=id_font)
    draw.text((1050, 2750), org, fill=(0, 0, 0), font=other_font)
    draw.text((1050, 2895), life, fill=(0, 0, 0), font=other_font)
    
    # if ebgvar.get():
    #     avatar = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
    #     im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
    #     im = changeBackground(avatar, im, (500, 670), (690, 1500))
    #     im = PImage.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))
    # else:
    #     avatar = avatar.resize((500, 670))
    #     avatar = avatar.convert('RGBA')
    #     im.paste(avatar, (1500, 690), mask=avatar)
    #     #im = paste(avatar, im, (500, 670), (690, 1500))
        

    im.save('/data/back/idcardgenerator/create/color.png')
    im.convert('L').save('/data/back/idcardgenerator/create/bw.png')


if __name__ == '__main__':

