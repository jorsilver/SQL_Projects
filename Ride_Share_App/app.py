"""
ride_share.py - A ride-sharing application module.

This module provides functionalities for a ride-sharing application, including user authentication,\n
ride booking and tracking, driver scheduling, and car management.

*Note: This module utilizes functions from the 'db_operations.py' and 'helper.py' modules, as well as the <time> and <threading> libraries.

Global Variables:
- max_search_time: Maximum time to wait for a driver to become available.
- wait_time (s): Wait time for a ride.
- trip_time (s): Trip time for a ride.
    *Note: Hardcoded values here for all rides... could be calculated using maps API

Functions:
- startScreen(): Landing page of the app
- logIn(): Handles user login
- newUser(): Creates a new user account
- inActiveRide(userID, actType): Retrieves ride status for a user
- riderMenu(userID): Main menu for riders
- driverMenu(userID): Main menu for drivers
- viewRating(userID, actType): Displays the average rating for a user
- viewRides(userID, actType): Displays the rides associated with a user
- rateRide(userID, actType): Allows a user to rate a ride
- addCar(userID): Allows a driver to add a new car to their account
- toggleDriverMode(userID): Allows a driver to toggle their driving mode
- takeRide(userID): Creates a new ride for a rider, if a driver can be found
- executeRide(wait, duration, driverName, driverID, VIN, destination): Simulates ride progress and notifications
"""
import time
import threading
from helper import helper
from db_operations import db_operations

db_ops = db_operations()

max_search_time = 20 #seconds

wait_time = 20.0 #seconds
trip_time = 40.0 #seconds

def startScreen():
    """
    Landing page when the application is opened and when the user logs out or just created their account.

    Returns:
    - None

    Displays a menu with options for the user to log in, create a new account, or exit the application.
    """
    while True:
        choice = helper.get_choice('''\n********************************************\n
            Welcome to the ride share app\n
            1.) Log In
            2.) Create New Acount
            3.) Exit\n''', [1,2,3])
        if choice == 1:
            logIn()
        if choice == 2:# Create new account
            prompt = '''\nWhat type of account would you like to create:
                1.) Rider
                2.) Driver\n'''
            actTypes = {1: "Rider", 2: "Driver"}
            newUser(actTypes[helper.get_choice(prompt, [1,2])])
        if choice == 3:# Log out
            print("Goodbye!")
            break

def logIn():
    """
    Login screen for all users.

    Returns:
    - None

    Prompts the user to enter their user ID and password, then directs them to their respective menu based on their account type.
    """
    userID = input("Enter your user ID\n")
    query = '''
        SELECT ActType, Password, Name
        FROM users
        WHERE userID = %s;'''
    credentials = db_ops.first_record_params(query, (userID,))
    if not helper.credentialCheck(credentials): return
    riderMenu(userID) if credentials[0] == "Rider" else driverMenu(userID)
    print(f"Goodbye {credentials[2]}")

def newUser(actType):
    """
    Gets input from the user to create a new account of the specified type.

    Parameters:
    - actType (str): The type of account to create ("Rider" or "Driver").

    Returns:
    - None

    Prompts the user to enter a user ID, name, and password, then adds the user to the database.
    """
    print(f"           Let's create a {actType} account")
    userID = input("Enter a number for your user ID\n")# User ID and name
    while not userID.isdigit() or db_ops.first_row_first_attr_params("SELECT userID FROM users WHERE userID = %s", (userID,)):
        userID = input("Try again: Positive integers only\n") if not userID.isdigit() else input("Try again: User ID already exists\n")
    name = input("Enter your first name\n")
    while True:# Password
        password = input("Enter your password\n")
        if password == input("Enter your password again\n"): break
        print("Passwords don't match")
    query = '''
        INSERT INTO users(userID, Name, Password, ActType)
        VALUES(%s,%s,%s,%s);'''# Add the user
    db_ops.modify_query_params(query, (userID, name, password, actType))

def inActiveRide(userID, actType):
    """
    Gets the origin and destination for an ongoing ride involving the specified user, if one exists.

    Parameters:
    - userID (int): The ID of the user.
    - actType (str): The type of user ("Rider" or "Driver").

    Returns:
    - list or []: A list containing the pick-up and drop-off addresses if an ongoing ride exists, else []].
    """
    query = f'''
        SELECT PickUpAdr, DropOffAdr
        FROM rides
        WHERE {actType}ID = %s AND arvlTime IS NULL;'''
    return  db_ops.first_record_params(query, (userID,))

