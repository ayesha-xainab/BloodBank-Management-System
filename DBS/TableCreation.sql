-- DONOR TABLE
CREATE TABLE Donor (
    Donor_ID INT PRIMARY KEY,
    Donor_Name VARCHAR(100) NOT NULL,
    Donor_NICnumber VARCHAR(15) NOT NULL,
    Donor_Age INT,
    Donor_Gender CHAR(1),
    Donor_BloodType VARCHAR(3) NOT NULL,
    Donor_Contact VARCHAR(15),
    Eligibility_Status VARCHAR(10)
);

-- RECIPIENT TABLE
CREATE TABLE Recipient (
    Recipient_ID INT PRIMARY KEY,
    Recipient_Name VARCHAR(100) NOT NULL,
    Recipient_NICnumber VARCHAR(15) NOT NULL,
    Recipient_Age INT,
    Recipient_Gender CHAR(1),
    Recipient_BloodType VARCHAR(3) NOT NULL,
    Recipient_Contact VARCHAR(15)
);

-- STAFF TABLE
CREATE TABLE Staff (
    Staff_ID INT PRIMARY KEY,
    Staff_Name VARCHAR(100) NOT NULL,
    Staff_Role VARCHAR(50),
    Staff_Contact VARCHAR(15)
);

-- DONORSCREENING TABLE
CREATE TABLE DonorScreening (
    Donor_ID INT,
    Last_DonationDate DATE,
    HB_Level DECIMAL(5, 2),
    Weight DECIMAL(5, 2),
    HIV_Test VARCHAR(1),
    Hepatitis_Test VARCHAR(1),
    Syphilis_Test VARCHAR(1),
    Malaria_Test VARCHAR(1)
);

-- DONATION TABLE
CREATE TABLE Donation (
    Donation_ID INT PRIMARY KEY,
    Donor_ID INT NOT NULL,
    Donated_BloodType VARCHAR(3) NOT NULL,
    Donated_Quantity INT,
    Donation_Date DATE NOT NULL,
    Recipient_ID INT,
    Inventory_ID INT
);

-- BLOODINVENTORY TABLE
CREATE TABLE BloodInventory (
    Inventory_ID INT PRIMARY KEY,
    Blood_Type VARCHAR(3) NOT NULL,
    Blood_Component VARCHAR(50) NOT NULL,
    Quantity INT NOT NULL,
    Temperature DECIMAL(5, 2),
    Expiry_Date DATE NOT NULL,
    Donation_ID INT NOT NULL
);

-- EXPIREDBLOOD TABLE
CREATE TABLE ExpiredBlood (
    Expired_Log_ID INT PRIMARY KEY,
    Inventory_ID INT NOT NULL,
    Expired_BloodType VARCHAR(3) NOT NULL,
    Expired_BloodComponent VARCHAR(50) NOT NULL,
    Disposal_Date DATE NOT NULL,
    Staff_ID INT NOT NULL,
    Remarks VARCHAR(100)
);

-- TRANSFUSION TABLE
CREATE TABLE Transfusion (
    Transfusion_ID INT PRIMARY KEY,
    Recipient_ID INT NOT NULL,
    Requested_BloodType VARCHAR(3) NOT NULL,
    Requested_Component VARCHAR(50) NOT NULL,
    Requested_Quantity INT NOT NULL,
    Request_Date DATE NOT NULL,
    Exchange_Type VARCHAR(50),
    Exchange_Donor_ID INT,
    Donation_ID INT,
    Inventory_ID INT
);

-- DONORSCREENING FOREIGN KEY
ALTER TABLE DonorScreening 
ADD CONSTRAINT FK_DonorScreening_Donor
FOREIGN KEY (Donor_ID) REFERENCES Donor(Donor_ID);

-- DONATION FOREIGN KEYS
ALTER TABLE Donation 
ADD CONSTRAINT FK_Donation_Donor
FOREIGN KEY (Donor_ID) REFERENCES Donor(Donor_ID)
ALTER TABLE Donation
ADD CONSTRAINT FK_Donation_Recipient
FOREIGN KEY (Recipient_ID) REFERENCES Recipient(Recipient_ID)
ALTER TABLE Donation
ADD CONSTRAINT FK_Donation_Inventory
FOREIGN KEY (Inventory_ID) REFERENCES BloodInventory(Inventory_ID)

-- BLOODINVENTORY FOREIGN KEY
ALTER TABLE BloodInventory 
ADD CONSTRAINT FK_BloodInventory_Donation
FOREIGN KEY (Donation_ID) REFERENCES Donation(Donation_ID)

-- EXPIREDBLOOD FOREIGN KEYS
ALTER TABLE ExpiredBlood 
ADD CONSTRAINT FK_ExpiredBlood_Inventory
FOREIGN KEY (Inventory_ID) REFERENCES BloodInventory(Inventory_ID)
ALTER TABLE ExpiredBlood
ADD CONSTRAINT FK_ExpiredBlood_Staff
FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)

-- TRANSFUSION FOREIGN KEYS
ALTER TABLE Transfusion 
ADD CONSTRAINT FK_Transfusion_Recipient
FOREIGN KEY (Recipient_ID) REFERENCES Recipient(Recipient_ID)
ALTER TABLE Transfusion 
ADD CONSTRAINT FK_Transfusion_Donor
FOREIGN KEY (Exchange_Donor_ID) REFERENCES Donor(Donor_ID)
ALTER TABLE Transfusion 
ADD CONSTRAINT FK_Transfusion_Donation
FOREIGN KEY (Donation_ID) REFERENCES Donation(Donation_ID)
ALTER TABLE Transfusion 
ADD CONSTRAINT FK_Transfusion_Inventory
FOREIGN KEY (Inventory_ID) REFERENCES BloodInventory(Inventory_ID)


ALTER TABLE Donor
MODIFY Donor_Gender VARCHAR2(10);

ALTER TABLE Recipient
MODIFY Recipient_Gender VARCHAR2(10);

ALTER TABLE Donor
MODIFY Eligibility_Status VARCHAR2(20);
