import pandas as pd
from sqlalchemy import create_engine, text

class db_operations:
    """
    Handles database operations for the fitness application.

    Functions:
    - __init__(): Initializes the database connection
    - modify_query(query, params): Executes insert/update/delete queries with optional parameters
    - select_query(query, params): Executes select queries with optional parameters
    - first_row(query, params): Retrieves the first row of a select query with optional parameters
    - first_row_first_attr(query, params): Retrieves the value of the first row's first attribute of a select query with optional parameters
    - close(): Closes the connection with the database
    """

    def __init__(self):
        """
        Initializes the database connection using SQLAlchemy.

        Connects to the MySQL database using the provided credentials.
        Sets the transaction isolation level to READ COMMITTED.
        """
        db_username = "root"
        db_password = "CPSC408!"
        db_host = "127.0.0.1"
        db_database = "Fitness"
        self.engine = create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_database}")
        self.conn = self.engine.connect()
        print("\n\nConnection made...\n\n")


    def commit(self):
        self.conn.commit()


    def connect(self):
        """
        Reconnects to database if connection is lost due to an error
        """
        if self.conn is not None:
            self.conn.close()
        self.conn = self.engine.connect()
        print("\n\nConnection refreshed...\n\n")


    def modify_query(self, query, params=None):
        """
        Executes modify queries, with optional parameters for queries with placeholders.

        Parameters:
        - query (str): The SQL modify query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.
        """

        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params) if params is not None else conn.execute(text(query))
        except Exception as e:
            print(f"Error: {e}")
            self.connect()  # Refresh the connection
            with self.engine.begin() as conn:
                conn.execute(text(query), params) if params is not None else conn.execute(text(query))


    def select_query(self, query, params=None):
        """
        Executes select queries, with optional parameters for queries with placeholders.

        Parameters:
        - query (str): The SQL select query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - DataFrame: The result set of the select query.
        """
        try:
            return pd.read_sql_query(text(query), self.conn, params=params) if params is not None else pd.read_sql_query(text(query), self.conn)
        except Exception as err:
            print(f"Error: {err}")
            print(f"query = {query}")
            print(f"params = {params}")
            self.connect()  # Attempt to reconnect
            return pd.read_sql_query(text(query), self.conn, params=params) if params is not None else pd.read_sql_query(text(query), self.conn)
        

    def first_row(self, query, params=None) -> (pd.Series | None):
        """
        Executes a query and returns the first row of the result set, with optional parameters.

        Parameters:
        - query (str): The SQL query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - tuple: The first row of the result set.
        """
        result = self.select_query(query, params)
        return result.iloc[0] if not result.empty else None
    
    
    def first_row_first_attr(self, query, params=None):
        """
        Executes a query and returns the first attribute of the first row of the result set, with optional parameters.

        Parameters:
        - query (str): The SQL query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - any: The first attribute of the first row of the result set.
        """
        first_row = self.first_row(query, params)
        return first_row[0] if first_row is not None else None
        

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