def riderMenu(userID):
    """
    Menu for users who log in to a rider account.

    Parameters:
    - userID (int): The ID of the rider

    Returns:
    - None

    Displays a menu with the following options:
    - View Rating
    - View Rides
    - Rate A Ride
    - Take A Ride
    - Refresh Menu
    - Log Out

    Menu options vary depending on whether or not the user is in an ongoing ride.

    If the user is in an ongoing ride, information about the ride is also displayed.
    """
    while True:
        taking_ride = inActiveRide(userID, "Rider")# Check ride status
        menu = '''\n********************************************\n
              Rider Menu\n
            1.) View Rating
            2.) View Rides
            3.) Rate A Ride''' + ('''
            4.) Take A Ride''' if not taking_ride else "\n") + '''
            5.) Refresh Menu
            6.) Log Out''' + (f'''\n
            You're currently taking a ride
            |Origin: '{taking_ride[0]}'|Destination: '{taking_ride[1]}'|''' if taking_ride else "\n")
        choices = [1,2,3,4,5,6] if not taking_ride else [1,2,3,5,6]
        choice = helper.get_choice(menu, choices)

        taking_ride = inActiveRide(userID, "Rider")# Waited for user input - check ride status again
        if choice == 1: # View Rating
            print("            My rating\n" + viewRating(userID, "Rider") + " stars")
        if choice == 2: # View Rides
            helper.print_table(viewRides(userID, "Rider"))
        if choice == 3: # Rate a Ride
            rateRide(userID, "Rider")
        if choice == 4 and not taking_ride: # No changes to ride status while waiting for user input
            takeRide(userID)
        elif choice == 4: # A new ride was added from a different console
            print(f"Unable: Currently riding\n|Origin: '{taking_ride[0]}'|Destination: '{taking_ride[1]}'|")
        if choice == 6: # Log Out
            break

def driverMenu(userID):
    """
    Menu for users who log in to a driver account.

    Parameters:
    - userID (int): The ID of the driver

    Returns:
    - None

    Displays a menu with the following options:
    - View Rating
    - View Rides
    - Rate A Ride
    - Set Driving Status
    - Add New Car
    - Refresh Menu
    - Log Out

    Menu options vary depending on whether or not the user is in an ongoing ride.

    If the user is in an ongoing ride, information about the ride is also displayed.
    """
    while True:
        giving_ride = inActiveRide(userID, "Driver")# Check ride status
        menu = '''\n********************************************\n
              Driver Menu\n     
            1.) View Rating
            2.) View Rides
            3.) Rate a Ride''' + ('''
            4.) Set Driving Status''' if not giving_ride else "\n") + '''
            5.) Add New Car
            6.) Refresh Menu
            7.) Log Out''' + (f'''\n
            You're currently giving a ride
            |Origin: '{giving_ride[0]}'|Destination: '{giving_ride[1]}'|''' if giving_ride else "\n")
        choices = [1,2,3,4,5,6,7] if not giving_ride else [1,2,3,5,6,7]
        choice = helper.get_choice(menu, choices)

        giving_ride = inActiveRide(userID, "Driver")# Waited for user input - check ride status again
        if choice == 1: # View Rating
            print("           My rating\n" + viewRating(userID, "Driver") + " stars")
        if choice == 2: # View Rides
            helper.print_table(viewRides(userID, "Driver"))
        if choice == 3: # Rate a Ride
            rateRide(userID, "Driver")
        if choice == 4 and not giving_ride: # No changes to ride status while waiting for user input
            toggleDriverMode(userID)
        elif choice == 4: # A new ride was added from a different console
            print(f"Unable: Currently on a ride\n|Origin: '{giving_ride[0]}'|Destination: '{giving_ride[1]}'|")
        if choice == 5: # Add New Car
            addCar(userID)
        if choice == 7: # Log Out, set all the driver's cars' Availability to 0
            db_ops.modify_query_params("CALL switch_cars(%s, %s);", (userID, 'N/A'))
            break

def viewRating(userID, actType):
    """
    View the average rating of a user (rider or driver).

    Parameters:
    - userID (int): The ID of the user.
    - actType (str): The type of user ("Rider" or "Driver").

    Returns:
    - str: A string containing the average rating of the user.
    """
    query = f'''
        SELECT AVG({actType}Rtg)
        FROM rides
        WHERE {actType}ID = %s;
    '''
    return "            " + str(db_ops.first_row_first_attr_params(query, (userID,)))

