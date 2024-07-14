#   --------------------------------注释区--------------------------------
#   https://www.52bjy.com/api/app/user.php?action=userinfo找username和auth值
#   变量:bjyhs ，格式：username#auth，多号@分割或者直接填到cookie
#   创建账号以后把完善信息手动填掉，否则会报错，福利→完善信息→去填写
#   corn: 每天跑一次就行 22 7 * * *
#   建议把请求头替换成自己的UA，填进ua里，不改也行挑选随机幸运儿封号
#   by fisher 2024.06.30
exchange =True #答题开关 开启True 关闭False
cookie =""
ua = ""

import requests
import json
import os
import hashlib
import time
from urllib.parse import urlencode
import random


cookie = ""#测试ck
class yyf():
    def __init__(self,cookie):
        
        self.key = "1f70a57fdf4061a7"
        self.scret = "eBRaFLkuJ5"
        self.username, self.auth = cookie.split('#') 
        self.token = ""     
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090819) XWEB/9129",
        'xweb_xhr': "1",
        'envconnection': "test",
        'content-type': "application/json",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://servicewechat.com/wxc525caf8e3a9e434/282/page-frame.html",
        'accept-language': "zh-CN,zh;q=0.9"
}
        if ua:
            self.headers['User-Agent'] = ua

    def md5(self,dict):
        sorted_dict = sorted(dict.items())
        str = urlencode(sorted_dict, doseq=True)+self.scret
        #print(f"加密前{str}")
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()
    
    def get_time(self):
        times = int(time.time())
        return times
    
    def userinfo(self):

        url = "https://www.52bjy.com/api/app/user.php"

        params = {
        'action': "userinfo",
        'app': "wx",
        'appkey': self.key,
        'auth': self.auth,
        'is_pop': "0",
        'username': self.username,
        'version': "2"
        }
        sign = self.md5(params)
        params['sign'] = sign
        headers = self.headers

        response = requests.get(url, params=params, headers=headers).json()
        if response['is_success'] == True:
            nickname = response['data']['nickname']
            print(f"查询信息{nickname}")
            self.token = response['data']['token']
            #print(f"token:{self.token}")
            credits = response['data']['credit']
            cash = response['data']['credit_to_cash']
            print(f"鲸鱼币:{credits},{cash}")
        else:
            print('获取失败',response['message'])

    def get_question(self):
        for i in range(0,10):
            url = "https://www.52bjy.com/api/app/question.php"

            params = {
            'action': "list",
            'appkey': self.key,
            'username': self.username,
            'version': "1"
            }
            sign = self.md5(params)
            params['sign'] = sign
            response = requests.get(url, params=params, headers=self.headers).json()
            if response['code'] == 200:
                i = response['data'][0]['index']
                q = response['data'][0]['question']
                print(f"获取到今天第{i}个问题:{q}")
                if i <= 10:
                   time.sleep(2)
                   self.answer()
                if i == 10:
                   break
            else:
                print('获取失败',response['message'])
                break
    
    def answer(self):
        url = "https://www.52bjy.com/api/app/question.php"
        
        params = {
        'action': "addcount",
        'appkey': self.key,
        'result': "1",
        'username': self.username,
        'version': "1"
        }
        sign = self.md5(params)
        params['sign'] = sign

        response = requests.get(url, params=params, headers=self.headers).json()
        if response['code'] == 200 and response['isSucess']:
            i = response['data']['index']
            r = response['data']['right']
            w = response['data']['wrong']
            print(f"回答正确{r}道题，回答错误{w}道题，当前第{i}题")
            if i == 10:
                print('今日答题结束，去领奖')
                self.credit(r)
        
    def credit(self,price):

        url = "https://www.52bjy.com/api/app/credit.php"

        params = {
        'action': "add",
        'appkey': self.key,
        'price': f"{price}",
        'reason': "每日答题",
        'timestamp': f"{self.get_time()}",
        'token': self.token,
        'type': "promotion",
        'username': self.username,
        'version': "4",
        }
        sign = self.md5(params)
        params['sign'] = sign

        headers = self.headers

        response = requests.get(url, params=params, headers=headers).json()
        if response['is_success'] == True:
            print("🎉️领取成功")
        else:
            print("❌️失败",response['message'])


    #def money(self):提现要短信验证码

    def signin(self):
        url = "https://www.52bjy.com/api/app/user.php"
        
        params = {
        'action': "qiandao",
        'app': "wx",
        'appkey': self.key,
        'auth': self.auth,
        'username': self.username
        }
        sign = self.md5(params)
        params['sign'] = sign
        response = requests.get(url, params=params, headers=self.headers).json()
        if response['is_success'] == True:
            print("🎉️签到成功")
        else:
            print("❌️签到失败",response['message'])
        time.sleep(2)
    def signinfo(self):
        url = "https://www.52bjy.com/api/app/user.php"

        params = {
        'action': "getsigninfo",
        'app': "wx",
        'appkey': self.key,
        'auth': self.auth,
        'username': self.username
        }
        sign = self.md5(params)
        params['sign'] = sign

        response = requests.get(url, params=params, headers=self.headers).json()
        if response['code'] == 200:
            day = response['data']['thisturn']
            print(f"签到天数{day}")
            if day == 7 and response['data']['status'] == 0:
                print("🎉️签满7天,去开盒")
                self.openbox()
    def openbox(self):
        url = "https://www.52bjy.com/api/app/user.php"

        params = {
        'action': "qiandaobox",
        'app': "wx",
        'appkey': self.key,
        'auth': self.auth,
        'merchant_id': "1",
        'username': self.username
        }
        sign = self.md5(params)
        params['sign'] = sign

        response = requests.get(url, params=params, headers=self.headers)
        print(f"获得鲸鱼币{response['data']['data']}")
    def tasklist(self):
        url = "https://www.52bjy.com/api/app/promotion.php"

        params = {
        'action': "tasklist",
        'app': "wx",
        'appkey': self.key,
        'merchant_id': "1",
        'type': "welfare",
        'username': self.username,
        }
        sign = self.md5(params) 
        params['sign'] = sign

        headers = self.headers

        response = requests.get(url, params=params, headers=headers).json()
        title = response['data'][0]['title']
        if response['is_success'] == True and title == "浏览小来小程序": 
            if response['data'][0]['is_done'] == 0:
                print("🎉️任务未完成，开始执行")
                time.sleep(2)           
                print(f"开始执行任务{title}")
                self.xiaolai()
        else:
            print("❌️查询任务失败",response['message'])
    
    def xiaolai(self):
        url = "https://www.52bjy.com/api/app/user.php"

        params = {
        'action': "task",
        'app': "wx",
        'appkey': self.key,
        'auth': self.auth,
        'type': "browse",
        'username': self.username,
        }
        sign = self.md5(params)
        params['sign'] = sign

        headers = self.headers

        response = requests.get(url, params=params, headers=headers).json()
        if response['is_success'] == True:
            print("🎉️",response['message'])
        else:
            print("❌️任务失败",response['message'])


    def task(self):
        self.userinfo()
        print("🎉️开始执行[签到]")
        self.signin()
        self.signinfo()
        print("===========================")
        print("🎉️开始执行[答题]")
        if exchange == True:
           self.get_question()
        else:
            print("❌️跳过答题")
        print("===========================")
        print("🎉️开始执行[任务]")
        self.tasklist()
        print("===========================")
        print("🎉️开始执行[查询信息]")
        self.userinfo()
        '''
        print("===========================")
        print("🎉️开始执行[提现]")
        self.money()
        '''

if __name__ == '__main__':
    
    if not cookie:
        cookie = os.getenv("bjyhs")
        if not cookie:
            print("请设置环境变量:bjyhs")
            exit()
    cookies = cookie.split("@")
    print(f"一共获取到{len(cookies)}个账号")
    i = 1
    for cookie in cookies:
     print(f"\n--------开始第{i}个账号--------")
     t = random.randint(1, 300)
     print(f"随机等待{t}秒")
     time.sleep(t)
     main = yyf(cookie)
     main.task()
     print(f"--------第{i}个账号执行完毕--------")
     i += 1
    