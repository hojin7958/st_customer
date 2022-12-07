import time
import requests
import hashlib
import hmac
import base64
import streamlit as st

def send_sms(phone_number, subject, message):
  def make_signature(access_key, secret_key, method, uri, timestmap):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

  #  URL
  url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:99999999999:sample/messages'
  # access key
  access_key = st.secrets.naver_sms.access_key
  # secret key
  secret_key = st.secrets.naver_sms.secret_key		
  # uri
  uri = '/sms/v2/services/ncp:sms:kr:259200498077:connect/messages'
  timestamp = str(int(time.time() * 1000))

  body = {
    "type":"LMS",
    "contentType":"COMM",
    "countryCode":"82",
    "from":"01030181959",
    "content": message,
    "messages":[
        {
            "to": phone_number,
            "subject": subject,
            "content": message
        }
    ]
  }

  key = make_signature(access_key, secret_key, 'POST', uri, timestamp)
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-ncp-apigw-timestamp': timestamp,
    'x-ncp-iam-access-key': access_key,
    'x-ncp-apigw-signature-v2': key
  }


  res = requests.post(url, json=body, headers=headers)
  print(res.json())
  return res.json()