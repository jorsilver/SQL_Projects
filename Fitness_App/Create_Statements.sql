-- User Table
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(35) NOT NULL UNIQUE,
    password VARCHAR(18) NOT NULL,
    current_program INT,
    first_name VARCHAR(35) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    height DECIMAL(5,2) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    body_fat_percentage DECIMAL(4,2),
    dob DATE NOT NULL,
    gender VARCHAR(35),
    unit_type ENUM('metric', 'imperial') NOT NULL DEFAULT 'metric'
    -- FOREIGN KEY (current_program) REFERENCES Program(program_id) -- FK will be added later due
);

-- Fitness Target Table
CREATE TABLE fitness_target (
    user_id INT PRIMARY KEY,
    weight DECIMAL(5,2),
    body_fat_percentage DECIMAL(4,2),
    daily_caloric_intake INT,
    daily_carb_intake_grams INT,
    daily_protein_intake_grams INT,
    daily_fat_intake_grams INT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Meal Table
CREATE TABLE meal (
    meal_id INT AUTO_INCREMENT PRIMARY KEY,
    creator_id INT NOT NULL, -- user_id
    recipe TEXT NOT NULL,
    serving_size DECIMAL(5,2),
    serving_unit VARCHAR(25),
    calories_per_serving INT,
    carbs_per_serving DECIMAL(5,2),
    protein_per_serving DECIMAL(5,2),
    fat_per_serving DECIMAL(5,2),
    public BOOLEAN not null DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES user(user_id)
);


-- Program Table
CREATE TABLE program (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    creator_id INT NOT NULL, -- user_id
    program_name VARCHAR(35) NOT NULL,
    description TEXT,
    days_per_week INT NOT NULL,
    public BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES user(user_id)
);

-- Daily Log Table
CREATE TABLE daily_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    total_caloric_burn INT,
    total_caloric_intake INT,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Workout Table
CREATE TABLE workout (
    workout_id INT AUTO_INCREMENT PRIMARY KEY,
    workout_name VARCHAR(35) NOT NULL,
    approx_duration_mins INT
);

-- Session Table
CREATE TABLE session (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    log_id INT NOT NULL,
    workout_id INT,
    start_time TIME NOT NULL,
    duration_mins INT,
    cals_burned INT,
    weight_moved DECIMAL(10,2), #see user preference for unit
    notes TEXT,
    FOREIGN KEY (log_id) REFERENCES daily_log(log_id),
    FOREIGN KEY (workout_id) REFERENCES workout(workout_id)
);

-- Exercise Table
CREATE TABLE exercise (
    exercise_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    muscle_group VARCHAR(35) NOT NULL,
    description TEXT,
    MET_value DECIMAL(5,2),
    10_reps_time_secs INT
);

-- Program_Workout Table
CREATE TABLE program_workout (
    program_id INT,
    workout_id INT,
    day_number INT NOT NULL,
    PRIMARY KEY (program_id, workout_id),
    FOREIGN KEY (program_id) REFERENCES program(program_id),
    FOREIGN KEY (workout_id) REFERENCES workout(workout_id)
);

-- Workout_Exercise Table
CREATE TABLE workout_exercise (
    workout_id INT,
    exercise_id INT,
    set_number INT NOT NULL,
    reps INT NOT NULL,
    PRIMARY KEY (workout_id, exercise_id),
    FOREIGN KEY (workout_id) REFERENCES workout(workout_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);

-- Session_Exercise Table
CREATE TABLE session_exercise (
    session_id INT,
    exercise_id INT,
    set_number INT NOT NULL,
    reps INT NOT NULL,
    weight DECIMAL(4,2) NOT NULL, #see corresponding user for unit type
    PRIMARY KEY (session_id, exercise_id),
    FOREIGN KEY (session_id) REFERENCES session(session_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);

-- Daily_Log_Meal Table
CREATE TABLE daily_log_meal (
    log_id INT,
    meal_id INT,
    time TIME NOT NULL,
    servings DECIMAL(5,2),
    PRIMARY KEY (log_id, meal_id),
    FOREIGN KEY (log_id) REFERENCES daily_log(log_id),
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
);

-- Update User table to add foreign key for current_program
ALTER TABLE user
ADD CONSTRAINT user_ibfk_1
FOREIGN KEY (current_program) REFERENCES program(program_id);