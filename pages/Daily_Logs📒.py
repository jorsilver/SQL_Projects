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
from Hello import db_ops  # Ensure this is imported correctly based on your project structure

# Setting page configuration
st.set_page_config(page_title="Daily Logs", page_icon="📈")

# Check if the user is authenticated before showing the content
if not st.session_state.get('authenticated', False):
    st.error("You must log in first.")
    st.stop()

def fetch_user_logs(user_id):
    query = """
    SELECT date, total_caloric_burn, total_caloric_intake, notes
    FROM daily_log
    WHERE user_id = %s
    ORDER BY date DESC;
    """
    return db_ops.select_query(query, (user_id,))

def add_daily_log(user_id, date, caloric_burn, caloric_intake, notes):
    query = """
    INSERT INTO daily_log (user_id, date, total_caloric_burn, total_caloric_intake, notes)
    VALUES (%s, %s, %s, %s, %s);
    """
    db_ops.modify_query(query, (user_id, date, caloric_burn, caloric_intake, notes))

def display_daily_logs():
    st.title("Your Daily Logs")
    
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        user_id = st.session_state['user_info']['user_id']
        logs = fetch_user_logs(user_id)
        if logs:
            for log in logs:
                st.subheader(f"Date: {log[0]}")
                st.write(f"Total Caloric Burn: {log[1]}")
                st.write(f"Total Caloric Intake: {log[2]}")
                st.write(f"Notes: {log[3]}")
        else:
            st.write("No daily logs found.")
    else:
        st.error("You must log in to view this page.")

    # Sidebar for adding new daily log
    st.sidebar.header("Add New Daily Log")
    with st.sidebar.form("new_log_form"):
        new_log_date = st.date_input("Date")
        new_caloric_burn = st.number_input("Total Caloric Burn", min_value=0)
        new_caloric_intake = st.number_input("Total Caloric Intake", min_value=0)
        new_notes = st.text_area("Notes")
        submit_new_log = st.form_submit_button("Add Log")

    if submit_new_log:
        add_daily_log(user_id, new_log_date, new_caloric_burn, new_caloric_intake, new_notes)
        st.success("New daily log added successfully!")

if __name__ == "__main__":
    display_daily_logs()