# coding:utf-8
import re
import time
from urllib import request
 
 
class PL:
    def __init__(self):  # 定义初始信息
        # 定义http头信息
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
            "referer": "http://music.163.com/song?id=4466775&market=baiduqk"
        }
 
    # 使用request打开api接口，获取数据
    def single(self, song_id):
        offset = 0
        comment = []
        # 爬虫爬35*28条评论
        for i in range(28):
            # api里limit对应的是每页多少条，offset对应的是页数
            single_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_'+str(song_id)+'?limit35&offset='+str(offset)
            offset += 35
            # requst访问api接口获取数据
            html_url = request.Request(url=single_url, headers=self.headers)
            html = request.urlopen(html_url)
            data = html.read()
            # 转换获取数据的格式为str
            str_data = data.decode()
            # 已"content":"为分隔符，分割获取的字符串
            split_data = str_data.split('"content":"')
            # 循环处理所有字符
            for i in split_data:
                data_split = i.split('","')
                if data_split[0] not in comment:
                    comment.append(data_split[0])
            pl = open(r'C:\Users\liushipeng\Documents\pl.txt', 'a+')
            # 由于评论里有些表情字符无法储存到文本里，删除所有无法处理的字符，方法比较笨
            for i in comment:
                try:
                    pl.write(i + '\n')
                except Exception as error:
                    data = self.error_gbk(error, i)
                    try:
                        pl.write(data + '\n')
                    except Exception as error:
                        data1 = self.error_gbk(error, data)
                        try:
                            pl.write(data1 + '\n')
                        except Exception as error:
                            data2 = self.error_gbk(error, data1)
                            try:
                                pl.write(data2 + '\n')
                            except:
                                pass
            time.sleep(2)
            pl.close()
 
    # 清除写入文本里时报错的字符
    def error_gbk(self, error, content):
        u = str(error).split(" '")
        u_error = str(u[1]).split("' ")
        result = re.sub(u_error[0], '', content)
        return result
 
 
if __name__ == '__main__':
    # 通过歌曲id来访问歌曲对应的API接口
    song_id = '1365221826'
    p = PL()
    p.single(song_id)