import os
from datetime import date
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import utils
from db_operations import db_operations
from user_info import User_Info_Series


st.set_page_config(page_title="Fitness App", page_icon="💪", layout="wide")


if 'runs' not in st.session_state:
    st.session_state.runs = 1
    st.session_state.authenticated = False
    st.session_state.creating_account = False
    db_ops = st.session_state.db_ops = db_operations()
    print("-" * 69)
    utils.print_session_state("******FIRST ENTRY******")
else:
    st.session_state.runs = st.session_state.runs + 1
    db_ops: db_operations = st.session_state.db_ops
    print("-" * st.session_state['max_len'])
    print(f"******START OF RUN({st.session_state['runs']})******".center(st.session_state['max_len']))


def delete_account():
    """
    Delete the current user's account and clear the session state.

    If the user has a custom profile picture, it will be removed from the file system.
    """
    user_info = st.session_state.user_info
    if user_info['profile_pic_path'] != "profile_pics/default.jpg": os.remove(user_info['profile_pic_path'])
    db_ops.modify_query("DELETE FROM user WHERE user_id = :user_id", {'user_id': int(user_info.user_id)})
    st.session_state.clear()
    st.success("Account deleted successfully. Please create a new account or log in with another account.")


def get_user_info(username, password):
    """
    Retrieve user information from the database.

    Args:\n
            - username (str): The username of the user.
            - password (str): The password of the user.

    Returns:\n
            - (`User_Info_Series`): A series containing user information
            - (None): if 'username' or 'password' are incorrect
    """
    user_info: pd.Series = db_ops.first_row("CALL get_user_info(:username, :password)", {"username": username, "password": password})
    return User_Info_Series(user_info) if user_info is not None else None


def username_taken(username):
    """
    Check if the given username is already taken.

    Args:\n
            - 'username' (str): The username to check.

    Returns:\n
            - True: if 'username' is taken
    """
    if db_ops.first_row_first_attr("SELECT 1 FROM user WHERE username = :username", {'username': username}):
        st.error("Username already taken. Please choose a different username.")
        return True
    return False


def login():
    """
    Attempt to log in the user with the provided credentials.

    Returns:\n
            - (DeltaGenerator): if login fails.
            - (None): `user_info` stored in `st.session_state`

    """
    user_info = get_user_info(st.session_state.username, st.session_state.password)
    if user_info is None: return st.error("Incorrect username or password")
    st.session_state.authenticated = True
    st.session_state.user_info = user_info
    st.success("Logged in successfully.")


def show_login_form():
    """
    Renders the login form and handles the login process

    See Also:
        `login()`: (on_click) Handle credential verification and storing
    """
    with st.form("login_form"):
        st.text_input("Username", key='username')
        st.text_input("Password", type="password", key='password')

        st.form_submit_button("Login", on_click=login)


def create_new_user():
    """
    Handle the creation of a new user account\n
            - checks the input fields for validity
            - verifies if the username is taken
            - saves the profile picture in the `profile_pics` directory
            - inserts new user information into the database 

    See Also:
        - `utils.check_profile_input_fields()`: Validates the user input fields.
        - `username_taken()`: Checks if the username is already taken.
        - `utils.save_profile_picture()`: Saves the profile picture and returns the path.
        - `db_ops.modify_query()`: Executes modify queries, with optional parameters.
    """
    user_info = utils.check_profile_input_fields() # Check user input

    if isinstance(user_info, DeltaGenerator): return # Input check failed
    
    if username_taken(user_info['username']): return # Username taken

    saved_path = utils.save_profile_picture(st.session_state.pop('opt_profile_pic'), user_info['username'])
    
    if saved_path is None: 
        return st.error("Invalid image format. Please upload a valid file.")# Invalid file format
    user_info['profile_pic_path'] = saved_path

    
    attributes = ", ".join([key for key in user_info.keys()])
    values = ", ".join([f":{key}" for key in user_info.keys()])
    db_ops.modify_query(f"INSERT INTO user\n({attributes})\nVALUES\n({values})", user_info)
    

    st.session_state.creating_account = False
    st.success("Account created successfully. Please log in.")


