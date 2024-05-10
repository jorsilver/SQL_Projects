# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from db_operations import db_operations

LOGGER = get_logger(__name__)

st.set_page_config(page_title="Fitness App", page_icon="💪", layout="wide")

db_ops = db_operations()

def authenticate(username, password):
    user = db_ops.select_query("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    if user:
        return user[0]  # Assuming the query returns a list of tuples
    return None

def create_account(username, password, first_name, last_name, height, weight, dob):
    existing_user = db_ops.select_query("SELECT * FROM user WHERE username=%s", (username,))
    if existing_user:
        return False  # Username is not unique
    db_ops.modify_query_params(
        "INSERT INTO user (username, password, first_name, last_name, height, weight, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, password, first_name, last_name, height, weight, dob)
    )
    return True

def user_home_screen(user_info):
    st.header(f"Welcome, {user_info['first_name']}!")
    st.subheader("Your Profile")
    st.write(f"**First Name:** {user_info['first_name']}")
    st.write(f"**Last Name:** {user_info['last_name']}")
    st.write(f"**Height:** {user_info['height']}")
    st.write(f"**Weight:** {user_info['weight']}")
    st.write(f"**Date of Birth:** {user_info['dob']}")

def run():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['show_register'] = False

    if st.session_state['authenticated'] and 'user_info' in st.session_state:
        user_home_screen(st.session_state['user_info'])
    else:
        if not st.session_state.get('show_register', False):
            with st.form("login_form"):
                st.header("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login = st.form_submit_button("Login")
                
                if login:
                    user_data = authenticate(username, password)
                    if user_data:
                        st.session_state['authenticated'] = True
                        st.session_state['user_info'] = {
                            'user_id': user_data[0],
                            'username': user_data[1],  # Adjust indices based on your DB schema
                            'first_name': user_data[4],
                            'last_name': user_data[5],
                            'height': user_data[6],
                            'weight': user_data[7],
                            'dob': user_data[9]
                        }
                        st.success("Logged in successfully.")
                    else:
                        st.error("Incorrect username or password")
            
            if st.button("Create New Account"):
                st.session_state['show_register'] = True
        else:
            st.header("Create a New Account")
            new_username = st.text_input("New Username", key="new_username")
            new_password = st.text_input("New Password", type="password", key="new_password")
            first_name = st.text_input("First Name", key="new_first_name")
            last_name = st.text_input("Last Name", key="new_last_name")
            height = st.number_input("Height", min_value=0, key="new_height")
            weight = st.number_input("Weight", min_value=0, key="new_weight")
            dob = st.date_input("Date of Birth", key="new_dob")
            if st.button("Register"):
                if create_account(new_username, new_password, first_name, last_name, height, weight, dob):
                    st.success("Account created successfully. Please log in.")
                    st.session_state['show_register'] = False
            if st.button("Back to Login"):
                st.session_state['show_register'] = False

if __name__ == "__main__":
    run()