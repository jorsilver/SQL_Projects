import streamlit as st
import pandas as pd
from Hello import db_ops
import utils

# Setting page configuration
st.set_page_config(page_title="Workouts", page_icon="🏋️‍♂️", layout="wide")

# Check if the user is authenticated before showing the content
# if not st.session_state.get('authenticated', False):
#     st.error("You must log in first.")
#     st.stop()

# def fetch_programs():
#     query = """
#     SELECT program_id, program_name
#     FROM program
#     LIMIT 10;
#     """
#     return db_ops.select_query(query)

# def fetch_workouts(program_id):
#     query = """
#     SELECT workout_name, approx_duration_mins
#     FROM workout
#     JOIN program_workout ON workout.workout_id = program_workout.workout_id
#     WHERE program_id = %s;
#     """
#     return db_ops.select_query(query, (program_id,))

# def display_programs():
#     st.title("Your Workout Programs")
#     programs = fetch_programs()
    
#     if programs:
#         for program in programs:
#             st.subheader(f"Program: {program[1]}")
#             workouts = fetch_workouts(program[0])
#             if workouts:
#                 for workout in workouts:
#                     st.write(f"Workout: {workout[0]}, Duration: {workout[1]} minutes")
#             else:
#                 st.write("No workouts found for this program.")
#     else:
#         st.write("No programs found.")

# def create_program():
#     st.sidebar.header("Create New Program")
#     program_name = st.sidebar.text_input("Program Name")
#     days_per_week = st.sidebar.number_input("Days per Week", min_value=1, max_value=7, step=1)
#     if st.sidebar.button("Create Program"):
#         user_id = st.session_state['user_info']['user_id']
#         query = "INSERT INTO program (creator_id, program_name, days_week) VALUES (%s, %s, %s);"
#         db_ops.modify_query(query, (user_id, program_name, days_per_week))
#         st.sidebar.success("Program created successfully!")

# if __name__ == "__main__":
#     if 'authenticated' in st.session_state and st.session_state['authenticated']:
#         display_programs()
#         create_program()
#     else:
#         st.error("You must log in to view this page.")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Function to fetch workout programs for the user
def get_public_workout_programs():
    query = "SELECT * FROM v_public_programs LIMIT 501"
    return db_ops.select_query(query)

# Function to display the user's workout programs
def show_public_workout_programs():
    user_info = st.session_state['user_info']
    st.header("Workout Programs")
    
    workout_programs = get_public_workout_programs()
    
    if workout_programs:
        for program in workout_programs:
            # st.subheader(program['program_name'])
            # st.write(f"**Start Date:** {program['start_date']}")
            # st.write(f"**End Date:** {program['end_date']}")
            # st.write(f"**Description:** {program['description']}")
            # st.write(f"**Goals:** {program['goals']}")
            st.write(program)
    else:
        st.write("No workout programs found.")
        
def run():
    if st.session_state['authenticated']:
        show_public_workout_programs()
    else:
        st.error("Please log in to view your workout programs.")

if __name__ == "__main__":
    run()