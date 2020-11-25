

from moviepy.editor import *

'''基本方法
for method in [
    "afx.audio_fadein",
    "afx.audio_fadeout",
    "afx.audio_normalize",
    "afx.volumex",
    "transfx.crossfadein",
    "transfx.crossfadeout",
    "vfx.crop",
    "vfx.fadein",
    "vfx.fadeout",
    "vfx.invert_colors",
    "vfx.loop",
    "vfx.margin",
    "vfx.mask_and",
    "vfx.mask_or",
    "vfx.resize",
    "vfx.rotate",
    "vfx.speedx",
]:
https://blog.csdn.net/ucsheep/article/details/82787043
'''

def special_effects(inputfile,outputfile):
    video=VideoFileClip(inputfile)
    w,h=video.size
    subvideo=video.subclip(0,8).fadein(8,(0.5,1,1))
    subvideo1=video.subclip(8,video.duration-6)
    subvideo2=video.subclip(video.duration-6).fadeout(3,(0,0,0))

    txt = TextClip('---YQL python auto create',font='simhei.ttf',fontsize=40)
    final_clip =  concatenate_videoclips([subvideo,subvideo1,subvideo2])
    painting_txt = (CompositeVideoClip([final_clip,txt.set_pos((w/2,h-100))]).set_duration(final_clip.duration))
    


    #w,h=subvideo1.size
    #subvideo1.mask.get_frame=lambda t:circle(screensize(subvideo1.w,subvideo1.h),center=(subvideo1.w/2,subvideo1.h/4),radius=max(0,int(800-200*t)),col1=1,col2=0,blur=4)
    #trans=ImageClip('mount.jpg').resize(video.size)
    #resultvideo=concatenate_videoclips([subvideo,subvideo1,subvideo2])
    #resultvideo.write_videofile(outputfile)
    painting_txt.write_videofile(outputfile)
if __name__ == '__main__':
    special_effects('202011202324_output.mp4','done_temp.mp4')