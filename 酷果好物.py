#   --------------------------------注释区--------------------------------
#   https://www.kugua.com/wxapp/openidLogin找refresh_token和openid
#   环境变量:yyf_kghw ，格式token&openid,多号@分割或者直接填到cookie
#   corn: 每天跑一次就行 22 7 * * *
#   建议把请求头替换成自己的UA，填进ua里，不改也行挑选随机幸运儿封号
#   by fisher 2024.06.30
exchange =True #助力开关 开启True 关闭False
cookie ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE3MTk5MTc0MTgsImRhdGEiOnsidWlkIjoyNDA4NSwiYXBwaWQiOiJ3eDFmOWZjOGU3OWZjYmNlMTYifSwic2NvcGVzIjoicm9sZV9yZWZyZXNoIiwiZXhwIjoxNzIyNTA5NDE4fQ.Vj1Jpmoq8B-RbPeqly-4YeZcvqfJhiC85zKnNAXv0T0&oWvZH5PZrYb0rwgmKojb-D9fMYbE@eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE3MjAwMTUzOTYsImRhdGEiOnsidWlkIjoyNDA4NCwiYXBwaWQiOiJ3eDFmOWZjOGU3OWZjYmNlMTYifSwic2NvcGVzIjoicm9sZV9yZWZyZXNoIiwiZXhwIjoxNzIyNjA3Mzk2fQ.gItgAf0W6TzRubtvVfkebqrwv3Gu2mjUS9WHFfD6Thc&oWvZH5Muh_czp4SnX6do5ukSucE8"
ua = ""
debug = 0
import requests
import json
import os
import time
import random
class yyf():
    def __init__(self,cookie):
        self.authority = "https://www.kugua.com"
        cookie = cookie.split("&")
        self.cookie = cookie[0]
        self.data = {
        "appid": "wx1f9fc8e79fcbce16",
        "token": "",
        "openid": cookie[1]
        }
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/599.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/599.36 MicroMessenger/7.0.20.1781(0x6700166B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11)XWEB/9885",
        'Content-Type': "application/json",
        'xweb_xhr': "1",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://servicewechat.com/wx1f9fc8e79fcbce16/94/page-frame.html",
        'accept-language': "zh-CN,zh;q=0.9"
        }
        if ua:
            self.headers['User-Agent'] = ua
    def get_token(self):
        url = f"{self.authority}/wxapp/refreshToken"
        data = {
        "appid": "wx1f9fc8e79fcbce16",
        "openid": "oWvZH5PZrYb0rwgmKojb-D9fMYbE",
        "refresh_token": self.cookie
        }
        respone = requests.post(url,headers=self.headers,json=data).json()
        if respone["status"] == "0000":
            self.data['token'] = respone["data"]["token"]
            print(f"刷新token成功,token={self.data['token']}")
        else:
            print(f"刷新token失败{respone}")   
            exit()    
    def signlist(self):
        url = f"{self.authority}/wxapp/inflatedv3/signList"
        response = requests.post(url, headers=self.headers, json=self.data).text
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = json.loads(response)
        if response["codemsg"] == "success":
            if response["data"]["isSign"] == 0 and response["data"]["show"] == True:
                print(f"查询成功,今日未签到,去签到")
                time.sleep(1)
                self.signin()
            else :
                print("查询成功,今日已签到")
        else:
            print(f"查询失败{response}")
    def signin(self):
        url = f"{self.authority}/wxapp/inflatedv3/popUpRedEnvelopes"
        data = {
        "type": 1,
        "invite_id": "",
        "code_ticket": "",
        "count": ""
        }
        data.update(self.data)
        response = requests.post(url, headers=self.headers, json=data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()    
        if response["codemsg"] == "success":
            dilogId = response["data"]["dialogId"]
            print(f"签到成功,获得{response['data']['amount']}元红包")
            if dilogId == "":
                print("没有弹窗红包")
            else:
                time.sleep(1)
                self.receiveRedEnvelopes(dilogId)
        else:
            print(f"签到失败{response}")
    def receiveRedEnvelopes(self,dilogId):
        url = f"{self.authority}/wxapp/inflatedv3/receiveRedEnvelopes"
        data = {"dialogId": dilogId}
        data.update(self.data)
        response = requests.post(url, headers=self.headers, json=data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response['status'] == "0000":
            print("领取成功")
        else:
            print(f"领取失败,{response}")
    
    def withdrawlist(self):
        url = f"{self.authority}/wxapp/withdrawalv3/index"
        response = requests.post(url, headers=self.headers, json=self.data,)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response["codemsg"] == "success":
            withdrawalId = response["data"]["withdrawalList"][0]["withdrawalId"]
            time.sleep(1)
            self.withdraw(withdrawalId)
    def withdraw(self,withdrawalId):
        url = f"{self.authority}/wxapp/withdrawal/withdrawal"
        data = {"withdrawalId":withdrawalId}
        data.update(self.data)
        response = requests.post(url, headers=self.headers, json=data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response["status"] == "0000":
            print("提现成功")
        else:
            print(f"提现失败，{response}")
    def daliytask(self):
        url = f"{self.authority}/wxapp/dailyTaskv2/index"
        response = requests.post(url, headers=self.headers, json=self.data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response["codemsg"] == "success":
           tasklist = response["data"]
           print(f"一共有{len(tasklist)}个任务")
           for i in tasklist:
               type = i["inflated_type"]
               if int(i["count"]) < i["limit_num"]:
                   name = i["task_name"]
                   print(f"任务{name}未完成,去完成")
                   self.taskredEnvelopes(type)
                   time.sleep(11)
    def taskredEnvelopes(self,type):
        url = f"{self.authority}/wxapp/inflatedv3/popUpRedEnvelopes"
        data = {"type": type}
        data.update(self.data)
        response = requests.post(url,  headers=self.headers, json=data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response["codemsg"] == "success":
            amount = response["data"]["amount"]
            dialogId = response["data"]["dialogId"]
            print(f"任务完成,获得{amount}元红包")
            self.receiveRedEnvelopes(dialogId)
        else:
            print(response["codemsg"])

    def helplist(self):
        url = f"{self.authority}/wxapp/inflatedv3/list"
        response = requests.post(url, headers=self.headers, json=self.data)
        if debug == 1:
            request = response.request
            print(f"请求url:{request.url}")
            print(f"请求头:{request.headers}")
            print(f"请求体:{request.body}")
            print(f"响应体:{response.text}")
        response = response.json()
        if response["codemsg"] == "success":
            helplist = response["data"]["list"]
            num = response['data']["shareUserNum"]
            print(f"一共有{num}人助力")
            
        else:
            print(f"查询助力失败,{response}")

    def task(self):
        print("🎉️刷新token")
        self.get_token()
        print("===========================")
        time.sleep(1)
        print("🎉️开始执行[签到]")
        self.signlist()
        print("===========================")
        time.sleep(1)
        print("🎉️开始执行[日常任务]")
        self.daliytask()
        print("===========================")
        time.sleep(1)
        print("🎉️开始执行[提现]")
        self.withdrawlist()
        print("===========================")
        print("🎉️开始查询[助力]")
        self.helplist()
        time.sleep(1)

if __name__ == '__main__':
    
    if not cookie:
        cookie = os.getenv("yyf_kghw")
        if not cookie:
            print("请设置环境变量:yyf_kghw")
            exit()
    cookies = cookie.split("@")
    print(f"一共获取到{len(cookies)}个账号")
    i = 1
    for cookie in cookies:
     print(f"\n--------开始第{i}个账号--------")
     t = 1#random.randint(1, 300)
     print(f"随机等待{t}秒")
     time.sleep(t)
     main = yyf(cookie)
     main.task()
     print(f"--------第{i}个账号执行完毕--------")
     i += 1

