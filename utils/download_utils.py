import requests
import os
from bs4 import BeautifulSoup as bs
import re
import execjs
import json 
 
def getHtml(url):
    try:
        res = requests.get(url)
        return res.text
    except:
        return False
    
def getData(html):
    soup = bs(html,'html.parser')
    pics = soup.select('.photos a')
    print(len(pics))

    cmd_list = []
    for pic in pics:
        # print(pic['data-lazy'])
        cmds = 'you-get' +" "+ pic['data-lazy']
        cmd_list.append(cmds)
 
    for each in cmd_list:
        os.system(each)



class Down(object):
    def __init__(self):
        pass

    # 获取音乐文件的 ids 参数
    def getids(self):
        _headers = {'Referer': 'https://music.163.com/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        # 通过该链接，获取该页面的源码。
        html = requests.get('https://music.163.com/artist?id=3685', headers=_headers).text
        # 返回通过正则匹配获得的所有 ids 值。
        return re.findall('<li><a.href=.*?song.*?id=(.*?)">(.*?)</a></li>', html)

    # 计算 ids 的加密后的值（通过引入js文件，计算相应的值）
    def countids(self,ids):
        # 传入的参数，这里指的是获取音乐URL时，需要传入含有该音乐文件ids的字符串。
        ddd = '{"ids":"['+ids+']","level":"standard","encodeType":"aac","csrf_token":""}'
        # 导入js文件
        f=open('countdis.js','r',encoding='utf-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        f.close()
        # 运行js的 d 函数，并传入参数 ddd，也就是刚才定义的完整字符串，并返回。
        return ctx.call('d', ddd)

    # 获取到该音乐的真实 url 地址
    def geturl(self):
        # 因为该页面有多个音乐，会生成多个加密文本，所以这里迭代出来。
        for i in self.getids():
            # getids返回的是含有params 和 encSecKey两个加密文的，所以通过列表获取到相应的值。
            str=self.countids(i[0])
            encSecKey=str[0]
            params=str[1]
            _headers={'Referer':'https://music.163.com/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                      }
            _data={'encSecKey':encSecKey,'params':params}
            # 把获取到的两个参数值，提交到服务器，获得 URL 地址。
            urltext=requests.post('https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=',headers=_headers,data=_data).text
            _json=json.loads(urltext)
            url=_json['data'][0]['url']
            # 获得URL后，直接使用get下载音乐文件到本地。
            data=requests.get(url,_headers,stream=True)
            with open(i[1]+'.mp3','wb') as f:
                for j in data.iter_content(chunk_size=512):
                    f.write(j)
                print(i[1]+'.mp3 写出完毕!')

# 运行
if __name__=='__main__':
    bb=Down()
    bb.geturl()

