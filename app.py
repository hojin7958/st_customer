import streamlit as st

st.set_page_config(page_title="보험 커넥트 - 당신의 소득에 보험을 연결하세요",page_icon=":moneybag:")


st.header("보험 커넥트")
st.subheader("당신의 소득에 보험을 연결하세요")

col1, col2 = st.columns([1,2])

with col1:
    st.write("야! 너두?")





hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
