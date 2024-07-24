#   --------------------------------注释区--------------------------------
#   变量:xsyAccount ，格式：账号#密码#code，多号&分割
#   code是微信小程序的code，要自己领奖的时候抓包，https://op-api.cloud.jinhua.com.cn/api/study/get_red_envelop
#   不填也能运行，但是要自己领奖
#   corn: 每天跑两次 22 7,19 * * *
#   by fisher 2024.07.14
import hashlib
import time
import requests
import os
import random 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import urllib
import easyocr
import json
import hmac
debug=0
accounts = ''
def AES_Encrypt(dict, key):
    aes_str = json.dumps(dict,separators=(',', ':'),indent=None)
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')  
    encrypt_aes = aes.encrypt(pad_pkcs7)
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8').replace('\n','')
    return encrypted_text
def get_pic(url):
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'X-Requested-With': "com.zjonline.zhuji",
    'Sec-Fetch-Site': "same-site",
    'Sec-Fetch-Mode': "no-cors",
    'Sec-Fetch-Dest': "image",
    'Referer': "https://op-h5.cloud.jinhua.com.cn/",
    'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, headers=headers).content
    return response

def jm(password):
    public_key_base64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXizPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXFc+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlTHMlluw4ZYmnOwg+thwIDAQAB"
    public_key_der = base64.b64decode(public_key_base64)
    key = RSA.importKey(public_key_der)
    cipher = PKCS1_v1_5.new(key)
    password_bytes = password.encode('utf-8')
    encrypted_password = cipher.encrypt(password_bytes)
    encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')
    url_encoded_data = urllib.parse.quote(encrypted_password_base64)
    return url_encoded_data

def generate_random_uuid():
    # 设备号其实可以写死，保险起见选择随机生成
    uuid_str = '00000000-{:04x}-{:04x}-0000-0000{:08x}'.format(
        random.randint(0, 0xfff) | 0x4000, 
        random.randint(0, 0x3fff) | 0x8000,  
        random.getrandbits(32)
    )
    print(f'生成设备号：{uuid_str}')
    return uuid_str

def randomcode():
    randomcode =  '{:08x}-{:04x}-{:04x}-{:04x}-{:12x}'.format(
        random.getrandbits(32),
        random.randint(0, 0x3fff) | 0x8000,
        random.randint(0, 0x3fff) | 0x8000,
        random.randint(0, 0x3fff) | 0x8000,   
        random.getrandbits(48)    
    )
    return randomcode

def timestamp():
    return str(int(time.time() * 1000))


def getApiSign( deviceid, nonce, times, accountid, token, dict, scret):
    data = {
        "app_id": "uhzfzpj5l78yq6di",
        "device_id": deviceid,
        "nonce_str": nonce,
        "timestamp": times,
        "auth_id": accountid,
        "token": token,
        "source_type": "app",
        }
    data.update(dict)
    sorted_list = sorted(data.items())
    str = '&&'.join([f"{k}={v}" for k, v in sorted_list])+"&&"+scret
    sign = hashlib.sha256(str.encode()).hexdigest()
    #print("加密前："+str)
    #print("加密后："+sign)
    return sign
