#!/usr/bin/env python
# _*_ coding utf-8 _*_
from bs4 import BeautifulSoup
import requests


def dlimg_from_unsplash(url='https://unsplash.com/'):
    i = 0
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    header = {"User-Agent": ua}
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.text, 'lxml')

    img_class = soup.find_all('div', {"class": "IEpfq"})      
    for img_list in img_class:
        imgs = img_list.find_all('img')                         
        for img in imgs:
            src = img['src']                                   
            r = requests.get(src, stream=True)
            image_name = 'unsplash_' + str(i) + '.jpg'         
            i += 1
            with open('.././source/img/%s' % image_name, 'wb') as file: 
                for chunk in r.iter_content(chunk_size=1024):
                    file.write(chunk)
            return
if __name__ == "__main__":
    dlimg_from_unsplash()