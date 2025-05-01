import streamlit as st
import mysql.connector
from datetime import datetime
import time

# Establish the database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="CPSC408!",
        auth_plugin='mysql_native_password',
        database="RideShare2")

# Streamlit page configuration
st.set_page_config(page_title="Ride Share App", layout="wide")

# Database Operations Class
class db_operations():
    def __init__(self):
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor(buffered=True)
        self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

# Helper Functions
class helper():
    @staticmethod
    def get_formatted_time(time):
        return datetime.fromtimestamp(time).strftime("%I:%M:%S %p")

# Streamlit App Logic
def main():
    db = db_operations()
    st.sidebar.title("Navigation")
    options = ["Log In", "Create New Account", "Exit"]
    choice = st.sidebar.selectbox("Choose an option:", options)

    if choice == "Log In":
        user_id = st.sidebar.text_input("Enter your user ID")
        submit = st.sidebar.button("Log In")
        if submit:
            log_in(user_id, db)
    elif choice == "Create New Account":
        create_new_user(db)
    elif choice == "Exit":
        st.sidebar.success("Goodbye!")
        db.close()

def log_in(user_id, db):
    query = "SELECT ActType, Password, Name FROM users WHERE userID = %s;"
    result = db.execute_query(query, (user_id,))
    if result:
        act_type, _, name = result[0]
        st.session_state['user_id'] = user_id
        st.session_state['user_name'] = name
        st.session_state['act_type'] = act_type
        user_dashboard(act_type, db)
    else:
        st.error("User not found.")

def create_new_user(db):
    st.header("Create New Account")
    act_type = st.radio("Account Type:", ["Rider", "Driver"])
    user_id = st.text_input("User ID")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if password == confirm_password:
            query = "INSERT INTO users (userID, Name, Password, ActType) VALUES (%s, %s, %s, %s);"
            db.execute_query(query, (user_id, name, password, act_type))
            db.commit()
            st.success("Account Created Successfully!")
        else:
            st.error("Passwords do not match.")

def user_dashboard(act_type, db):
    st.title(f"{act_type} Dashboard")
    if act_type == "Rider":
        rider_dashboard(db)
    elif act_type == "Driver":
        driver_dashboard(db)

def rider_dashboard(db):
    st.subheader("Rider Options")
    # Implement specific rider functionalities
    pass

def driver_dashboard(db):
    st.subheader("Driver Options")
    # Implement specific driver functionalities
    pass

if __name__ == "__main__":
    main()