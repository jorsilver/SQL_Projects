import os
from datetime import date
import streamlit as st
from PIL import Image, ImageOps
from db_operations import db_operations
import utils

# Initialize Streamlit app
st.set_page_config(page_title="Fitness App", page_icon="💪", layout="wide")

# Initialize database operations
db_ops = db_operations()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'edit_profile' not in st.session_state:
    st.session_state.edit_profile = False


def authenticate_user(username, password):
    return db_ops.first_row("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))


def find_profile_picture(username):
    for ext in [".jpg", ".jpeg"]:
        file_path = f"profile_pics/{username}{ext}"
        if os.path.exists(file_path):
            return file_path
    return "profile_pics/default.jpg"


def login():
    user_data = authenticate_user(st.session_state.username, st.session_state.password)
    if user_data:
        st.session_state.authenticated = True
        st.session_state.user_info = {
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


def show_login_form():
    with st.form("login_form"):
        st.text_input("Username", key='username')
        st.text_input("Password", type="password", key='password')

        st.form_submit_button("Login", on_click=login)


def create_new_account():
    if not st.session_state.new_username or \
        not st.session_state.new_password or \
        not st.session_state.first_name or \
        not st.session_state.last_name or \
        st.session_state.height <= 0 or \
        st.session_state.weight <= 0 or \
        not st.session_state.dob:
            st.error("All fields are required and must be valid.")
            return
    
    if db_ops.first_row_first_attr("SELECT username FROM user WHERE username = %s", (st.session_state.new_username,)):
        st.error("Username already taken. Please choose a different username.")
    else:
        db_ops.modify_query(
            "INSERT INTO user (username, password, first_name, last_name, height, weight, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (st.session_state.new_username, st.session_state.new_password, st.session_state.first_name,
             st.session_state.last_name, st.session_state.height, st.session_state.weight, st.session_state.dob)
        )
        st.success("Account created successfully. Please log in.")
        st.session_state.show_register = False


def show_register_form():
    with st.form("register_form"):
        st.text_input("New Username",max_chars=20, key='new_username')
        st.text_input("New Password", type="password", key='new_password')
        st.text_input("First Name", key='first_name')
        st.text_input("Last Name", key='last_name')
        st.number_input("Height", min_value=0, key='height')
        st.number_input("Weight", min_value=0, key='weight')
        st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today(), key='dob')

        st.form_submit_button("Register", on_click=create_new_account)


def save_profile_picture(image_file, username):
    file_extension = os.path.splitext(image_file.name)[1].lower()
    image_path = f"profile_pics/{username}{file_extension}"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    try:
        with Image.open(image_file) as img:
            img = ImageOps.exif_transpose(img)
            img.save(image_path)
    except Exception as e:
        st.error("Invalid image format. Please upload a valid image.")
        return None
    return image_path


def save_changes():
    st.session_state.user_info.update({
        'first_name': st.session_state.edited_first_name,
        'last_name': st.session_state.edited_last_name,
        'height': st.session_state.edited_height,
        'weight': st.session_state.edited_weight,
        'dob': st.session_state.edited_dob,
        'gender': st.session_state.edited_gender,
        'unit_type': st.session_state.edited_unit_type,
    })
    if st.session_state.edited_profile_pic is not None:
        edited_image_path = save_profile_picture(st.session_state.edited_profile_pic, st.session_state.user_info.username)
        if edited_image_path:
            st.session_state.user_info.profile_image_path = edited_image_path
    
    user_info = st.session_state.user_info

    db_ops.modify_query(
        "UPDATE user SET first_name=%s, last_name=%s, height=%s, weight=%s, dob=%s, gender=%s, unit_type=%s WHERE user_id=%s",
        (user_info.first_name, user_info.last_name, user_info.height, user_info.weight, user_info.dob, user_info.gender, user_info.unit_type, user_info.user_id)
    )
    st.success("Profile updated successfully.")
    st.session_state.edit_profile = False


def delete_account():
    db_ops.modify_query("DELETE FROM user WHERE user_id = %s", (st.session_state.user_info.user_id,))
    st.session_state.clear()
    st.success("Account deleted successfully. Please create a new account or log in with another account.")


def show_edit_profile_form():
    with st.form("edit_profile_form"):
        user_info = st.session_state.user_info
        st.text_input("First Name", value=user_info['first_name'], key='edited_first_name')
        st.text_input("Last Name", value=user_info['last_name'], key='edited_last_name')
        st.number_input("Height", value=float(user_info['height']), key='edited_height')
        st.number_input("Weight", value=float(user_info['weight']), key='edited_weight')
        st.date_input("Date of Birth", value=user_info['dob'], key='edited_dob')
        st.text_input("Gender", value=user_info['gender'], key='edited_gender')
        st.text_input("Unit Type", value=user_info['unit_type'], key='edited_unit_type')
        st.file_uploader("Upload Profile Picture", type=['jpg', 'jpeg'], key='edited_profile_pic')

        st.form_submit_button("Save Changes", on_click=save_changes)
        st.form_submit_button("Delete Account", on_click=delete_account)


def show_user_home_screen():
    user_info = st.session_state.user_info
    st.header(f"Welcome, {user_info['first_name']}!")
    st.subheader("Your Profile")

    if st.session_state.edit_profile:
        show_edit_profile_form()

        st.button("Cancel", on_click=lambda: st.session_state.update({'edit_profile': False}))
    else:
        st.image(user_info['profile_image_path'], width=150, use_column_width=False)
        formatted_height, formatted_weight = utils.format_height_weight(user_info['height'], user_info['weight'], user_info['unit_type'])
        st.write(f"**Height:** {formatted_height}")
        st.write(f"**Weight:** {formatted_weight}")
        st.write(f"**Gender:** {user_info['gender']}")
        st.write(f"**Age:** {utils.calculate_age(user_info['dob'])}")

        st.button("Edit", on_click=lambda: st.session_state.update({'edit_profile': True}))
        st.button("Logout", on_click=lambda: st.session_state.clear())


def run():
    if st.session_state.authenticated:
        show_user_home_screen()
    elif st.session_state.show_register:
        show_register_form()
        st.button("Back to Login", on_click=lambda: st.session_state.update({'show_register': False}))
    else:
        show_login_form()
        st.button("Create New Account", on_click=lambda: st.session_state.update({'show_register': True}))


if __name__ == "__main__":
    run()