def show_new_user_form():
    """
    Renders the 'new_user' form and handles creating accounts

    See Also:
        `create_new_user()`: (on_click) Handle the creation of a new user account
    """
    with st.form("new_user_form"):
        st.text_input("Username", value=None, max_chars=35, key='username')
        st.text_input("Password", value=None, max_chars=18, type="password", key='password')
        st.text_input("Verify Password", value=None, max_chars=18, type="password", key='password_check')
        st.text_input("First Name", value=None, max_chars=35, key='first_name')
        st.text_input("Last Name", value=None, max_chars=35, key='last_name')
        st.number_input("Height", value=None, placeholder="Inches / Centimeters", key='height')
        st.number_input("Weight", value=None, placeholder="Lbs or Kg", key='weight')
        st.number_input("Body Fat %", max_value=100.00, value=None, placeholder="Enter manually here (Can be left blank)", key='opt_body_fat_percentage')
        st.text_input("Gender", max_chars=35, value="N/A", key="gender")
        st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today(), key='dob')
        st.radio("Unit type", options=["metric", "imperial"], index=None, key='unit_type')
        "---"
        "**Body Fat % Calculation Metrics**"
        st.number_input("Waist Size", value=None, placeholder="Inches or Centimeters (Can be left blank)",       
                        help="Measure your waist circumference for body fat %% calculation", key='opt_waist_size')
        st.number_input("Neck Size", value=None, placeholder="Inches or Centimeters (Can be left blank)",
                        help="Measure your neck circumference for body fat %% calculation", key='opt_neck_size')
        st.number_input("Hip Size (Women Only)", value=None, placeholder="Inches or Centimeters (Can be left blank)",
                        help="Measure your hip circumference for body fat %% calculation", key='opt_hip_size')
        "---"
        st.file_uploader("Upload Profile Picture (Can Be Done Later)", type=['jpg', 'jpeg'], key='opt_profile_pic')

        st.form_submit_button("Register", on_click=create_new_user)


def save_profile_changes():
    """
    Handle updating account details\n
        - Validates the input fields
        - Identifies changed attributes and stroes them in a dict
        - Saves or updates the profile picture and it's path
        - inserts new user information into the database
        - Updates user information in the database
        - Updates `session_state.user_info` to reflect the changes

    See Also:
        - `utils.check_profile_input_fields()`: Validates the user input fields.
        - `username_taken()`: Checks if the username is already taken.
        - `utils.save_profile_picture()`: Saves the profile picture and returns the path.
        - `db_ops.modify_query()`: Executes modify queries, with optional parameters.
    """
    utils.print_session_state(f"******EDIT PROFILE FORM SUBMITTED (BEFORE USER INPUT CHECK)******")
    user_info = utils.check_profile_input_fields() # check user input

    if isinstance(user_info, DeltaGenerator): return # input check failed

    #Subset, only containing key-value pairs where the value has been changed
    changed_attributes = {key: value for key, value in user_info.items() if value != st.session_state.user_info.get(key)}
    
    if 'username' not in changed_attributes:# Username not changed:
        saved_path = utils.save_profile_picture(st.session_state.pop('opt_profile_pic'), user_info['username'])
        if saved_path is None:
            return st.error("Invalid image format. Please upload a valid file.")# Invalid file format
        
        if saved_path != st.session_state.user_info.profile_pic_path: changed_attributes['profile_pic_path'] = saved_path
    
    elif username_taken(changed_attributes['username']): return # Username taken
    
    elif st.session_state['opt_profile_pic'] is None: # Username changed but no file uploaded
        old_path = st.session_state.user_info['profile_pic_path']
        if old_path != "profile_pics/default.jpg":
            changed_attributes['profile_pic_path'] = f"profile_pics/{changed_attributes['username']}{os.path.splitext(old_path)[1].lower()}"
            os.rename(old_path, changed_attributes['profile_pic_path'])
        
    else: # Username changed & file uploaded
        old_path = st.session_state.user_info['profile_pic_path']
        if old_path != "profile_pics/default.jpg":
            os.remove(old_path)

        saved_path = utils.save_profile_picture(st.session_state.pop('opt_profile_pic'), changed_attributes['username'])
        if saved_path is None:
            return st.error("Invalid image format. Please upload a valid file.")# Invalid file format
        changed_attributes['profile_pic_path'] = saved_path

    print(f"\n\n      CHANGED_ATTRIBUTES\n\n{pd.Series(changed_attributes)}\n\n".center(st.session_state['max_len']))
    if changed_attributes:
        attributes = ", ".join([f"{key} = :{key}" for key in changed_attributes.keys()])
        db_ops.modify_query(f"UPDATE user SET\n{attributes}\nWHERE user_id = :user_id" ,
                {**changed_attributes, 'user_id': int(st.session_state.user_info['user_id'])})
        st.session_state.user_info.update(changed_attributes)

    # Update st.session_state.user_info to reflect the changes
    st.session_state.editing_profile = False
    st.success("Profile updated successfully.")

    utils.print_session_state(f"******EDIT PROFILE FORM SUBMITTED (AFTER USER INPUT CHECK)******")


