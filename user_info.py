from datetime import date
from pandas import Series

class User_Info_Series(Series):
    """
    A class to store user information in a pandas Series-like structure.

    This class extends the pandas Series class to include user-specific attributes

    Attributes:\n
            - `user_id` (int): The user's unique identifier.
            - `username` (str): The user's username.
            - `password` (str): The user's password.
            - `current_program` (int): The user's current fitness program identifier.
            - `first_name` (str): The user's first name.
            - `last_name` (str): The user's last name.
            - `height` (float): The user's height.
            - `weight` (float): The user's weight.
            - `body_fat_percentage` (float): The user's body fat percentage.
            - `dob` (date): The user's date of birth.
            - `gender` (str): The user's gender.
            - `unit_type` (str): The user's preferred unit type for height and weight.
            - `profile_pic_path` (str): The path to the user's profile picture.
    """
    user_id: int
    username: str
    password: str
    current_program: int
    first_name: str
    last_name: str
    height: float
    weight: float
    body_fat_percentage: float
    dob: date
    gender: str
    unit_type: str
    profile_pic_path: str

    def __init__(self, series=None):
        """
        Initialize the user info series.

        Args:
            series (Series, optional): A pandas Series containing user information. Defaults to None.
        """
        if series is not None:
            super().__init__(series)
            self.user_id = series.get("user_id", None)
            self.username = series.get("username", None)
            self.password = series.get("password", None)
            self.current_program = series.get("current_program", None)
            self.first_name = series.get("first_name", None)
            self.last_name = series.get("last_name", None)
            self.height = series.get("height", None)
            self.weight = series.get("weight", None)
            self.body_fat_percentage = series.get("body_fat_percentage", None)
            self.dob = series.get("dob", None)
            self.gender = series.get("gender", None)
            self.unit_type = series.get("unit_type", None)
            self.profile_pic_path = series.get("profile_pic_path", None)