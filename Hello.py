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

import os
import streamlit as st
from streamlit.logger import get_logger
from PIL import Image, ImageOps
from db_operations import db_operations
import utils

LOGGER = get_logger(__name__)

st.set_page_config(page_title="Fitness App", page_icon="💪", layout="wide")

db_ops = db_operations()

def authenticate_user(username, password):
    return db_ops.first_row("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))

def find_profile_picture(username):
    for ext in [".jpg", ".jpeg"]:
        file_path = f"profile_pics/{username}{ext}"
        if os.path.exists(file_path):
            return file_path
    return "profile_pics/default.jpg"

def show_login_form():
    with st.form("login_form"):
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user_data = authenticate_user(username, password)
            if user_data:
                st.session_state['authenticated'] = True
                st.session_state['user_info'] = {
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'current_program': user_data[3],
                    'first_name': user_data[4],
                    'last_name': user_data[5],
                    'height': user_data[6],
                    'weight': user_data[7],
                    'dob': user_data[9],
                    'gender': user_data[10],
                    'unit_type': user_data[11],
                    'profile_image_path': find_profile_picture(user_data[1])
                }
                st.success("Logged in successfully.")
            else:
                st.error("Incorrect username or password")

def create_new_account(username, password, first_name, last_name, height, weight, dob):
    if db_ops.first_row_first_attr("SELECT username FROM user WHERE username = %s", (username,)):
        st.error("Username already taken. Please choose a different username.")
        return False
    db_ops.modify_query(
        "INSERT INTO user (username, password, first_name, last_name, height, weight, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, password, first_name, last_name, height, weight, dob)
    )
    return True

def show_register_form():
    with st.form("register_form"):
        st.header("Create a New Account")
        new_username = st.text_input("New Username", key="new_username")
        new_password = st.text_input("New Password", type="password", key="new_password")
        first_name = st.text_input("First Name", key="new_first_name")
        last_name = st.text_input("Last Name", key="new_last_name")
        height = st.number_input("Height", min_value=0, key="new_height")
        weight = st.number_input("Weight", min_value=0, key="new_weight")
        dob = st.date_input("Date of Birth", key="new_dob")
        register_button = st.form_submit_button("Register")
    if register_button:
        if create_new_account(new_username, new_password, first_name, last_name, height, weight, dob):
            st.success("Account created successfully. Please log in.")
            st.session_state['show_register'] = False

def save_profile_picture(image_file, username):
    file_extension = os.path.splitext(image_file.name)[1].lower()
    image_path = f"profile_pics/{username}{file_extension}"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    try:
        with Image.open(image_file) as img:
            img = ImageOps.exif_transpose(img)
            img.save(image_path)
    except Exception as e:
        LOGGER.error(f"Error: {e}")
        st.error("Invalid image format. Please upload a valid image.")
        return None
    return image_path

def show_edit_profile_form(user_info):
    with st.form("edit_profile_form"):
        first_name = st.text_input("First Name", value=user_info['first_name'])
        last_name = st.text_input("Last Name", value=user_info['last_name'])
        height = st.number_input("Height", value=float(user_info['height']))
        weight = st.number_input("Weight", value=float(user_info['weight']))
        dob = st.date_input("Date of Birth", value=user_info['dob'])
        gender = st.text_input("Gender", value=user_info['gender'])
        unit_type = st.text_input("Unit Type", value=user_info['unit_type'])
        profile_pic = st.file_uploader("Upload Profile Picture", type=['jpg', 'jpeg'])

        save_button = st.form_submit_button("Save Changes")
        cancel_button = st.form_submit_button("Cancel")

    if save_button:
        st.session_state['user_info'].update({
            'first_name': first_name,
            'last_name': last_name,
            'height': height,
            'weight': weight,
            'dob': dob,
            'gender': gender,
            'unit_type': unit_type,
        })
        if profile_pic is not None:
            image_path = save_profile_picture(profile_pic, user_info['username'])
            if image_path:
                st.session_state['user_info']['profile_image_path'] = image_path

        db_ops.modify_query(
            "UPDATE user SET first_name=%s, last_name=%s, height=%s, weight=%s, dob=%s, gender=%s, unit_type=%s WHERE user_id=%s",
            (first_name, last_name, height, weight, dob, gender, unit_type, user_info['user_id'])
        )
        st.success("Profile updated successfully.")
        st.session_state['edit_profile'] = False

    if cancel_button:
        st.session_state['edit_profile'] = False

def show_user_home_screen():
    user_info = st.session_state['user_info']
    st.header(f"Welcome, {user_info['first_name']}!")
    st.subheader("Your Profile")

    if 'edit_profile' not in st.session_state:
        st.session_state['edit_profile'] = False

    if st.session_state['edit_profile']:
        show_edit_profile_form(user_info)
    else:
        st.image(user_info['profile_image_path'], width=150)
        formatted_height, formatted_weight = utils.format_height_weight(user_info['height'], user_info['weight'], user_info['unit_type'])
        st.write(f"**Height:** {formatted_height}")
        st.write(f"**Weight:** {formatted_weight}")
        st.write(f"**Gender:** {user_info['gender']}")
        st.write(f"**Age:** {utils.calculate_age(user_info['dob'])}")

        if st.button("Edit"):
            st.session_state['edit_profile'] = True

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['show_register'] = False

    if st.session_state['authenticated']:
        show_user_home_screen()
    elif st.session_state['show_register']:
        show_register_form()
        if st.button("Back to Login"):
            st.session_state['show_register'] = False
    else:
        show_login_form()
        if st.button("Create New Account"):
            st.session_state['show_register'] = True

if __name__ == "__main__":
    main()
