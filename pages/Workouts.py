import json
import streamlit as st
import pandas as pd
from db_operations import db_operations

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.error("You must log in first.")
    st.stop()

db_ops: db_operations = st.session_state.db_ops

if 'creating_program' not in st.session_state:
    st.session_state.creating_program = False
if 'editing_program' not in st.session_state:
    st.session_state.editing_program = None
if 'program_view' not in st.session_state:
    st.session_state.program_view = None

if 'update_from_db' not in st.session_state:
    st.session_state.public_programs = db_ops.select_query("SELECT * FROM v_public_programs LIMIT 501;")
    st.session_state.custom_programs = db_ops.select_query("CALL get_user_programs(:user_id);", {'user_id': int(st.session_state.user_info['user_id'])})
    st.session_state.update_from_db = False
    print("***Public Programs***\n".center(st.session_state['max_len']), st.session_state.public_programs)
    print("\n***Custom Programs***\n".center(st.session_state['max_len']), st.session_state.custom_programs)
if 'update_from_db' == True:
    st.session_state.public_programs = db_ops.select_query("SELECT * FROM v_public_programs LIMIT 501;")
    st.session_state.custom_programs = db_ops.select_query("CALL get_user_programs(:user_id);", {'user_id': int(st.session_state.user_info['user_id'])})
    st.session_state.update_from_db = False


def get_filtered_programs(program_view):
    """
    Filters public or custom programs based on the selected filters

    Returns:\n
            - (DataFrame): The filtered programs based on the user's selection.
    """

    if program_view == "Public Programs":
        programs = st.session_state.public_programs
    else:
        programs = st.session_state.custom_programs

    st.sidebar.header("Filters")
    selected_days = st.sidebar.multiselect(
        "Days/Week",
        options=programs['days_per_week'].unique(),
        default=None
    )
    selected_focuses = st.sidebar.multiselect(
        "Focus",
        options=programs['focus'].unique(),
        default=None
    )

    if selected_days:
        programs = programs[programs['days_per_week'].isin(selected_days)]
    if selected_focuses:
        programs = programs[programs['focus'].isin(selected_focuses)]

    return programs


def display_workout_exercise(p_id, w_id, e_id, exercise):
    """
    Display details of a specific exercise within a workout.

    This function shows the name and muscle group of the exercise and provides
    a button to toggle the display of detailed exercise information, including sets,
    reps, and description.

    Args:
        p_id (int): The program ID.
        w_id (int): The workout ID.
        e_id (int): The exercise ID.
        exercise (Series): The exercise details as a pandas Series.
    """
    if f"p_{p_id}_w_{w_id}_exercise_{e_id}_is_expanded" not in st.session_state:
        st.session_state[f"p_{p_id}_w_{w_id}_exercise_{e_id}_is_expanded"] = False
    is_expanded = st.session_state[f"p_{p_id}_w_{w_id}_exercise_{e_id}_is_expanded"]
    muscle_group = exercise['muscle_group']

    f"**{exercise['name']}**"
    muscle_group
    

    st.button( # Toggle workout details
        f"{'Hide' if is_expanded else 'Show'} Exercise Details",
        key=f"p_{p_id}_w_{w_id}_exercise_{e_id}_details_button",
        on_click=lambda state_key=f"p_{p_id}_w_{w_id}_exercise_{e_id}_is_expanded": 
        st.session_state.update({state_key: not st.session_state[state_key]}))

    if is_expanded:
        sets = json.loads(exercise['sets_and_reps']) if exercise['sets_and_reps'] else []
    
        for set in sets:
            f"Set {set['set_number']} X {set['reps_or_distance']} {'Reps' if muscle_group != 'Cardio' else 'Miles'}"

        exercise['description']
    "---"    


def display_program_workout(p_id, w_id, workout):
    """
    Display details of a specific workout within a program.

    This function shows the day number and workout name, and provides a button to
    toggle the display of detailed workout information, including exercises within the workout.
    
    Args:
        p_id (int): The program ID.
        w_id (int): The workout ID.
        workout (Series): The workout details as a pandas Series.
    """
    col1, col2 = st.columns(2)

    if f"p_{p_id}_workout_{w_id}_is_expanded" not in st.session_state:
        st.session_state[f"p_{p_id}_workout_{w_id}_is_expanded"] = False
    is_expanded = st.session_state[f"p_{p_id}_workout_{w_id}_is_expanded"]

    with col1:
        f"## Day {workout['day_number']}"

        st.button( # Toggle workout details
            f"{'Hide' if is_expanded else 'Show'} Workout Details",
            key=f"p_{p_id}_workout_{w_id}_details_button",
            on_click=lambda state_key=f"p_{p_id}_workout_{w_id}_is_expanded": 
            st.session_state.update({state_key: not st.session_state[state_key]}))
    
    if is_expanded:
        exercises = db_ops.select_query("CALL get_workout_exercises(:w_id);", {'w_id': w_id})
        with col1:
            f"**{workout['workout_name']}**"
            f"Duration: {workout['approx_duration']} Mins"
        with col2:
            for index, exercise in exercises.iterrows():
                display_workout_exercise(p_id, w_id, int(exercise['exercise_id']), exercise)
    
    "---"


