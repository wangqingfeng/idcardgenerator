# coding:utf-8
import os
import random
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageEnhance
import cv2


g_num_saved = 0
# if getattr(sys, 'frozen', None):
#     base_dir = os.path.join(sys._MEIPASS, 'usedres')
# else:
#     base_dir = os.path.join(os.path.dirname(__file__), 'usedres')


POSITION = ('LEFTTOP','RIGHTTOP','CENTER','LEFTBOTTOM','RIGHTBOTTOM')
PADDING = 10
MARKIMAGE = '/data/back/idcardgenerator/resource/fx.png'

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position=POSITION[4], opacity=1):
    """Adds a watermark to an image."""
    # im = Image.open(imagefile)
    # mark = Image.open(markfile)
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    # mark = mark.rotate(random.randint(-6,6))
    if im.mode != 'RGBA':
        # print(im.mode)
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'title':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    # elif position == POSITION[0]:
    #     #lefttop
    #     position = (random.randint(PADDING,int(im.size[0]/4)), random.randint(-int(mark.size[1]/2),int(mark.size[1]/2)))
    #     layer.paste(mark, position)
    # elif position == POSITION[1]:
    #     #righttop
    #     position =  (random.randint(int(im.size[0]/3),int(im.size[0]-PADDING)), random.randint(-int(mark.size[1]/2),int(mark.size[1]/2)))
    #     layer.paste(mark, position)
    # elif position == POSITION[2]:
    #     #center
    #     position = (random.randint(int(im.size[0]/4),int(im.size[0]*3/4)),random.randint(-10,int(mark.size[1]/2)))
    #     layer.paste(mark, position)
    # elif position == POSITION[3]:
    #     #left bottom
    #     position = (random.randint(20,im.size[0] - mark.size[0]-PADDING),random.randint(40,im.size[1] - mark.size[1]-PADDING),)
    #     layer.paste(mark, position)
    else:
        #right bottom (default)
        position = (random.randint(242,1230), random.randint(483,1100),)
        layer.paste(mark, position)
        position = (random.randint(242,1230), random.randint(1800,2600),)
        layer.paste(mark, position)

    # composite the watermark with the layer
    imgrgba = Image.composite(layer, im, layer)
    return imgrgba.convert('RGB')    

def get_all_folder_file_list(dirfullpath,listfile):
    img_list_dir = os.listdir(dirfullpath)
    for item in img_list_dir:
        if os.path.isfile(os.path.join(dirfullpath,item)):
            listfile.append(os.path.join(dirfullpath,item))
        elif os.path.isdir(os.path.join(dirfullpath,item)):
            get_all_folder_file_list(os.path.join(dirfullpath,item),listfile)
        else:
            pass

def readTxt (filelisttxt)            :
    list_allline = []
    f = open(filelisttxt)
    line = f.readline()
    while line:
        line = line.strip('\n')
        list_allline.append(line)
        line = f.readline()
    f.close()
    return list_allline

def read_txt_to_list(filename_txt):
    imglist = []
    print("========================================")
    if os.path.isfile(filename_txt):
        imglist = readTxt(filename_txt)
    elif os.path.isdir(filename_txt):
        get_all_folder_file_list(filename_txt,imglist)
    else:
        pass
        print("Error: 不支持的路径输入 -> %s" %(filename_txt))
    print("Deal with folder/txt file: %s[size: %s]" %(filename_txt, len(imglist)))
    return imglist

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

def generator(name, sex, nation, year, mon, day, addr, idn, org, life,savedir):
    global g_num_saved
    g_num_saved += 1

    # fname = askopenfilename(parent=root, initialdir=os.getcwd(), title=u'选择头像')
    # print fname
    # im = Image.open(os.path.join(base_dir, 'empty.png'))
    # avatar = Image.open(fname)  # 500x670
    im = Image.open("/data/back/idcardgenerator/resource/empty.png")
    base_dir = '/data/back/idcardgenerator/resource'

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
    #     im = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))
    # else:
    #     avatar = avatar.resize((500, 670))
    #     avatar = avatar.convert('RGBA')
    #     im.paste(avatar, (1500, 690), mask=avatar)
    #     #im = paste(avatar, im, (500, 670), (690, 1500))
        
    saved_labelname_write = str(g_num_saved) + '_' + name +'_'+sex+'_'+nation + '_'+year+'_'+mon+'_'+day+'_'+addr+'_'+idn+'_'+org+'_'+life+'\n'
    saved_labelname = str(g_num_saved) + '.png'
    save_label_filename= savedir + '/label_name.txt'
    f = open(save_label_filename,'a+')
    f.write(saved_labelname_write)
    f.close()

    saved_full_path = savedir + '/color/'
    if not os.path.exists(saved_full_path):
        os.mkdir(saved_full_path)
    saved_full_path += saved_labelname
    im.save(saved_full_path)
    saved_full_path = savedir + '/gray/'
    if not os.path.exists(saved_full_path):
        os.mkdir(saved_full_path)
    imgMark = Image.open(MARKIMAGE)
    w_m = int(imgMark.size[0]*1.78)
    h_m = int(imgMark.size[1]*1.78)
    imgMark = imgMark.resize((w_m,h_m))
    imgray = watermark(im, imgMark, POSITION[random.randint(0, 4)], random.randint(5,9)/10.0).convert('L')
    # imgray = imgray.point(lambda p: p * random.randint(5,10)/10.0)
    imgray.save(os.path.join(saved_full_path,saved_labelname))

