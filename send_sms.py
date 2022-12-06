import streamlit as st
import hashlib
import hmac
import base64
import requests
import time
import json


timestamp=int(time.time() * 1000)
timestamp=str(timestamp)

access_key = st.secrets.naver_sms.access_key			# access key id (from portal or Sub Account)
secret_key = st.secrets.naver_sms.secret_key					# secret key (from portal or Sub Account)

url="https://sens.apigw.ntruss.com"
uri="/sms/v2/services/ncp:sms:kr:259200498077:connect/messages"


def	make_signature():
    global secret_key
    global access_key
    global timestamp
    global url
    global uri
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, encoding='utf-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey



def send_sms(number, contents):
    header = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp, 
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signature()
    }
    data = {
        "type":"LMS",
        "from":"01030181959",
        "content":contents,
        "subject":"SENS",
        "messages":[
            {
                "to":number,
            }
        ]
    }
    res = requests.post(url+uri,headers=header,data=json.dumps(data))
    datas=json.loads(res.text)
    reid=datas['requestId']

    print("메시지 전송 상태")
    print(res.text+"\n")
