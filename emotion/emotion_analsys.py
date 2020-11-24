# encoding:utf-8
#use  baiducloud api

'''
情绪二级分类标签；客服模型正向（thankful感谢、happy愉快）、
客服模型负向（complaining抱怨、angry愤怒）；闲聊模型正向（like喜爱、happy愉快）、
闲聊模型负向（angry愤怒、disgusting厌恶、fearful恐惧、sad悲伤）
'''
import requests
import json


def emotion_class(inputText,access_token):
    url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=' + access_token
    header = {'Content-Type ': 'application/json'}
    body = {'text': inputText}
    requests.packages.urllib3.disable_warnings()
    res = requests.post(url=url, data=json.dumps(body), headers=header, verify=False)
    if res.status_code == 200:
        info = json.loads(res.text)
        info_contenct=info['items'][0]
        return info_contenct
    else:
        return 'neutral'

# 情感分析
def getEmotion(inputText, access_token):

    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?access_token=' + access_token
    header = {'Content-Type	': 'application/json'}
    body = {'text': inputText}
    requests.packages.urllib3.disable_warnings()
    res = requests.post(url=url, data=json.dumps(body), headers=header, verify=False)
    if res.status_code == 200:
        info = json.loads(res.text)
        print(info)
        if 'items' in info and len(info['items']) > 0:
            if len(info['items'][0]['subitems'])>0:
                sentiment = info['items'][0]['subitems'][0]['label']
                print(inputText + '  情感分析结果:%s'%sentiment)
                return sentiment
            else:
                #emotion_class()
                print(inputText + '  情感分析结果:中性')
                return 'neutral'
        else:
            print(inputText + '  情感分析结果:中性')
            return 'neutral'
# 获取token
def getToken(path='../secret.json'):
    with open(path,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
    App_Key=json_data['App_Key']
    Secret_Key=json_data['Secret_Key']    
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + App_Key + '&client_secret=' + Secret_Key
    response = requests.get(host)

    if response.status_code == 200:
        info = json.loads(response.text)  # 将字符串转成字典
        access_token = info['access_token']  # 解析数据到access_token
        return access_token
    return ''

# 主函数
def analsys(inputText=''):
    accessToken = getToken()
    emotion=getEmotion(inputText, accessToken)
    return emotion

if __name__ == '__main__':
    analsys("test")
