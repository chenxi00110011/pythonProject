import time
import hashlib
import hmac
import base64
import urllib.parse
import requests
import json

ding_talk_robots = dict(运营商测试组=dict(
    prefix='https://oapi.dingtalk.com/robot/send?access_token'
              '=d952b046915fc70190a19de3182b4240b89c22fa5d72c0dcfa27457e0bf89a06',
    secret= 'SEC000cdbc89beccd0d4da5fb1fef729244c32eb65c2d2408fe2e7b54de5499550f'),
    T41运营商项目烤机群=dict(
    prefix='https://oapi.dingtalk.com/robot/send?access_token'
           '=5254c4994726ff1a9cfdc218538a424149a251a24f674214b086200afc08df5c',
    secret='SECb8bf00029e0ef971dd78aab4fe87033c81b5053cb8a29d9a67e4817bf8fbf043'))


def countersign(ding_talk_robot):
    secret = ding_talk_robot['secret']
    prefix = ding_talk_robot['prefix']
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'{prefix}&timestamp={timestamp}&sign={sign}'
    return url


def send_dd_news(news_flag, url, news):
    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    # 钉钉消息格式，其中 news 就是我们要发送的具体内容
    if news_flag == 1:
        data = {
            "at": {"isAtAll": False},
            "text": {"content": news},
            "msgtype": "text"
        }
    elif news_flag == 2:
        data = {
            "at": {"atMobiles": ["15899785563"], "isAtAll": False},
            "text": {"content": news},
            "msgtype": "text"
        }
    elif news_flag == 3:
        data = {
            "msgtype": "markdown",
            "at": {"isAtAll": False},
            "markdown": {
                "title": "烤机日报",
                "text": f"# {time.strftime('%Y-%m-%d %H:%M')}烤机日报\n>"
                        f"![](http://kisyu.oicp.net:9001/{news})"}}
    else:
        data = {
            "msgtype": "markdown",
            "at": {"isAtAll": False},
            "markdown": {
                "title": "异常日志",
                "text": "### 异常日志下载:\n>"
                        f"#### [{news}](http://kisyu.oicp.net:9001/{news})"}}
    return requests.post(url=url, data=json.dumps(data), headers=headers).text

news = 'this is a test message'
url = countersign(ding_talk_robots['运营商测试组'])
send_dd_news(1,url,news)