def viewRides(userID, actType):
    """
    Collects all the rides associated with a user, and creates a table of them, only including the attributes that type of user should see.

    Parameters:
    - userID (int): The ID of the user.
    - actType (str): The type of user ("Rider" or "Driver").

    Returns:
    - list[list[]]: A formated table of the user's rides, with columns excluded based on user type.
    """
    cols = [row[0] for i, row in enumerate(db_ops.select_query("DESCRIBE rides;")) if i > 3]
    query = ("        SELECT rides.RideID, r.Name, d.Name, c.Make, c.Model, " +
        ", ".join([f"rides.{col}" for i, col in enumerate(cols)]) +
        f'''
            FROM rides
            INNER JOIN users r ON rides.RiderID = r.userID
            INNER JOIN users d ON rides.DriverID = d.userID
            INNER JOIN cars c ON rides.VIN = c.VIN
            WHERE rides.{actType}ID = %s
            ORDER BY rides.ReqTime DESC;''')
    rides = db_ops.select_query_params(query,(userID,))
    cols = ["RideID", "RiderName", "DriverName", "Make", "Model"] + cols
    hide_cols = [2, 7] if actType == "Driver" else [1,8]
    return helper.generateTable(cols, rides, hide_cols)

def rateRide(userID, actType):
    """
    Rate a ride that the user is associated with, for the opposite party (<<rider> rates <driver>> & <<driver> rates <rider>>)

    Parameters:
    - userID (int): The ID of the user.
    - actType (str): The type of account ("Rider" or "Driver")

    Steps:
    1 Display the user's most recent ride
    2 User can either rate that ride or see all their rides and choose one to rate
    3 Prompt the user for a decimal value betwen 1 and 5
    4 Set the chosen rides' opposite party's rating attribute to the given value

    Returns:
    None
    """
    act_to_rate = "Driver" if actType == "Rider" else "Rider"
    rides = viewRides(userID, actType)
    print("\nYour most recent ride:\n")
    helper.print_table(rides[:2])
    if helper.get_choice("\n1.) Rate this ride\n2.) Rate a different ride\n", [1,2]) == 1:
        rating = helper.get_float_input(0,5)
        db_ops.modify_query_params(f"UPDATE rides\nSET {act_to_rate}Rtg = %s\nWHERE RideID = %s", (rating, rides[1][0]))
    else:
        helper.print_table(rides)
        choices = [int(choice.strip()) for choice in list(zip(*rides))[0][1:]]
        ride_choice =  helper.get_choice("Enter the ride ID for the ride you wish to rate", choices)
        helper.print_table([rides[0], rides[choices.index(ride_choice)+1]])
        rating = helper.get_float_input(0,5)
        db_ops.modify_query_params(f"UPDATE rides\nSET {act_to_rate}Rtg = %s\nWHERE RideID = %s", (rating, ride_choice))
        
def addCar(userID):
    """
    Add a new car to the user's account.

    Parameters:
    - userID (int): The ID of the user

    Steps:
    1 Prompt the user for car details
        - VIN, plate number, make, model
    2 Check that the car doesn't already exist in the database
    3 If the car is unique, insert a new record into the database with the given values and the user's ID

    Returns:
    None
    """
    vin = input("\nEnter the VIN number for the vehicle you wish to add\n")
    existing_car_owner = db_ops.first_row_first_attr_params("SELECT OwnerID FROM cars WHERE VIN = %s", (vin,))
    if existing_car_owner: return print("           This car already belongs to" + 
        f"user {existing_car_owner}" if existing_car_owner != userID else "you")
    plateNum = input("Enter the license plate number\n")
    make = input("Enter the car make (Ford, Toyota, Bugatti,...)\n")
    model = input("Enter the car model (Fiesta, Camry, Chiron,...)\n")
    query = '''
        INSERT INTO cars(VIN, OwnerID, PlateNum, Make, Model)
        VALUES(%s,%s,%s,%s,%s);'''
    values = (vin, userID, plateNum, make, model)
    db_ops.modify_query_params(query, values)

def toggleDriverMode(userID):
    """
    Toggle the driving mode for the user.

    Steps:
    1 User can either Start driving, switch vehicles, or finish driving
    2 If the user doesn't want to finish driving, all their available cars are displayed
    3 The user then picks a car to switch to
    4 The availabilty flags are adjusted accordingly for both
        - The car they are switching out of (if applicable)
        - The car they are switching into (if applicable)

    Parameters:
    - userID (int): The ID of the user.

    Returns:
    None
    """
    query = '''SELECT VIN
               FROM cars
               WHERE Available = 1 AND ownerID = %s'''
    in_car = db_ops.first_row_first_attr_params(query, (userID,))
    if not in_car or helper.get_choice("Would you like to\n1.) Switch cars\n2.) Finish driving\n", [1,2]) == 1:
        query = '''
            SELECT VIN, Make, Model, PlateNum
            FROM cars
            WHERE Available = 0 AND OwnerID = %s'''
        cars = db_ops.select_query_params(query, (userID,))
        car_dict = {}
        for i, car in enumerate(cars):
            print(f"           {i+1}.) {car[1]} {car[2]} - Plane Number: {car[3]}")
            car_dict[i+1] = car[0]
        new_vin = car_dict[helper.get_choice("\nWhich car are you driving\n", car_dict.keys())]
        db_ops.modify_query_params("CALL switch_cars(%s, %s);", (userID, new_vin))
    else:
        db_ops.modify_query_params("CALL switch_cars(%s, %s);", (userID, 'N/A'))

