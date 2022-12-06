### 커넥터용 페이지

import streamlit as st
import database as db
import send_sms
import telegrambot

## 시간체크
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")


## 파라미터 체크영역 
params = st.experimental_get_query_params()
if params:
    temp1 = params['branchcode']
    branchcode = "".join(map(str,temp1))
    display_branchcode = branchcode
else:
    branchcode ="base"
    display_branchcode = ""

st.set_page_config(page_title="보험 커넥트 - 당신의 사업에 보험수익을 연결하세요",page_icon=":moneybag:")

st.write(str(display_branchcode))


# 광고 하단 / 우측상단 햄버거 문구 없애는 코드 

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
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
with st.form("info"):
    st.write(
        """
        ### 기본정보를 입력해주세요
        """)


    form_name = st.text_input("이름을 입력해주세요")
    form_phone_num = st.text_input("전화번호를 입력해주세요 입력예시) 01012341234")
    form_work = st.text_input("활동방식을 입력해주세요(예. 영업고객, 주변지인, 동료기사)")

    st.write("---")
    st.write(
        """
        ### 개인별 모집 페이지 제작에 필요한 정보입니다
        ID : 앱 ID로 유입된 고객기준으로 정산됩니다  
        커넥터 닉네임 : 앱에 표시되는 이름입니다  
        한번 입력된 ID / 닉네임은 변경이 불가능합니다
        """)
    form_id = st.text_input("ID를 입력해주세요")
    form_nick = st.text_input("닉네임을 입력해주세요")

    print(len(form_phone_num))
    submit = st.form_submit_button("입력완료")


if submit > 0:

    ## 폼 유효성 검증

    if len(form_id)<1:
        st.error("ID를 입력해주세요")

    elif len(form_name)<1:
        st.error("이름을 입력해주세요")

    elif len(form_nick)<1:
        st.error("닉네임을 입력해주세요")

    elif len(form_phone_num)<1:
        st.error("휴대폰번호를 입력해주세요")

    elif len(form_work)<1:
        st.error("영업방식을 입력해주세요(예. 영업고객, 주변지인, 동료기사)")
    else:
        pass



    if len(form_phone_num) != 11:
        st.error("핸드폰번호를 숫자로 11자리 입력해주세요")
    elif db.check_id(form_id)>=1:
        st.error("동일한 ID가 있습니다 ID를 변경해주세요")
    elif db.check_nick(form_nick)>=1:
        st.error("동일한 닉네임이 있습니다 닉네임을 변경해주세요")
    else:
        db.insert_user(form_name, form_phone_num,form_work,form_id,form_nick, date_time)
        msg = "이름 : " + form_name +"\n" + "전화번호 : " + form_phone_num +"\n" + "근무지 : " + form_work +"\n" + "ID : " + form_id +"\n" + "닉네임 : " + form_nick
        st.success("입력이 완료되었습니다")
        # st.write(msg)
        connect_url = "https://bohumcheck.streamlit.app/?branchcode="+str(form_id)
        msg_content = "[보험커넥트]\n"+date_time+"\n"+"커넥터 접수내역\n"+msg +"\n"+"{}님 전용 접속주소 :\n {}".format(form_name,connect_url)
        telegrambot.send_telegram(msg_content)
        send_sms.send_sms(str(form_phone_num),msg_content)
        # st.write(base_url)

