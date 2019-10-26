# -*- coding: utf-8 -*-
import random
import os
import cv2


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

def get_all_list_FromListUseKeycode(list_src,key_code):
    list_key_code = []
    for item in list_src:
        key_now = item.split(',')[-1]
        if key_now == key_code:
            list_key_code.append(item)

    return list_key_code


def get_all_keyvalue_filelist(filename_provinces,filename_cities,filename_areas,filename_streets,filename_villages,saved_list_txt):
    list_provinces = readTxt(filename_provinces)
    list_cities = readTxt(filename_cities)
    list_areas = readTxt(filename_areas)
    list_streets = readTxt(filename_streets)
    list_villages = readTxt(filename_villages)

    f = open(saved_list_txt,'w')

    #process  get whole adress
    str_address_whole = ''
    str_pro_use  = ''
    str_city_use = ''
    str_area_use = ''
    str_street_use  = ''
    str_village_use = ''
    for item_provinces in list_provinces:
        str_provinces = item_provinces.split(',')[-1]
        code_provinces = (item_provinces.split(',')[0])

        str_pro_use = str_provinces
        str_city_all = get_all_list_FromListUseKeycode(list_cities,code_provinces)
        for item_city in str_city_all:
            str_city = item_city.split(',')[1]
            code_city = item_city.split(',')[0]

            str_city_use = str_city
            str_area_all = get_all_list_FromListUseKeycode(list_areas,code_city)
            for item_area in str_area_all:
                str_area = item_area.split(',')[1]
                code_area = item_area.split(',')[0]

                str_area_use = str_area
                str_street_all = get_all_list_FromListUseKeycode(list_streets,code_area)
                if len(str_street_all) < 1:
                    # save the adress to file
                    str_address_whole = str_pro_use + str_city_use + str_area_use  + '\n'
                    str_address_whole = str_address_whole.replace('"','')
                    f.write(str_address_whole)
                for item_street in str_street_all:
                    str_street = item_street.split(',')[1]
                    code_street = item_street.split(',')[0]

                    str_street_use = str_street
                    str_village_all = get_all_list_FromListUseKeycode(list_villages,code_street)
                    if len(str_village_all) < 1:
                        #save the adress to file
                        str_address_whole = str_pro_use + str_city_use + str_area_use + str_street_use  + '\n'
                        str_address_whole = str_address_whole.replace('"','')
                        f.write(str_address_whole)
                        continue
                    for item_village in str_village_all:
                        str_village = item_village.split(',')[1]
                        code_village = item_village.split(',')[0]

                        str_village_use = str_village
                        #save the adress to file
                        str_address_whole = str_pro_use + str_city_use + str_area_use + str_street_use + str_village_use + '\n'
                        str_address_whole = str_address_whole.replace('"','')
                        f.write(str_address_whole)


def main_process_adress_fun():
    file_provinces = '/data/OCR/省市县街道数据/127.0.0.1-idoc_dev-20191025.sql_std_provinces'
    file_city = '/data/OCR/省市县街道数据/127.0.0.1-idoc_dev-20191025.sql_std_cities'
    file_area = '/data/OCR/省市县街道数据/127.0.0.1-idoc_dev-20191025.sql_std_areas'
    file_street = '/data/OCR/省市县街道数据/127.0.0.1-idoc_dev-20191025.sql_std_streets'
    file_village = '/data/OCR/省市县街道数据/127.0.0.1-idoc_dev-20191025.sql_std_villages'

    file_saved_txt = '/data/OCR/省市县街道数据/address_whole.txt'
    get_all_keyvalue_filelist(file_provinces,file_city,file_area,file_street,file_village,file_saved_txt)


if __name__ == "__main__":
    #get whole address
    main_process_adress_fun()