def bind_curr_prog_db():
    """
    For the current user, update current_program in the DB to their selected program's program_id
    """
    user_info = st.session_state.user_info
    db_ops.modify_query("UPDATE user SET current_program = :current_program WHERE user_id = :user_id",
        {'current_program': int(user_info['current_program']['program_id']), 'user_id': int(user_info['user_id'])})


def unbind_curr_prog_db():
    """
    For the current user, sets current_program to NULL in the DB
    """
    user_info = st.session_state.user_info
    db_ops.modify_query("UPDATE user SET current_program = NULL WHERE user_id = :user_id",
        {'user_id': int(user_info['user_id'])})


def stop_current_program():
    """
    Stop the user's current program.
    """
    st.session_state.user_info['current_program'] = None
    user_id = st.session_state.user_info['user_id']
    db_ops.modify_query("UPDATE user SET current_program = NULL WHERE user_id = :user_id", {'user_id': int(user_id)})
    st.success('Program stopped successfully.')
    print(f"Current program after 'Stop Program' pressed: \n{st.session_state.user_info.get('current_program')}") # print statement for debugging


def display_active_program():
    """
    Display details for the user's current active program.
    """
    program = st.session_state.user_info['current_program']
    workouts = json.loads(program['workouts']) if program['workouts'] else []

    col1, col2 = st.columns([1, 2])

    with col1:
        f"## {program['program_name']}"
        "**Focus:**", program['focus']
        "**Days/Week:**", str(program['days_per_week'])
        f"**Description:** {program['description']}"
    with col2:
            for workout in workouts:
                display_program_workout(int(program['program_id']), int(workout['workout_id']), workout)
    "---"


def display_program(p_id, program):
    """
    Display `program` details and options for interacting with `program`\n
        - interaction options depend on `program_view`
        - Options for all views (EXCEPT '`My Current Program`'):\n
            - `Show/Hide Details`
            - `Start Program`
        - Additional options when `program_view` == '`My Custom Programs`':\n
            - `Edit Program`

    Args:\n
        - `index` (int): The index of the program in the list.
        - `program` (Series): The program details as a pandas Series.
    """
    col1, col2 = st.columns([1, 2])

    if f"program_{p_id}_is_expanded" not in st.session_state:
        st.session_state[f"program_{p_id}_is_expanded"] = False
    is_expanded = st.session_state[f"program_{p_id}_is_expanded"]

    with col1:
        f"## {program['program_name']}"

        st.button( # Toggle program details
            f"{'Hide' if is_expanded else 'Show'} Program Details",
            key=f"program_details_button_{p_id}",
            on_click=lambda state_key=f"program_{p_id}_is_expanded": 
            st.session_state.update({state_key: not st.session_state[state_key]}))
        
        st.button( # Start program
            "Start This Program",
            key=f"start_button_{p_id}",
            on_click=lambda p=program: st.session_state.user_info.update({'current_program': p}),
            disabled=(st.session_state.user_info['current_program'] is not None and \
                        st.session_state.user_info['current_program']['program_id'] == program['program_id'])
        )
        
        if st.session_state['program_view'] == "My Custom Programs":
            st.button( # Edit program
                "Edit Program",
                key=f"edit_program_{p_id}",
                on_click=lambda p=program: st.session_state.update({'editing_program': p})
            )

    if is_expanded:
        workouts = json.loads(program['workouts']) if program['workouts'] else []
        with col1:
            "**Focus:**", program['focus']
            "**Days/Week:**", str(program['days_per_week'])
            f"**Description:** {program['description']}"
        with col2:
            for workout in workouts:
                display_program_workout(p_id, int(workout['workout_id']), workout)

    "---"


def render_program_view():
    """
    Render the program selection interface and generate the selected programs.

    Also handles updating `st.session_state` and the `Data Base` accordingly

    See Also:
        - `get_filtered_programs()`: Filters programs based on user selection.
        - `display_active_program()`: Displays the details of the active program.
        - `display_programs()`: Displays a list of programs with options.
        - `stop_current_program()`: Stops the current program.
        - `bind_curr_prog_db()`: Binds the current program to the user in the database.
        - `unbind_curr_prog_db()`: Unbinds the current program from the user in the database.
    """
    
    program_view = st.session_state.program_view = st.selectbox(
        "Which programs would you like to view?",
        options=["Public Programs", "My Custom Programs", "My Current Program"],
        index= 0 if st.session_state.user_info['current_program'] is None else 2
    )

    col1, col2, col3 = st.columns(3)
    with col1: "# Programs"
    with col2: "# Workouts"
    with col3: "# Exercises"
    "---"

    if program_view == "My Current Program":
        if st.session_state.user_info['current_program'] is None: 
            unbind_curr_prog_db()
            st.write("You're not on a program currently")
            return
        elif isinstance(st.session_state.user_info['current_program'], pd.Series):
            display_active_program()
            st.button(
                "Stop Program",
                on_click=stop_current_program
            )
            bind_curr_prog_db()
            return
        else: # //current_program still stores int value from db
            st.session_state.user_info['current_program'] = db_ops.first_row("CALL get_active_program_details(:program_id)",
            {'program_id': int(st.session_state.user_info['current_program'])})
            return

    # get programs based on program view and active filters
    for index, program in get_filtered_programs(program_view).iterrows():
        display_program(int(program['program_id']), program)


