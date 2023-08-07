import streamlit as st

st.set_page_config(page_title="보험 커넥트 - 당신의 소득에 보험을 연결하세요",page_icon=":moneybag:", initial_sidebar_state="collapsed")

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




st.header("보험 커넥트")
st.subheader("당신의 소득에 보험을 연결하세요")

col1, col2 = st.columns([1,2])

with col1:
    st.write("NGIX기본페이지입니다")
