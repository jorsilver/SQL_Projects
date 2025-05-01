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
from datetime import time
from db_operations import db_operations

db_ops: db_operations = st.session_state.db_ops

# Check if the user is authenticated before showing the content
if not st.session_state.get('authenticated', False):
    st.error("You must log in first.")
    st.stop()

def fetch_user_logs(user_id):
    query = """
    SELECT date, total_caloric_burn, total_caloric_intake, notes
    FROM daily_log
    WHERE user_id = :user_id
    ORDER BY date DESC;
    """
    return db_ops.select_query(query, {'user_id': int(user_id)})

def add_daily_log(user_id: int):
    log_info = {key: st.session_state.pop(key) for key in list(st.session_state.keys()) # All key-vals required in the form
        if key in ['date', 'total_caloric_burn', 'total_caloric_intake', 'notes']}
    
    if not all(log_info.values()): return st.error("Required fields left blank") # Empty fields

    log_info['total_caloric_burn'] = int(log_info['total_caloric_burn'])
    log_info['total_caloric_intake'] = int(log_info['total_caloric_intake'])
    log_info['user_id'] = user_id
    print("***log_info***".center(st.session_state['max_len']), log_info)

    exercise_names = tuple(st.session_state.pop('exercise_names'))

    if exercise_names is None: return st.error("Must Select At Least One Exercise")

    attributes = ", ".join([key for key in log_info.keys()])
    values = ", ".join([f":{key}" for key in log_info.keys()])
    db_ops.modify_query(f"INSERT INTO daily_log\n({attributes})\nVALUES\n({values});", log_info)

    exercises = db_ops.select_query("SELECT exercise_id, name FROM exercise WHERE name IN :exercise_names;",
                            {'exercise_names': tuple(exercise_names)})
    
    start_time = time(st.session_state.pop('start_time'))
    duration_mins = int(st.session_state.pop('duration_mins'))
    log_id = int(db_ops.first_row_first_attr("SELECT log_id FROM daily_log WHERE user_id = :user_id ORDER BY date DESC LIMIT 1;", 
                {'user_id': int(user_id)}))
    
    db_ops.modify_query('''INSERT INTO session(log_id, start_time, duration_mins, cals_burned)
                        VALUES(:log_id, :start_time, :duration_mins, :cals_burned);''',
                        {'log_id': log_id, 'start_time': start_time, 'duration_mins': duration_mins, 'cals_burned': log_info['total_caloric_burn']})
    
    session_id = int(db_ops.first_row_first_attr("SELECT session_id FROM session WHERE log_id = :log_id ORDER BY start_time DESC LIMIT 1",
                    {'log_id': log_id}))
    
    with st.sidebar.form('add_exercise_info'):
        for index, exercise in exercises.iterrows():
            f"{exercise['name']}"
            st.number_input("Sets", key=f'exercise_{index}_num_sets')
            st.number_input("Max Reps", key=f'exercise_{index}_max_reps')
            st.number_input("Max Weight", key=f'exercise_{index}_max_weight')

        # if st.sidebar.form_submit_button("Add Exercises"):
        #     query = "INSERT INTO session_exercise(session_id, exercise_id, set_number, reps, weight)\nVALUES\n"
        #     for index, exercise in  exercises.iterrows():
        #         query += f"({session_id}, {exercise['exercise_id']}, UGHHHHH, {st.session_state.pop(f"exercise_{index}_max_reps")}, {st.session_state.pop(f"exercise_{index}_max_weight")})" * int(st.session_state.pop(f"exercise_{index}_num_sets"))

        if st.sidebar.form_submit_button("Add Exercises"):
            query = "INSERT INTO session_exercise(session_id, exercise_id, set_number, reps, weight)\nVALUES\n"
            values = []

            for index, exercise in exercises.iterrows():
                num_sets = int(st.session_state.pop(f"exercise_{index}_num_sets"))
                for set_num in range(1, num_sets + 1):
                    reps = st.session_state.pop(f"exercise_{index}_max_reps")
                    weight = st.session_state.pop(f"exercise_{index}_max_weight")
                    values.append(f"({session_id}, {exercise['exercise_id']}, {set_num}, {reps}, {weight})")

            query += ",\n".join(values) + ";"
            # Now you can execute the query using your database connection
            print(query)  # For debugging purposes



            db_ops.modify_query("INSERT INTO session")


def show_new_log_form(user_id):
    st.sidebar.header("Add New Daily Log")
    with st.sidebar.form("new_log_form"):
        st.date_input("Date", key='date')
        st.time_input("Start_time",value="now", key='start_time')
        st.number_input("Duration (mins)", key='duration_mins')
        st.multiselect("Exercises", options=db_ops.select_query("SELECT name from exercise"), default=None, key='exercise_names')
        st.number_input("Total Caloric Burn", key='total_caloric_burn')
        st.number_input("Total Caloric Intake", key='total_caloric_intake')
        st.text_area("Notes", key='notes')
        
        st.form_submit_button("Add Log", on_click=add_daily_log, args=(user_id,))

    st.success("New daily log added successfully!")

def add_workout():
    st.write("New Workout")


def display_daily_logs():
    st.title("Your Daily Logs")
    user_id = st.session_state['user_info']['user_id']
    logs = fetch_user_logs(user_id)
    if logs is not None:
        for index, log in logs.iterrows():
            st.subheader(f"Date: {log['date']}")
            st.write(f"Total Caloric Burn: {log['total_caloric_burn']}")
            st.write(f"Total Caloric Intake: {log['total_caloric_intake']}")
            st.write(f"Notes: {log['notes']}")
    else:
        st.write("No daily logs found.")

    st.sidebar.button("Add a New Daily Log,", on_click=show_new_log_form, args=(user_id,))
    
        

if __name__ == "__main__":
    display_daily_logs()