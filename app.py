### 고객용 페이지

import streamlit as st
import database_customer as db
import send_sms
import telegrambot



## 시간체크
from datetime import datetime
from pytz import timezone

now = datetime.now(timezone('Asia/Seoul'))
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
    

st.set_page_config(page_title="보험체크 - 당신의 보험은 건강한가요? ",page_icon=":thermometer:", initial_sidebar_state="collapsed")
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



st.header("보험체크 :thermometer:")
st.subheader("당신의 보험은 건강한가요? 보험 건강을 체크해드립니다")


# 구분선

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.subheader("보험체크에서는 쉽고 간편하게 진행해요!")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### :pencil2:상담신청")
    st.markdown("""
    :white_small_square: 연락받으실 이름과 연락처를 남겨주세요  
    :white_small_square: 업무하시는데 부담이 없도록 카카오톡이나 문자로 상담가능한 시간을 여쭤볼께요
    """)

with col2:
    st.markdown("### :white_check_mark:보험체크")
    st.markdown("""
    :white_small_square: 중복해서 보험을 가입할 수 없기때문에 현재 가입한 보험을 체크합니다  
    :white_small_square: 가입상담에 필요한 주민번호를 확인합니다
    """)

with col3:
    st.markdown("### :grin:상담")
    st.markdown("""
    :white_small_square: 배정된 보험설계사가 고객님과 연락을 해서 다시한번 상담을 진행합니다  
    :white_small_square: 꼼꼼히 설명을 듣고, 가입을 결정해주세요(비대면상담가능)
    """)


st.write("---")

with st.form("info"):
    st.write(
        """
        ### 보험체크 상담신청하기
        """)

    form_name = st.text_input("이름을 입력해주세요")
    form_phone_num = st.text_input("전화번호를 입력해주세요 입력예시) 01012341234")
    form_howto = st.selectbox(
    '편하신 상담방법을 선택해주세요',
    ('카카오톡', '전화통화'))

    col_1, col_2 = st.columns([2,1])

    with col_1:
        with st.expander("개인정보 수집 및 이용 동의"):
            st.write("""
            1. 수집/이용목적 : 보험체크에서 제공하는 재화/서비스 관련 상담 및 안내   
            2. 보유 및 이용기간 : 동의 철회시점까지
            3. 수집/이용항목 : 재화/서비스 제공을 위한 일반 개인정보                 
            """)
    with col_2:
        form_agree1 = st.checkbox("동의합니다")

    submit = st.form_submit_button("입력완료")


if submit > 0:

    ## 폼 유효성 검증

    if len(form_name)<1:
        st.error("이름을 입력해주세요")

    elif form_agree1 == False:
        st.error("개인정보 수집 및 이용에 동의해주세요")

    elif len(form_phone_num)<1:
        st.error("휴대폰번호를 입력해주세요")
    else:
        pass

    if len(form_phone_num) != 11:
        st.error("핸드폰번호를 숫자 11자리로 입력해주세요")
    else:
        db.insert_user(form_name, form_phone_num,form_howto, branchcode, date_time)
        msg ="이름 : " + form_name +"\n" + "전화번호 : " + form_phone_num +"\n" + "연락방법 : " + form_howto +"\n" +"추천코드 : "+branchcode 
        st.success("입력이 완료되었습니다. 상담신청을 남겨주셔서 감사합니다")
        # st.write(msg)
        telegrambot.send_telegram(date_time+"\n"+"보험체크 고객 접수내역\n"+msg)


print(branchcode)
# send_sms.send_sms('01030657958','장문테스트')