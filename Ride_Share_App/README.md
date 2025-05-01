# Ride Share Application

This is a project for a ride share application using a MySQL database to store information on users, rides, and cars
and a Python program, which interacts with the database to provide a text based front end

## Identifying Information

* Name: Quang Thomas Ninh, Jordan Silver
* Student ID: 2432456, 2352988
* Email: qninh@chapman.edu, jorsilver@chapman.edu
* Course: CPSC 408
* Assignment: Assignment 5 Ride Share App

## Source Files  

* [app.py](app.py)
* [helper.py](helper.py)
* [db_operations.py](db_operations.py)
* [data_dump.sql](data-dump.sql)
* [DDL statements](Tables_Procedures_Triggers.sql)
* [ERD & Schema](ERD&Schema.pdf)

## The Python Program

* Allows users to book rides and manage their accounts.
* Insures seamless comunication between the database and sevral instances of the application at the same time
* Tracks ride progress and generates ride notifications through separate threads

Files and their functionalities:

1. **`app.py`**: Contains the main logic for handling user inputs, processing requests, and displaying outputs
2. **`helper.py`**: Provides miscellaneous helper functions used throughout the application, such as input validation, formatting output, and credential checking.
3. **`db_operations.py`**: Encapsulates database operations, including querying the database for user information, inserting new records, updating existing records, and deleting data.

## The Database

- **`users`**: Stores details about users, including their user ID, name, password, and account type (rider or driver).
- **`cars`**: Contains information about cars available for rides, including the VIN (Vehicle Identification Number), owner ID, license plate number, make, model, and availability status.
- **`rides`**: Tracks information about rides booked by users, including the ride ID, rider ID, driver ID, VIN of the car used for the ride, request time, arrival time, driver rating, rider rating, pickup address, and drop-off address.

## MySQL Dump

import [data_dump.sql](data-dump.sql) as a new data source. If you have problems with that use the [DDL statements](Tables_Procedures_Triggers.sql)

## References
- Class slides
- https://www.geeksforgeeks.org/zip-in-python/
- https://docs.python.org/3/library/threading.html

## Known Errors

- No known errors.
- Program has been successfully tested and reviewed.

## Build Instructions

- Ensure python is installed and an instance of MySQL is running and accessible.
- Build the database with the data dump
- Modify the database connection credentials in [db_operations.py](db_operations.py)

## Execution Instructions

- Once the database is set up, execute the program by running `python app.py` in the terminal.
- Follow the on-screen prompts to navigate through the application.