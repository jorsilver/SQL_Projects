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

st.set_page_config(page_title="Fitness App", page_icon="👋", layout="wide")

db_ops = db_operations()

def authenticate(username, password):
    # Assume a SQL query function returning user info or None
    user = db_ops.select_query_params("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    return bool(user)

def run():
    st.write(db_ops.select_query("SELECT first_name from user;"))

    # Create session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # User interface for login
    if not st.session_state['authenticated']:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            # Authentication logic
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.success("Logged in successfully.")
            else:
                st.error("Incorrect username or password")

    if st.session_state['authenticated']:
        st.write("Welcome to the Fitness App!")



if __name__ == "__main__":
    run()
