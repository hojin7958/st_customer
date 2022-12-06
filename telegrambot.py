import telegram
import streamlit as st


def send_telegram(msg):
    hojin_token = st.secrets.telegram.hojin_token
    bot = telegram.Bot(token = hojin_token)
    try:
        bot.sendMessage(chat_id = 608499969, text=msg)
        return 1

    except:
        pass
        return 0