def login1():
    url = "https://passport.tmuyun.com/web/init"

    params = {
    'client_id': "50"
    }

    headers = {
    'User-Agent': "ANDROID;9;50;1.3.2;1.0;null;MI 9",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Cache-Control': "no-cache",
    'X-REQUEST-ID': randomcode(),
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    re_header = response.headers
    if data["code"] ==0:
        signature_key = data['data']['client']['signature_key']
        cookie = re_header.get('Set-Cookie')
        print(f'signature_key:{signature_key}\ncookie:{cookie}')
        return cookie,signature_key
    else:
        print("获取cookie失败")
        print(data)
        exit()

def login2():
    url = "https://passport.tmuyun.com/web/oauth/credential_auth"
    passcip = jm(password)
    payload = f"client_id=50&password={passcip}&phone_number={phone}"
    nonce = randomcode()
    signstr = f"post%%/web/oauth/credential_auth?client_id=50&password={passcip}&phone_number=19116317861%%{nonce}%%"
    sign = hmac.new(signature_key.encode('utf-8'), signstr.encode('utf-8'), 'sha256').hexdigest()
    headers = {
    'User-Agent': "ANDROID;9;50;1.3.2;1.0;null;MI 9",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Cache-Control': "no-cache",
    'X-REQUEST-ID': nonce,
    'X-SIGNATURE': sign,
    'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
    'Cookie': cookie
    }

    response = requests.post(url, data=payload, headers=headers).json()
    if response["code"] ==0:
       code = response["data"]['authorization_code']['code']
       print(f"code:{code}")
       return code
    else:
        print("code 获取失败")
        print(response)
        exit()

def login3():

    url = "https://vapp.tmuyun.com/api/zbtxz/login"

    payload = f"check_token=&code={code}&token=&type=-1&union_id="
    nonce = randomcode()
    times = timestamp()
    signstr = f"/api/zbtxz/login&&6698f34deb852e76c6f523a6&&{nonce}&&{times}&&FR*r!isE5W&&34"
    sign = hashlib.sha256(signstr.encode('utf-8')).hexdigest()
    headers = {
    'User-Agent': f"1.3.2;{deviceid};Xiaomi MI 9;Android;9;Release;6.10.0",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-SESSION-ID': '6698f34deb852e76c6f523a6',
    'X-REQUEST-ID': nonce,
    'X-TIMESTAMP': times,
    'X-SIGNATURE': sign,
    'X-TENANT-ID': "34",
    'Cache-Control': "no-cache"
    }
    response = requests.post(url, data=payload, headers=headers).json()

    if response["code"] ==0:
       accountid = response["data"]["account"]["id"]
       name = response["data"]["account"]["nick_name"]
       sessionid = response["data"]["session"]["id"]
       print(f"{name}登录成功")
       print(f"accountid:{accountid}\nsessionid:{sessionid}")
       return accountid,sessionid
    else:
        print("账号登录失败")
        print(response)
        exit()
def login4():

    url = "https://op-api.cloud.jinhua.com.cn/api/member/login"

    payload = {
    "debug": 0,
    "userId": ""
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, "35c782a2")

    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        token = response['data']['token']
        key = response['data']['key']
        print(f"token:{token}\nkey:{key}")
        return key,token
    else:
        print('获取token失败:下面是请求头')
        print(headers)
        print('下面是响应')
        print(response)
        exit()
def gettask():
    url = "https://op-api.cloud.jinhua.com.cn/api/study/detail"

    params = {
    'id': "192"
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, params, "35c782a2")
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    response = requests.get(url, params=params, headers=headers).json()

    if response["code"] ==0:
        lottery = response["data"]['lottery']['lottery_id']
        for i in response["data"]["levels"]:
            print(f"执行{i['name']}")
            taskid = i["id"]
            getarticle(taskid)
        return lottery
    else:
        print("查询任务失败")
        print(response)
        exit()
def getarticle(taskid):
    url = "https://op-api.cloud.jinhua.com.cn/api/study/level"
    params = {
    'id': str(taskid)
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, params, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization': "Bearer "+token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'access-type': "app",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, params=params, headers=headers).json()
    if response["code"] ==0:
        tasks = response['data']['tasks']
        completeTasks = response['data']['completedTasks']
        for task in tasks:
            if any(task['id'] == completed_task['task_id'] for completed_task in completeTasks):
                print(f"{task['id']}已完成,跳过")
                continue
            else:
                id = task['link'].split('&')[0].split('?id=')[1]
                tenanid = task['link'].split('tenantId=')[1].split('&')[0]
                titile = task['name']
                articleid = task['id']
                read = task['read']
                print(titile)
                if read == 0:
                    readarticle(id,tenanid)
                    time.sleep(4)
                    readtime(id,tenanid)
                    time.sleep(1)
                else:
                    print('已读')
                complete(articleid)
                time.sleep(1)
    else:
        print('get_article失败')
        print(response)
        exit()
def readarticle(id,tenanid):
    url = "https://vapp.tmuyun.com/api/article/detail"
    params = {
    'id': id
    }
    times = timestamp()
    nonce = randomcode()
    sign = hashlib.sha256(f"/api/article/detail&&{accesstoken}&&{nonce}&&{times}&&FR*r!isE5W&&{tenanid}".encode()).hexdigest()
    headers = {
    'User-Agent': f"3.1.0;{deviceid};Xiaomi MI 9;Android;9;Release;6.6.1",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'X-SESSION-ID': accesstoken,
    'X-REQUEST-ID': nonce,
    'X-TIMESTAMP': times,
    'X-SIGNATURE': sign,
    'X-TENANT-ID': tenanid,
    'X-ACCOUNT-ID': accountid,
    'Cache-Control': "no-cache"
    }

    response = requests.get(url, params=params, headers=headers).json()
    if response['code'] == 0:
        print(f"阅读{response['message']}")
    else:
        print('readarticle失败')
        print(response)
def readtime(id,tenanid):
    url = "https://vapp.tmuyun.com/api/article/read_time"
    params = {
    'channel_article_id': id,
    'is_end': "false",
    'read_time': "3000"
    }
    times = timestamp()
    nonce = randomcode()
    sign = hashlib.sha256(f"/api/article/read_time&&{accesstoken}&&{nonce}&&{times}&&FR*r!isE5W&&{tenanid}".encode()).hexdigest()
    headers = {
    'User-Agent': f"3.1.0;{deviceid};Xiaomi MI 9;Android;9;Release;6.6.1",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'X-SESSION-ID': accesstoken,
    'X-REQUEST-ID': nonce,
    'X-TIMESTAMP': times,
    'X-SIGNATURE': sign,
    'X-TENANT-ID': tenanid,
    'X-ACCOUNT-ID': accountid,
    'Cache-Control': "no-cache"
    }
    response = requests.get(url, params=params, headers=headers).json()
    if response['code'] == 0:
        print(f"上传阅读时间{response['message']}")
    else:
        print('readtime失败')
        print(response)
def complete(articleid):
    url = "https://op-api.cloud.jinhua.com.cn/api/study/task/complete"
    payload = {"id": articleid}
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization':'Bearer '+ token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        print(f"任务完成{response['message']}")
    else:
        print('complete失败')
        print(response)

def lotterycount(id):
    url = "https://op-api.cloud.jinhua.com.cn/api/lotterybigwheel/_ac_lottery_count"

    payload = {
    "id": id,
    "module": "study"
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization': "Bearer "+token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        count = response['data']['count']
        print(f"抽奖次数{count}")
        if response['data']['count'] == 0:
            print("抽奖次数不足")
        else:
            for i in range(count):
                msg = get_lottery(lottery)
                if msg == "请先选择验证码":
                   captcha(lottery)
                   time.sleep(2)
                   get_lottery(lottery)
                time.sleep(2)
    else:
        print('抽奖查询错误')
        print(response)
def get_lottery(lottery):
    url = "https://op-api.cloud.jinhua.com.cn/api/lotterybigwheel/_ac_lottery"

    payload = {
    "id": lottery,
    "app_id": "uhzfzpj5l78yq6di",
    "module": "study",
    "optionHash": ""
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization': "Bearer "+token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url,json=payload, headers=headers).json()
    if response['code'] == 0:
        print(f"抽奖结果：{response['data']['title']}")
    elif response['code'] == 10000:
        return response['message']
    else:
        print('抽奖错误：')
        print(response)
def captcha(lotteryid):
    url = "https://op-api.cloud.jinhua.com.cn/api/captcha/get"
    payload = {
    "activity_id": lotteryid,
    "module": "bigWheel"
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, "35c782a2")
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        print("获取验证码成功")
        jigsawImageUrl = response['data']['jigsawImageUrl']
        originalImageUrl = response['data']['originalImageUrl']
        secretKey = response['data']['secretKey']
        cap_token = response['data']['token']
        print(f"滑块链接是:{jigsawImageUrl}")
        print(f"背景链接是:{originalImageUrl}")
        print(f"加密密钥是:{secretKey}")
        print(f"cap_token是:{cap_token}")
        jigsawImage = get_pic(jigsawImageUrl)
        originalImage = get_pic(originalImageUrl)
        time.sleep(1)
        x=easyocr.easyocr(jigsawImage,originalImage)
        if x in range(0,310):
            print(f"返回的x偏移是:{x}")
            x_dict = {"x": x + 2,
                      "y": 5
                     }
            point = AES_Encrypt(x_dict,secretKey)
            print(f"AES加密结果是:{point}")
            check(lotteryid,point,cap_token)
        else:
            print("识别失败")
    else:
        print(headers)
        print('验证码获取错误,上面是请求头,下面是响应体')
        print(response)

def check(lottery,point,cap_token):
    url = "https://op-api.cloud.jinhua.com.cn/api/captcha/check"
    payload = {
    "activity_id": lottery,
    "module": "bigWheel",
    "cap_token": cap_token,
    "point": point,
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization': "Bearer "+token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        print("验证码校验成功")
    else:
        print(headers)
        print(payload)
        print("验证码校验失败,上面是请求,下面是响应体")
        print(response)
def records():
    url = "https://op-api.cloud.jinhua.com.cn/api/lotterybigwheel/_ac_lottery_records"

    payload = {
    "id": lottery,
    "module": "study"
    }
    times = timestamp()
    nonce = randomcode()
    sign = getApiSign(deviceid, nonce, times, accountid, accesstoken, payload, key)
    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;xsb_zhuji;xsb_zhuji;1.3.2;native_app;6.10.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': "gzip, deflate",
    'access-type': "app",
    'access-module': "study",
    'access-device-id': deviceid,
    'access-auth-id': accountid,
    'access-api-signature': sign,
    'access-nonce-str': nonce,
    'authorization': "Bearer "+token,
    'access-app-id': "uhzfzpj5l78yq6di",
    'access-timestamp': times,
    'access-api-token': accesstoken,
    'content-type': "application/json; charset=UTF-8",
    'origin': "https://op-h5.cloud.jinhua.com.cn",
    'x-requested-with': "com.zjonline.zhuji",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://op-h5.cloud.jinhua.com.cn/",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    if response['code'] == 0:
        print("获取抽奖记录成功")
        records_list = response['data']['list']
        for record in records_list:
            name = record['goodsTitle']
            state = record['state']
            print(name)
            if '元' in name and state != 1 and vxcode:
                record_code = record['code']
                print("去提现")
                get_redenvelope(record_code,vxcode)
    else:
        print(headers)
        print(payload)
        print("获取抽奖记录失败,上面是请求,下面是响应体")
        print(response)
def get_redenvelope(voucherCode,code):
    url = "https://op-api.cloud.jinhua.com.cn/api/study/get_red_envelop"

    payload = {
    "platform": "app",
    "voucherCode": voucherCode,
    "code": code
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; MI 9 Build/PQ3B.190801.06131105; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 MMWEBID/4927 MicroMessenger/8.0.49.2600(0x2800315A) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
    'Accept-Encoding': "gzip,compress,br,deflate",
    'Content-Type': "application/json",
    'charset': "utf-8",
    'Referer': "https://servicewechat.com/wx0babc7be8b49bd15/6/page-frame.html"
    }
    response = requests.post(url, data=payload, headers=headers).json()
    if response['code'] == 0:
        print(response['message'])
    else:
        print(response)
if __name__ == '__main__':
    if not accounts:
        accounts = os.getenv("xsyAccount")
        if not accounts:
            print("❌未找到环境变量！") 
            exit()
    accounts_list = accounts.split("&")
    print(f"一共在环境变量中获取到 {len(accounts_list)} 个账号")
    for account in accounts_list:

        account = account.split("#")
        if len(account) == 3:
            phone ,password, vxcode = account
        elif len(account) == 2:
            phone ,password = account
            vxcode = ""
        else:
            print("看看ck，孩子")
            exit()
        
        t = random.randint(10, 300)
        print(f"账号{phone[:3]+'****'+phone[7:]}开始运行,随机等待{t}秒")
        time.sleep(t)
        deviceid = generate_random_uuid()
        cookie,signature_key = login1()
        code = login2()
        accountid,accesstoken = login3()
        time.sleep(1)
        key,token = login4()
        time.sleep(1)
        lottery = gettask()
        time.sleep(1)
        lotterycount(lottery)
        lotterycount(lottery)
        time.sleep(1)
        records()
