import streamlit as st

with st.container():
    name2 = st.text_input("외부입력")
    st.write(name2)


with st.form("info"):
    name = st.text_input("이름을 입력해주세요")
    st.write(name)
    st.form_submit_button("입력완료")

msg1 = name+"이 맞습니까?"

st.write(msg1)

with st.form("info2"):
    name = st.text_input("이름을 입력해주세요")
    
    st.form_submit_button("입력완료")