def create_idcard_whole(filanme_xs,filename_xm,filename_mz,filename_zz,savedir):
    list_xs = read_txt_to_list(filanme_xs)
    list_xm = read_txt_to_list(filename_xm)
    list_mz = read_txt_to_list(filename_mz)
    list_zz = read_txt_to_list(filename_zz)
    # list_org = read_txt_to_list(filename_org)

    # list_idcard_top = read_txt_to_list(filename_idcardtop)
    # list_idcard = []
    # for item in list_idcard_top:
    #     item_id = item.replace('"','')
    #     item_id = item_id.split(',')[0]
    #     list_idcard.append(item_id)

    # 
    for item in list_zz:
        XS = random.choice(list_xs)
        xm1 = random.choice(list_xm)
        xm2 = random.choice(list_xm)
        name = XS + xm1+xm2

        sex = random.choice(['男','女'])
        nation = random.choice(list_mz)

        year = random.randint(1937,2020)
        mon = random.randint(1,12)
        day = random.randint(1,31)

        addr = item.split(',')[0]
        # idnum get 
        # ida_ahead = random.choice(list_idcard)
        ida_ahead = item.split(',')[1]
        year_str = str(year)
        mon_str = str(mon)
        if mon < 10:
            mon_str = '0' + mon_str
        day_str = str(day)
        if day < 10:
            day_str = '0' + day_str

        idn = ida_ahead + year_str+mon_str+day_str
        id_sex = '0'
        if sex == '男':
            id_sex = random.choice(['1','3','5','7','9'])
        else:
            id_sex = random.choice(['0','2','4','6','8'])
        id_2num = str(random.randint(10,100))
        id_last = random.choice(['0','1','2','3','4','5','6','7','8','9','X'])
        if random.randint(0,20)%10 == 0:
            idn += (id_sex)
        else:
            idn += (id_2num+id_sex+id_last)
        # 
        org = item.split(',')[-1]
        life_start = random.randint(year+1,2021)
        life_mon = random.randint(1,12)
        life_day = random.randint(1,31)

        life_mon_str = str(life_mon)
        life_day_str = str(life_day)
        if life_mon < 10 :
            life_mon_str = '0' + life_mon_str
        if life_day < 10:
            life_day_str = '0' + life_day_str

        life_start_str = str(life_start) +'.'+life_mon_str+'.'+life_day_str
        life_end_str = ''
        if life_start - year < 16:
            life_end_str = str(life_start+5)+'.'+life_mon_str+'.'+life_day_str
        elif life_start - year < 26:
            life_end_str = str(life_start+10)+'.'+life_mon_str+'.'+life_day_str
        elif life_start - year < 46:
            life_end_str = str(life_start+20)+'.'+life_mon_str+'.'+life_day_str
        else:
            life_end_str = '长期'
        life = life_start_str +'-'+life_end_str
        # 
        generator(name,sex,nation,year_str,mon_str,day_str,addr,idn,org,life,savedir)


if __name__ == '__main__':
    filename_xs = '/data/back/idcardgenerator/resource/x.txt'
    filename_name = '/data/back/idcardgenerator/resource/name.txt'
    filename_mz = '/data/back/idcardgenerator/resource/mz.txt'
    filename_zzall = '/data/OCR/省市县街道数据/address_wholeall.txt'
    # /data/back/idcardgenerator/resource/name.txt

    savedir = '/data/data/SFZ/身份证比赛数据/create_whole'
    create_idcard_whole(filename_xs,filename_name,filename_mz,filename_zzall,savedir)
