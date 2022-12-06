import streamlit as st
from deta import Deta  # pip install deta




DETA_KEY = st.secrets.deta.DETA_KEY
# Initialize with a project key
deta = Deta(DETA_KEY)
# This is how to create/connect a database
db = deta.Base("customer_db")


def insert_user(user_name, user_phone_num, user_howto,branchcode, timestamp):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"user_name": user_name, "user_phone_num": user_phone_num, "user_howto": user_howto, "branchcode":branchcode,"timestamp":timestamp})

def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items

def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)

def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)


def check_id(user_id):
    return db.fetch({'key':user_id}).count


def check_nick(user_nick):
    return db.fetch({'user_nick':user_nick}).count