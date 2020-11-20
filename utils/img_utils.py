
# encoding: utf-8  

import cv2
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import VideoFileClip


def one_pic_to_video(image_path, output_video_path, fps, time):
    """
    一张图片合成视频
    one_pic_to_video('./../source/mount.jpg', './../source/output.mp4', 25, 30)
    :param path: 图片文件路径
    :param output_video_path:合成视频的路径
    :param fps:帧率
    :param time:时长
    :return:
    """

    image_clip = ImageClip(image_path)
    img_width, img_height = image_clip.w, image_clip.h

    # 总共的帧数
    frame_num = (int)(fps * time)

    img_size = (int(img_width), int(img_height))

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    video = cv2.VideoWriter(output_video_path, fourcc, fps, img_size)

    for index in range(frame_num):
        frame = cv2.imread(image_path)
        # 直接缩放到指定大小
        frame_suitable = cv2.resize(frame, (img_size[0], img_size[1]), interpolation=cv2.INTER_CUBIC)

        # 把图片重复写进视频
        video.write(frame_suitable)

    # 释放资源
    video.release()

    return VideoFileClip(output_video_path)

if __name__ == '__main__':
    one_pic_to_video('./../source/img/mount.jpg', './../source/video/output.mp4', 25, 30)
