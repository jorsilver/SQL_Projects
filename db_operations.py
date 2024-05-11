import mysql.connector

class db_operations():
    """
    Handles database operations for the ride-sharing application.

    Functions:
    - __init__(): Initializes the database connection
    - modify_query_params(query, dictionary): Executes insert/update/delete queries with named placeholders
    - select_query(query): Executes select queries
    - select_query_params(query, dictionary): Executes select queries with named placeholders
    - first_record(query): Retrieves the first row of a select query
    - first_record_params(query, dictionary): Retrieves the first row of a select query with named placeholders
    - first_row_first_attr(query): Retrieves the value of the first row's first attribute of a select query
    - first_row_first_attr_params(query, dictionary): Retrieves the value of the first row's first attribute of a select query with named placeholders
    - destructor(): Closes the connection with the database
    """
    def __init__(self):
        """
        Initializes the database connection.

        Connects to the MySQL database using the provided credentials.
        Sets the transaction isolation level to READ COMMITTED.
        """
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="CPSC408!",
            auth_plugin='mysql_native_password',
            database ="Fitness")
        self.cursor = self.connection.cursor(buffered=True)
        self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        print("Connection made..\n")

    def modify_query(self, query, params = None):
        """
        Executes insert/update/delete queries with named placeholders.

        Parameters:
        - query (str): The SQL modify query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - None
        """
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        self.connection.commit()

    def select_query(self, query, params = None):
        """
        Executes select queries, with optional parameters for queries with placeholders.

        Parameters:
        - query (str): The SQL select query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - list[(,),]: The result set of the select query.
        """
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        return self.cursor.fetchall()

    def first_row(self, query, params = None):
        """
        Retrieves the first row of a select query.

        Parameters:
        - query (str): The SQL select query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - tuple or None: The first row of the result set if available, else None.
        """
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        result_set = self.cursor.fetchall()
        return result_set[0] if result_set else None
    
    def first_row_first_attr(self, query, params = None):
        """
        Retrieves the value of the first row's first attribute of a select query.

        Parameters:
        - query (str): The SQL select query, optionally containing named placeholders.
        - params (dict, optional): A dictionary containing the values for the named placeholders, if any.

        Returns:
        - Any: The value of the first row's first attribute if available, else None.
        """
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result[0][0] if result else None
    
    def destructor(self):
        """
        Closes the connection with the database.

        Returns:
        - None
        """
        self.cursor.close()
        self.connection.close()