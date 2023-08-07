### 커넥터용 페이지

import streamlit as st
import database as db
import telegrambot
import time
import streamlit as st

import hashlib
import hmac
import base64
import requests
import json



##문자보내는 영역##########################################################################


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
    secret_key = bytes(str(secret_key), encoding='utf-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, encoding='utf-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey



def send_sms(number, subject, contents):
    header = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp, 
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signature()
    }
    data = {
        "type":"LMS",
        "from":"01030181959",
        "countryCode":"82",
        "content":contents,
        "subject":subject,
        "messages":[
            {
                "to":number,
            }
        ]
    }
    res = requests.post(url+uri,headers=header,data=json.dumps(data))
    datas=json.loads(res.text)
    print(res.text+"\n")
    print(datas)
    # reid=datas['requestId']

    print("메시지 전송 상태")

############################################################################





## 시간체크
from datetime import datetime
from pytz import timezone

now = datetime.now(timezone('Asia/Seoul'))
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
date2 = now.strftime("%Y-%m-%d")



## 세션스테이트 정의    
if 'check_id' not in st.session_state:
    st.session_state['check_id'] = False


## 파라미터 체크영역 
params = st.experimental_get_query_params()
if params:
    temp1 = params['branchcode']
    branchcode = "".join(map(str,temp1))
    display_branchcode = branchcode
else:
    branchcode ="base"
    display_branchcode = ""

st.set_page_config(page_title="보험 커넥트 - 당신의 사업에 보험수익을 연결하세요",page_icon=":moneybag:" , initial_sidebar_state="collapsed")

st.write(str(display_branchcode))


### 여기부터는 햄버거 메뉴 없애는 곳들

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            [data-testid="collapsedControl"] {
                display: none
            }
            footer {visibility: hidden;}
             a:link {
                text-decoration: none;
            }

            a:visited {
                text-decoration: none;
            }

            a:hover {
                text-decoration: none;
            }

            a:active {
                text-decoration: none;
            }

            img {
            width: 100%; /* takes the 100 % width of its container (.box div)*/
            height: 100%; /* takes the 100 % height of its container (.box div)*/
            # border : 1;
            }


            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



st.header("보험커넥트 :moneybag:")
st.subheader("당신의 소득에 보험을 연결하세요")

# 구분선

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# 폼만들기
st.write(
    """
    ### 커넥터(Connector) 회원가입
    보험커넥트에 커넥터로 회원가입해주셔서 감사합니다  
    최종 승인까지 1~2일 정도 소요될 수 있습니다
    """)

with st.form("id_check"):
    st.write(
        """
        ### 개인별 모집 페이지 제작에 필요한 정보입니다  
        ID : 앱 ID로 개별페이지 링크를 제작합니다. ID로 유입된 고객기준으로 정산됩니다  
        본인임을 식별할 수 있는 고유 ID를 입력해주세요  
        한글, 숫자, 영문 등 가능 (개별페이지 상단에 ID표기됩니다)
        """)
    form_id = st.text_input("고유 ID를 입력해주세요")
    submit_id = st.form_submit_button("중복ID확인하기")

    if submit_id:
        if db.check_id(form_id)>=1:
            if 'check_id' not in st.session_state:
                st.session_state['check_id'] = False

            st.error("동일한 ID가 있습니다 ID를 변경해주세요")

            st.session_state['check_id'] = False
        else:
            if 'check_id' not in st.session_state:
                st.session_state['check_id'] = False
            st.session_state['check_id'] = True


### 연락처 입력폼

if st.session_state['check_id']==True:
    with st.form("info"):
        st.write(
            """
            ### 기본정보를 입력해주세요
            연락받으실 전화번호 정보가 부정확한 경우 정산이 지연될 수 있습니다  
            """)


        form_name = st.text_input("이름을 입력해주세요")
        form_phone_num = st.text_input("전화번호를 입력해주세요 입력예시) 01012341234")
        form_work = st.text_input("활동방식을 입력해주세요(예. 영업고객, 주변지인, 동료기사)")


        col_1, col_2 = st.columns([2,1])

        with col_1:
            with st.expander("개인정보 수집 및 이용 동의"):
                st.write("""
                1. 수집/이용목적 : 보험커넥트에서 제공하는 재화/서비스 관련 상담 및 안내   
                2. 보유 및 이용기간 : 동의 철회시점까지
                3. 수집/이용항목 : 재화/서비스 제공을 위한 일반 개인정보                 
                """)
        with col_2:
            form_agree1 = st.checkbox("동의합니다")
        submit = st.form_submit_button("최종제출하기")

    if submit:

        ## 폼 유효성 검증
        if db.check_id(form_id)>=1:
            st.error("이미 입력된 ID입니다, 제출하기는 한번만 눌러주세요")

        else:
            if len(form_id)<1:
                st.error("ID를 입력해주세요")

            elif len(form_name)<1:
                st.error("이름을 입력해주세요")

            elif len(form_phone_num)<1:
                st.error("휴대폰번호를 입력해주세요")
            elif len(form_work)<1:
                st.error("영업방식을 입력해주세요(예. 영업고객, 주변지인, 동료기사)")
            elif len(form_phone_num) != 11:
                st.error("핸드폰번호를 숫자로 11자리 입력해주세요")
            elif form_agree1 == False:
                st.error("개인정보 수집 및 이용에 동의해주세요")

            else:
                with st.spinner('Wait for it...'):
                    time.sleep(2)
                db.insert_user(form_name, form_phone_num,form_work,form_id,date_time)
                msg = "이름 : " + form_name +"\n" + "전화번호 : " + form_phone_num +"\n" + "근무지 : " + form_work +"\n" + "ID : " + form_id +"\n"
                st.success("입력이 완료되었습니다")
                # st.write(msg)
                connect_url = "https://bohumcheck.streamlit.app/?branchcode="+str(form_id)
                msg_header = "[보험커넥트]\n보험커넥트에 커넥트 회원가입이 완료되었습니다\n아래 전용 접속주소를 주위 고객분들에게 안내해주세요\n"
                msg_content = msg_header+date2+"\n"+"커넥터 가입내역\n"+msg +"\n"+"{}님 전용 접속주소 :\n {}".format(form_name,connect_url)
                telegrambot.send_telegram(msg_content)
                send_sms(str(form_phone_num),"보험체크", msg_content)
                # st.write(base_url)
                st.success("{}님 보험커넥터 활동을 위한 링크주소 :\n".format(form_name))
                st.success("{}\n".format(connect_url))
                st.balloons()