def create_new_program(creator_id):
    """
    ***MAKE THIS FUNCTION***

    Handle the creation of a new `program` and the `workouts` within
        - User can store as many `workouts` in a `program` as they wish:
            - User can create new `workouts` to store in the `program`
            - or pick from the `workouts` in `public programs`
            - or a combination of both
            - When creating new `workouts`:
                - User can store as many `exercises` as they wish in each `workout`
                - User can create new `exercises`
                - or pick from preexisting `exercises` in the `exercise` db table
                - or a combination of both
    
    Store the details of the new program in the database
        - This could mean updating none, 1 or many of the following tables\n
            - `program`
            - `workout`
            - `exercise`
            - `program_workout`
            - `workout_exercise`

    Update `st.session_state.custom_programs` - this can be done using the same query it was initialized with
    
    If program was made public
        - update `st.session_state.public_programs` - this can also be done using the same query it was initialized with
    """
    program_name = st.session_state['new_program_name']
    days_per_week = int(st.session_state['new_program_days_per_week'])
    selected_workouts = st.session_state['new_program_selected_workouts']

    if not program_name or not days_per_week or not selected_workouts:
        st.error("Please fill out all fields.")
        return

    # Create a new program
    db_ops.modify_query(
        "INSERT INTO program (creator_id, program_name, days_per_week) VALUES (:user_id, :program_name, :days_per_week)",
        {'user_id': int(creator_id), 'program_name': program_name, 'days_per_week': days_per_week}
    )
    
    # Commit the transaction to ensure the new program is available
    db_ops.commit()

    # Get the new program ID
    query = "SELECT program_id FROM program WHERE creator_id = :creator_id AND program_name = :program_name"
    program_id = db_ops.first_row_first_attr(query, {'creator_id': int(creator_id), 'program_name': program_name})

    if program_id is None:
        st.error("Program not uploaded")
        return
    
    # Create inputs for assigning days to workouts
    workout_days = {}
    for workout in selected_workouts:
        workout_days[workout] = st.selectbox(f"Day for {workout}", options=list(range(1, days_per_week + 1)), key=f"{workout}_day")

    # Add workouts to the program with assigned days
    for workout_name in selected_workouts:
        workout_id = db_ops.first_row_first_attr(
            "SELECT workout_id FROM workout WHERE workout_name = :workout_name",
            {'workout_name': workout_name}
        )
        day_number = workout_days[workout_name]
        db_ops.modify_query(
            "INSERT INTO program_workout (program_id, workout_id, day_number) VALUES (:program_id, :workout_id, :day_number)",
            {'program_id': int(program_id), 'workout_id': int(workout_id), 'day_number': day_number}
        )
    

    # Commit the transactions for adding workouts and exercises
    db_ops.commit()
    

    st.session_state.update_from_db = True
    st.success("Program created successfully!")


def show_new_program_form():
    """
    ***MAKE THIS FUNCTION***

    Renders the `new_program_form` and handles the creation of a new prorgam


    Make Also:
        - form_submit_button-`Create Program` (on_click) = `create_new_program()`
    """
    "# Create New Program"
    with st.form("new_program_form"):
        program_name = st.text_input("Program Name", key='new_program_name')
        days_per_week = st.slider("Days per Week", min_value=1, max_value=7, value=3, key='new_program_days_per_week')
        
        # Fetch all available workouts and exercises
        workout_options = db_ops.select_query("SELECT workout_id, workout_name FROM workout")
        workout_names = workout_options['workout_name'].tolist() if not workout_options.empty else []
        st.multiselect("Select Workouts", workout_names, key='new_program_selected_workouts')
        
        st.form_submit_button("Create Program", on_click=lambda: create_new_program(st.session_state.user_info['user_id']))


def run():
    if st.session_state.creating_program:
        show_new_program_form()
        st.sidebar.button("Back to Programs", on_click=lambda: st.session_state.update({'creating_program': False}))
    else: # View programs - logic should place us here on first entry
        render_program_view()
        st.sidebar.button("Create New Program", on_click=lambda: st.session_state.update({'creating_program': True}))
    
    st.sidebar.markdown("---")    
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear(), disabled=st.session_state.editing_profile)


if __name__ == "__main__":
    run()