def takeRide(userID):
    """
    Initiates the process of finding and booking a ride for a given user.

    Parameters:
    - userID (int): The ID of the user requesting the ride
    
    Steps:
    1. Searches for an available driver until an available driver is found or the maximum search time is reached
    3. Adds the ride(with many values null at this point) and reserves the found driver by fliping their availabilty flag
    4. Displays the driver name and their rating to the user
    5. Prompts the user for pick-up and drop-off addresses and adds them to the ride
    7. Displays ride information to the user including
        - Ride ID
        - Pick up location and approximate pick up time
        - Car make, model, & license plate num
    8. Tracks ride progress and generates ride notifications through a separate thread

    Returns:
    - None: Prints relevant information about the ride status and driver availability.
    """
    query = '''
        SELECT OwnerID, VIN, Make, Model, PlateNum
        FROM cars
        WHERE Available = 1;'''
    print("            Searching for driver...\n")
    attempts = 0
    available_driver = db_ops.first_record(query)
    while not available_driver and attempts < max_search_time/2:
        attempts += 1
        print("            Searching...\n")
        time.sleep(2)
        available_driver = db_ops.first_record(query)
    if not available_driver: return print("            No drivers available")
    db_ops.modify_query_params("CALL switch_cars(%s, %s);", (available_driver[0], 'N/A'))
    query = '''
        INSERT INTO rides(RiderID, DriverID, VIN)
        VALUES(%s,%s,%s);'''
    db_ops.modify_query_params(query,  (userID, available_driver[0], available_driver[1]))
    name = db_ops.first_row_first_attr_params("SELECT Name\nFROM users\nWHERE userID = %s", (available_driver[0],))
    print(f"            Driver found\n            {name}\n{viewRating(available_driver[0], "Driver")} stars\n")
    origin = input("Where would you like to be picked up?\n")
    dest = input("Where would you like to go?\n")
    rideID = db_ops.first_row_first_attr_params("SELECT rideID\nFROM rides\nWHERE riderID = %s\nORDER BY ReqTime DESC", (userID,))
    db_ops.modify_query_params("UPDATE rides\nSET PickUpAdr = %s, DropOffAdr = %s\nWHERE RideID = %s", (origin, dest, rideID))
    print(f'''
        {name} is on the way!\n
        Ride ID: {rideID}
        Picking up at: '{origin}'
        At: {helper.get_formatted_time(time.time() + wait_time)} (approximately)
        Car: {available_driver[2]} {available_driver[3]}
        License plate number: {available_driver[4]}\n''')
    thread = threading.Thread(target=executeRide, args=(wait_time, trip_time, name, available_driver[0], available_driver[1], dest))
    thread.start()

def executeRide(wait, duration, driverName, driverID, VIN, destination):
    """
    Simulates the ride progress and displays ride notifications.\n
        *Note: This function is called on a separate thread to execute concurrently with other operations

    Parameters:
    - wait (float): Time to wait for the driver to arrive
    - duration (float): Duration of the ride
    - driverName (str): Name of the driver
    - driverID (int): ID of the driver
    - VIN (str): Vehicle Identification Number of the vehicle in use
    - destination (str): Destination of the ride

    Steps:
    - Waits for a specified time, then notify the user when the driver arrives at the pick up location\n
    - Wait for another period of time, then notify the user they have arrived at the destination\n
    - Switches the driver's availability back

    Returns:
    - None
    """
    time.sleep(wait)
    print(f'''\n
          ***'{driverName}' HAS ARRIVED***
          You will arrive at '{destination}' at approximately {helper.get_formatted_time(time.time() + duration)}\n''')
    time.sleep(duration)
    print(f"\n\n           ***YOU HAVE ARRIVED AT '{destination}'***\n\n")
    db_ops.modify_query_params("CALL switch_cars(%s, %s);", (driverID, VIN))
    
startScreen()