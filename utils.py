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

import inspect
import textwrap
from datetime import date

import streamlit as st


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

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
        height = height * 12
        feet = int(height// 12)
        inches = int(height % 12)
        formatted_height = f"{feet}' {inches}\""
        formatted_weight = f"{weight} lbs"
    else:  # unit_type == 'metric'
        formatted_height = f"{height} cm"
        formatted_weight = f"{weight} kg"
    
    return formatted_height, formatted_weight
