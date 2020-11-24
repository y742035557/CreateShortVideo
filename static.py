#encoding: utf-8  
import os
import re
import datetime
from moviepy.video import fx

from utils.img_utils import *
from utils.video_utils import *
from utils.file_utils import *
from utils.info_utils import *



class Static_Video(object):

    def __init__(self, video_raw_path, desc):
        self.video_raw_path = video_raw_path
        self.desc = desc
        self.video_clip = None
        self.audio = None
        self.video_width = 0
        self.video_height = 0
        self.fps = 25
        self.time = 30
        self.font_params = {'size': 100,'color': 'red','kerning': 5,'position': 0}

   
    def find_new_file(self,dir='./source/img'):
        '''查找目录下最新的文件'''
        file_lists = os.listdir(dir)
        file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn) if not os.path.isdir(dir + "\\" + fn) else 0)
        print('最新文件： ' + file_lists[-1])
        file = os.path.join(dir, file_lists[-1])
        return file


    def run_static(self):

        position1, position2 = self.__get_frame(3)

        new_img_name=self.find_new_file('./source/img/')

        new_audio_name=self.find_new_file('./source/audio/')

        image_video_clip = one_pic_to_video(new_img_name, './source/temp_img_video.mp4', self.fps, self.time)

        self.audio= AudioFileClip(new_audio_name).subclip(0, image_video_clip.duration - 0)

        #生成描述信息
        desc_text_clip = generate_text_clip(self.desc, self.font_params, image_video_clip.duration)

        #desc_text_clip=set_list_text_clip(txt_, self.font_params, image_video_clip.duration)
        #视频加入描述信息
        video_with_text_clip = video_with_text(image_video_clip, desc_text_clip)

        #视频加入音频，并删除临时文件
        self.video_with_audio(video_with_text_clip)

    
    def __get_frame(self, time):

        position1 = (0, 0)
        position2 = (self.video_width, 1080)

        return position1, position2

    def video_with_audio(self, video_with_text_clip):
        """
        视频合成音频，并删除临时文件
        :return:
        """
        # 设置视频音频，并写入到文件中去
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')

        video_with_text_clip.set_audio(self.audio).write_videofile(now+"_output.mp4",
                                                                   codec='libx264',
                                                                   audio_codec='aac',
                                                                   temp_audiofile='temp-audio.m4a',
                                                                   remove_temp=True
                                                                   )
        #删除所有的临时文件
        del_temp_file("./source/")


if __name__ == '__main__':
    # 原视频文件 没用
    video_source = './source/'
    text_info = get_info()
    video_re = Static_Video(video_source, 'a,b,C.e,u')
    video_re.run_static()
