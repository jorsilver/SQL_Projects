import os
import math
import base64
import pandas as pd
import streamlit as st
from datetime import date
from PIL import Image, ImageOps
from user_info import User_Info_Series

def to_cm(value):
    return value * 2.54


def print_session_state(header):
    """
    Print the current state of the Streamlit session.
    
    Args:\n
            - 'header' (str): A message to print before displaying the session state.
    """
    main_series = {k: v for k, v in sorted(st.session_state.items()) if k != 'user_info'}
    user_info_series = {f'user_info.{k}': v for k, v in sorted(st.session_state.get('user_info', {}).items())}
    combined_series = pd.Series({**main_series, **user_info_series}).to_string().replace('\n', '\n\n')
    
    if user_info_series:
        user_info_section = combined_series.find('user_info.')
        combined_series = f"{combined_series[:user_info_section]}\n\n{combined_series[user_info_section:]}\n"
        
    st.session_state['max_len'] = max_len = max(len(line) for line in combined_series.split('\n\n'))
    
    print(f"{header.center(max_len)}\n\n{'SESSION_STATE'.center(max_len)}\n\n{combined_series}")


def calculate_age(dob: date):
    """
    Calculate age from date of birth.
    
    Args:
    dob (str): Date of birth in '%Y-%m-%d' format.
    
    Returns:
    int: Age in years.
    """
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def format_height_weight(height, weight, unit_type):
    """
    Formats the height and weight based on the unit type provided.

    Args:
    height (float): The height value to format.
    weight (float): The weight value to format.
    unit_type (str): Either 'imperial' or 'metric' to specify the unit type.

    Returns:
    str, str: Formatted height and weight strings.
    """
    if unit_type == 'imperial':
        # Convert height to feet and inches
        feet = int(height// 12)
        inches = int(height % 12)
        formatted_height = f"{feet}' {inches}\""
        formatted_weight = f"{weight} lbs"
    else:  # unit_type == 'metric'
        formatted_height = f"{height} cm"
        formatted_weight = f"{weight} kg"
    
    return formatted_height, formatted_weight


def calc_body_fat_percentage(user_info):
    """
    Calculate the body fat percentage based on the user's information.

        Args:\n
            - 'user_info' (dict): A dictionary containing user information.\n
        Expected keys:\n
            - 'gender' (str): Gender of the user ('male' or 'female')\n
            - 'weight' (float): Weight of the user in kilograms\n
            - 'height' (float): Height of the user in centimeters\n
            - 'age' (int): Age of the user in years\n


    Returns:
        float: The calculated body fat percentage.
    """
    bfp = st.session_state.pop('opt_body_fat_percentage')
    height = user_info['height']
    neck_size = st.session_state.pop('opt_neck_size')
    waist_size = st.session_state.pop('opt_waist_size')
    hip_size = st.session_state.pop('opt_hip_size')

    if neck_size is None or waist_size is None: return bfp

    if user_info['unit_type'] == 'imperial':
        height = to_cm(height)
        neck_size = to_cm(neck_size)
        waist_size = to_cm(waist_size)
        if hip_size is not None: hip_size = to_cm(hip_size)

    print("*****CALCULATING BFP*****".center(st.session_state['max_len']))
    print(pd.Series({'Height': height, 'Neck Size': neck_size, 'Waist Size': waist_size}), "\n")
    
    if user_info['gender'] == 'Male':
        bfp = (495 / (1.0324 - 0.19077 * math.log10(waist_size - neck_size) + 0.15456 * math.log10(height))) - 450
        print(f"BFP = {bfp}\n".center(st.session_state['max_len']))
    elif user_info['gender'] == 'Female' and hip_size is not None:
        bfp = (495 / (1.29579 - 0.35004 * math.log10(waist_size + hip_size - neck_size) + 0.22100 * math.log10(height))) - 450
    else:
        bfp_male = (495 / (1.0324 - 0.19077 * math.log10(waist_size - neck_size) + 0.15456 * math.log10(height))) - 450
        bfp_female = (495 / (1.29579 - 0.35004 * math.log10(2 * waist_size + 12 - neck_size) + 0.22100 * math.log10(height))) - 450
        bfp = (bfp_male + bfp_female + (bfp if bfp is not None else 0)) / (2 if bfp is None else 3)
    
    return bfp


def get_path(username):
    """
    Find the path to an existing profile picture

    Args:\n
            - 'username' (str): The username of the user.

    Returns:\n
            - (str): The existing path or "profile_pics/default.jpg"
    """
    extensions = [".jpg", ".jpeg"]
    for ext in extensions:
        if os.path.exists(f"profile_pics/{username}{ext}"):return f"profile_pics/{username}{ext}"
    return "profile_pics/default.jpg"


def save_profile_picture(picture_file, username):
    """
    Save an uploaded profile picture to the 'profile_pics' directory

    If a file is uploaded:\n
            - File path is set to username, + the extesnion of the file uploaded

    If no file is uploaded:\n
            - File path set to existing path or default path.

    Args:\n
            - 'picture_file' (UploadedFile): The uploaded profile picture file.\n
            - 'username' (str): The username of the user.

    Returns:\n
            - str: The file path to the saved profile picture, or None if there was an error.
    """
    if picture_file is None: return get_path(username) # No file uploaded

    # file path is set to username, + the extesnion of the file uploaded
    profile_pic_path = f"profile_pics/{username}{os.path.splitext(picture_file.name)[1].lower()}"
    
    try:
        os.makedirs(os.path.dirname(profile_pic_path), exist_ok=True) # will overwrite if path exists
        with Image.open(picture_file) as img:
            img = ImageOps.exif_transpose(img)
            img.save(profile_pic_path)
        return profile_pic_path
    except Exception as e: # Bad format
        return None
    

def get_image_base64(file_path):
    """
    Convert an image file to a base64-encoded string.

    Args:\n
            - 'file_path' (str): The path to the image file.

    Returns:\n
            - (str): The base64-encoded string of the image, or None if there was an error.
    """
    try:
        return base64.b64encode(open(file_path, "rb").read()).decode()
    except Exception as e:
        st.error(f"Error loading profile picture: {str(e)}")
        return None
    

def check_profile_input_fields():
    """
    Validate and process the profile input fields.\n
            - Extract the required fields\n
            - Validate the input fields\n
            - check for password match\n
            - calculate and store body fat percentage

    Returns:\n
            - (dict): A dictionary containing the validated user information
            - (DeltaGenerator) If validation fails.
    """
    user_info = {key: st.session_state.pop(key) for key in list(st.session_state.keys()) # All key-vals required in the form
        if key in User_Info_Series.__annotations__.keys() and not key.startswith('opt_')}
    
    if not all(user_info.values()): return st.error("Required fields left blank") # Empty fields
    
    if user_info['password'] != st.session_state.pop('password_check'): return st.error("Passwords don't match") # Passwords don't match

    user_info['body_fat_percentage'] = calc_body_fat_percentage(user_info)    

    return user_info