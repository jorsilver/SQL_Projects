CREATE TABLE users(
    userID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    ActType ENUM('Rider', 'Driver') NOT NULL
);

CREATE TABLE cars(
    VIN VARCHAR(17) NOT NULL PRIMARY KEY,
    OwnerID INT NOT NULL,
    PlateNum VARCHAR(10) NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    Available BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (OwnerID) REFERENCES users(userID)
);

CREATE TABLE rides(
    RideID INT AUTO_INCREMENT PRIMARY KEY,
    RiderID INT NOT NULL,
    DriverID INT,
    VIN VARCHAR(17),
    ReqTime TIMESTAMP NOT NULL DEFAULT NOW(),
    DriverRtg DECIMAL(3, 2),
    RiderRtg DECIMAL(3, 2),
    PickUpAdr VARCHAR(255),
    DropOffAdr VARCHAR(255),
    FOREIGN KEY (RiderID) REFERENCES users(userID),
    FOREIGN KEY (DriverID) REFERENCES users(userID),
    FOREIGN KEY (VIN) REFERENCES cars(VIN)
);

DELIMITER $$
CREATE PROCEDURE switch_cars(IN driverID INT, IN newVIN VARCHAR(17))
BEGIN
    UPDATE cars
    SET Available =
        CASE
            WHEN VIN != newVIN THEN 0
            WHEN VIN = newVIN THEN 1
        END
    WHERE OwnerID = driverID;
END $$

DELIMITER $$
CREATE TRIGGER update_arrival_Time
    AFTER UPDATE ON cars
    FOR EACH ROW
BEGIN
    IF NEW.Available = 1 THEN
        UPDATE rides
        SET arvlTime = NOW()
        WHERE Vin = NEW.VIN AND arvlTime IS NULL;
    END IF;
END $$