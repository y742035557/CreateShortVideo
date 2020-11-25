import os
import re
import datetime
from moviepy.editor  import *
#from moviepy.video import fx
import random
from PIL import Image, ImageDraw, ImageFont
from emotion.emotion_analsys import *

from utils.img_utils import *
from utils.video_utils import *
from utils.file_utils import *
from utils.info_utils import *
from utils.effect_utils import *

def random_select_audio(path='./source/img',typ='mp3'):
    audio_list=[]
    for home, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(typ):
                print(filename)
                fullname = os.path.join(home, filename)
                audio_list.append(fullname)
    print(random.choice(audio_list))
    return random.choice(audio_list)

def video_with_audio(audio,video_with_text_clip):
    """
    视频合成音频，并删除临时文件
    :return:
    """
    # 设置视频音频，并写入到文件中去
    #now = datetime.datetime.now().strftime('%Y%m%d%H%M')

    video_with_text_clip.set_audio(audio).write_videofile("output.mp4",
                                                               codec='libx264',
                                                               audio_codec='aac',
                                                               temp_audiofile='temp-audio.m4a',
                                                               remove_temp=True
                                                               )
    #删除所有的临时文件
    del_temp_file("./source/")

    

def add_logo(words='我要发表心灵，而不公开隐私'):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！|…|（|）'
    dy=30
    y=100
    txt_list = re.split(pattern, words)
    video_path=random_select_audio('../video_source/','mp4')
    video_raw = VideoFileClip(video_path)
    times = video_raw.duration
    if times<=20:
        video_raw = concatenate_videoclips([video_raw,video_raw])
        video=video_raw
        times=times*2
        w,h=video_raw.w,video_raw.h
    else:
       w,h=video_raw.w,video_raw.h
       video = VideoFileClip(video_path).subclip(t_start=0,t_end=times)
   
    font = ImageFont.truetype("simhei.ttf", 100, encoding="utf-8")

    logos = []
    for i,txt in enumerate(txt_list):
        txt = re.sub(pattern,'',txt)
        text_width = font.getsize(txt)
        print(text_width)
        y = y+text_width[1]
        (x,y) = (int((w-text_width[0]/2)/2), y)
        try: 
            logo = (TextClip((txt), fontsize=45, font='Simhei', color='black')
                    .set_start(0).set_end(times) 
                    .set_pos((x,y)))

            logos.append(logo)
        except:
            print(txt)
            continue

    final = CompositeVideoClip([video, *logos])
    new_audio_name=random_select_audio('../music_source/')
    audio= AudioFileClip(new_audio_name).subclip(7, final.duration +7)
    video_with_audio(audio,final) 
    special_effects("output.mp4",now+"_output.mp4")

if __name__ == '__main__':
    text_info = get_info()
    transfor=transfor(text_info)
    emotion=analsys(text_info)
    add_logo(text_info+'.'+transfor)