def show_edit_profile_form():
    """
    Renders the 'edit_profile' form and handles updating or deleting accounts

    See Also:
        - (on_click) 'Save Changes': `save_changes()`
        - (on_click) 'Delete Account': `delete_account()`
    """
    with st.form("edit_profile_form"):
        user_info: User_Info_Series = st.session_state.user_info
        st.text_input("Username",value=user_info.username, max_chars=35, key='username')
        st.text_input("Password",value=user_info.password, max_chars=18, type="password", key='password')
        st.text_input("Verify Password", value=None, max_chars=18, type="password", key='password_check')
        st.text_input("First Name", value=user_info.first_name, max_chars=35, key='first_name')
        st.text_input("Last Name", value=user_info.last_name, max_chars=35, key='last_name')
        st.number_input("Height", value=user_info.height, key='height')
        st.number_input("Weight", value=user_info.weight, key='weight')
        st.number_input("Body Fat %", max_value=100.00, value=user_info.body_fat_percentage, placeholder="Enter manually here (Can be left blank)", key='opt_body_fat_percentage')
        st.text_input("Gender", max_chars=35, value=user_info.gender, key='gender')
        st.date_input("Date of Birth", value=user_info.dob, min_value=date(1900, 1, 1), max_value=date.today(), key='dob')
        st.radio("Unit type", options=["metric", "imperial"], index=(0 if user_info.unit_type == "metric" else 1), key='unit_type')     
        "---"
        "**Body Fat % Calculation Metrics**"
        st.number_input("Waist Size", value=None, placeholder="Inches or Centimeters (Can be left blank)",
                        help="Measure your waist circumference for body fat %% calculation", key='opt_waist_size')
        st.number_input("Neck Size", value=None, placeholder="Inches or Centimeters (Can be left blank)",
                        help="Measure your neck circumference for body fat %% calculation", key='opt_neck_size')
        st.number_input("Hip Size (Only Used For Women's BF % Calculation)", value=None, placeholder="Inches or Centimeters (Can be left blank)",
                        help="Measure your hip circumference for body fat %% calculation", key='opt_hip_size')
        "---"
        st.file_uploader("Upload New Profile Picture", type=['jpg', 'jpeg'], key='opt_profile_pic')

        st.form_submit_button("Save Changes", on_click=save_profile_changes)
        st.form_submit_button("Delete Account", on_click=delete_account)

    print(f"******EDIT PROFILE FORM OPENED******".center(st.session_state['max_len']) + "\n")


def show_profile():
    """
    Display the user's profile information.

    Displays:\n
        - Profile Picture
        - Username
        - Name
        - Gender
        - Age
        - Height
        - Weight
        - Body Fat %
    """
    user_info: User_Info_Series = st.session_state.user_info
    concat_name = user_info.first_name + " " + user_info.last_name
    formatted_height, formatted_weight = utils.format_height_weight(user_info.height, user_info.weight, user_info.unit_type)
    img_base64 = utils.get_image_base64(user_info.profile_pic_path)
    age = utils.calculate_age(user_info.dob)

    st.markdown(f"""
        <div style="text-align: center;">
            <h1>YOUR PROFILE</h1>
            {f'<img src="data:image/jpeg;base64,{img_base64}" width="200" style="display: block; margin: 0 auto;">'
            if img_base64 else
            "<p style='color: red;'>Profile picture could not be loaded.</p>"}
        </div>
        """, unsafe_allow_html=True)

    "---"
    col1, col2 = st.columns(2)
    with col1:
        "**Username:** ", user_info.username
        "**Name:** ", concat_name
        "**Gender:** ", user_info.gender
        "**Age:** ", str(age)
    with col2:
        "**Height:** ", formatted_height
        "**Weight:** ", formatted_weight
        "**Body Fat:** ", str(user_info.body_fat_percentage) + "%"
    "---"


def show_user_home_screen():
    """
    Renders the user's profile or the edit profile form based on the session state.

    Provides buttons to toggle between viewing and editing the profile.

    See Also:
        - `show_profile()`: Displays the user's profile information.
        - `show_edit_profile_form()`: Displays the form for editing the user's profile information.
    """
    if 'editing_profile' not in st.session_state:
        st.session_state.editing_profile = False

    if st.session_state.editing_profile:
        show_edit_profile_form()
        st.button("Cancel", on_click=lambda: st.session_state.update({'editing_profile': False}))
    else:
        show_profile()
        st.button("Edit", on_click=lambda: st.session_state.update({'editing_profile': True}))


def run():
    if st.session_state.authenticated:
        show_user_home_screen()
        st.sidebar.button("Logout", on_click=lambda: st.session_state.clear(), disabled=st.session_state.editing_profile)

    elif st.session_state.creating_account:
        show_new_user_form()
        st.button("Back to Login", on_click=lambda: st.session_state.update({'creating_account': False}))
    
    else:
        show_login_form()
        st.button("Create New Account", on_click=lambda: st.session_state.update({'creating_account': True}))

if __name__ == "__main__":
    run()