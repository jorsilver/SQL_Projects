from datetime import datetime

class helper():
    """
    Contains miscellaneous helper functions for the ride share application.

    Functions:
    - get_choice(prompt, lst): Prompts the user to select an option from a list of choices
    - get_float_input(min, max): Prompts the user to input a decimal number within a specified range
    - print_table(table): Prints a formatted table
    - generateTable(col_names, values, excl_cols): Generates a table given a list of column names and a 2D list of values
    - credentialCheck(credentials): Checks user credentials
    - get_formatted_time(time): Formats the given time since epoch
    """
    
    @staticmethod
    def get_choice(prompt, lst):
        """
        Prompts the user to select an option from a list of choices.

        Parameters:
        - prompt (str): The prompt message to display
        - lst (list): The list of valid choice numbers

        Returns:
        - int: The selected choice number
        """
        choice = input(prompt + "\nEnter choice number\n")
        while not choice.isdigit() or int(choice) not in lst:
            choice = input("Invalid option\n" + prompt + "\nEnter choice number\n")
        return int(choice)
    
    @staticmethod
    def get_float_input(min, max):
        """
        Prompts the user to input a decimal number within a specified range.

        Parameters:
        - min (float): The minimum allowed value
        - max (float): The maximum allowed value

        Returns:
        - float: The user-inputted decimal number
        """
        while True:
            try:
                number = float(input(f"Enter a decimal number between {min} and {max}\n"))
                if min <= number <= max:
                    return number
                print(f"{number} is not in the specified range")
            except ValueError:
                print("Invalid input: float decimal values only")

    @staticmethod
    def print_table(table):
        """
        Prints a formatted table.

        Parameters:
        - table (list): The table data to print

        Returns:
        - None
        """
        for row in table:
            print("|" + ("|".join(value for i, value in enumerate(row))) + "|")

    @staticmethod
    def generateTable(col_names, values, excl_cols):
        """
        Generates a table given a list of column names and a 2D list of values

        Parameters:
        - col_names (list): List of column names
        - values (list): List of values to populate the table
        - excl_cols (list): List of column indices to exclude

        Returns:
        - list: The formatted table
        """
        # Transpose values to their respective column
        table_data = list(zip(col_names, *values))
        # Calculate the maximum width for each column
        max_widths = [max(len(str(item)) for item in col) for col in table_data]
        # Add each formatted row to the table
        table = [[str(value).center(max_widths[i]) for i, value in enumerate(row) if i not in excl_cols] for row in zip(*table_data)]
        return table

    @staticmethod
    def credentialCheck(credentials):
        """
        Checks whether user credentials exist and if the user can provide the correct password.

        Parameters:
        - credentials (tuple): Tuple containing user credentials (ActType, Password, Name)

        Returns:
        - bool: True if credentials are correct, False otherwise
        """
        if not credentials:
            print("User not found")
            return False
        print("Welcome back", credentials[2])
        attempts = 0
        while input("Enter your password\n") != credentials[1]:
            attempts += 1
            if attempts == 5:
                print("\nToo many attempts")
                return False
            print("\nIncorrect password, try again")
        return True

    @staticmethod
    def get_formatted_time(time):
        """
        Formats the given time since epoch.

        Parameters:
        - time (float): Time in seconds since epoch

        Returns:
        - str: Formatted time string <hour(%12)>:<minute> <AM/PM>
        """
        date_time = datetime.fromtimestamp(time)
        return date_time.strftime("%I:%M:%S %p")