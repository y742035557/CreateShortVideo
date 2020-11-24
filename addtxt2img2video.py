import cv2
import re
import numpy as np
import random
from utils.info_utils import *
from PIL import Image, ImageDraw, ImageFont
from utils.img_utils import *
from moviepy.video import fx
import os
import datetime
from utils.img_utils import *
from utils.video_utils import *
from utils.file_utils import *
from utils.info_utils import *
from emotion.emotion_analsys import *
from cutto import *
def random_select_audio(path='.source/img',typ='mp3'):
    audio_list=[]
    for home, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(typ):
                print(filename)
                fullname = os.path.join(home, filename)
                audio_list.append(fullname)
    print(random.choice(audio_list))
    return random.choice(audio_list)
    
def find_new_file(path='./source/img'):
    '''查找目录下最新的文件'''
    file_lists = os.listdir(path)
    file_lists.sort(key=lambda fn: os.path.getmtime(path + "\\" + fn) if not os.path.isdir(path + "\\" + fn) else 0)
    print('最新文件： ' + file_lists[-1])
    file = os.path.join(path, file_lists[-1])
    return file
def video_with_audio(audio,video_with_text_clip):
    """
    视频合成音频，并删除临时文件
    :return:
    """
    # 设置视频音频，并写入到文件中去
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')

    video_with_text_clip.set_audio(audio).write_videofile(now+"_output.mp4",
                                                               codec='libx264',
                                                               audio_codec='aac',
                                                               temp_audiofile='temp-audio.m4a',
                                                               remove_temp=True
                                                               )
    #删除所有的临时文件
    del_temp_file("./source/")


def addword2colorimg(words='我要发表心灵，而不公开隐私',W=1280,H=720):
    # Load image, define rectangle bounds
    image = cv2.imread(find_new_file())
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    dy=30
    y=150
    #image = np.zeros([H,W], dtype=np.uint8)
    H=image.shape[0]
    W=image.shape[1]
    pil_img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    txt_list = re.split(pattern, words)
    pilimg = Image.fromarray(pil_img)
    draw = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype("simhei.ttf", 100, encoding="utf-8") 

    for i,txt in enumerate(txt_list):
        text_width = font.getsize(txt)
        y = y+text_width[1]*1.5
        (x,y) = (int((W-text_width[0])/2), y)
        draw.text((x,y), txt, (255,255,255), font=font)
    
    #cv2img = cv2.cvtColor(np.array(pilimg),cv2.COLOR_RGB2BGR)
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    pilimg.save('./source/temp.jpg')

    image_video_clip=one_pic_to_video('./source/temp.jpg', './source/temp_img_video.mp4', 25, 60)
    new_audio_name=random_select_audio('../music_source/')
    audio= AudioFileClip(new_audio_name).subclip(4, image_video_clip.duration +4)
    video_with_audio(audio,image_video_clip) 
    special_effects(now+"_output.mp4",now+"_output.mp4")

def addword2binimg(words='我要发表心灵，而不公开隐私',W=1280,H=720):
    # Load image, define rectangle bounds
    #image = cv2.imread('1.jpg')
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    dy=30
    y=150
    image = np.zeros([H,W], dtype=np.uint8)
    txt_list = re.split(pattern, words)
    pilimg = Image.fromarray(image)
    draw = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype("simhei.ttf", 45, encoding="utf-8") 

    for i,txt in enumerate(txt_list):
        text_width = font.getsize(txt)
        y = y+text_width[1]*2
        (x,y) = (int((W-text_width[0])/2), y)
        draw.text((x,y), txt, 255, font=font)

    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    pilimg.save('./source/temp.jpg')
    image_video_clip=one_pic_to_video('./source/temp.jpg', './source/temp_img_video.mp4', 25, 60)
    new_audio_name=random_select_audio('../music_source/')
    audio= AudioFileClip(new_audio_name).subclip(4, image_video_clip.duration - 0)
    video_with_audio(audio,image_video_clip)
    special_effects(now+"_output.mp4",now+"_output.mp4")
if __name__ == '__main__':

    text_info = get_info()
    emotion=analsys(text_info)
    print(emotion)
    #addword2binimg(text_info)
    addword2colorimg(text_info)