--Donation Table Procedures
CREATE OR REPLACE PROCEDURE InsertDonation (
    p_Donation_ID INT,
    p_Donor_ID INT,
    p_Donated_BloodType VARCHAR,
    p_Donated_Quantity INT,
    p_Donation_Date DATE,
    p_Recipient_ID INT,
    p_Inventory_ID INT
) AS
BEGIN
    INSERT INTO Donation (Donation_ID, Donor_ID, Donated_BloodType, Donated_Quantity, Donation_Date, Recipient_ID, Inventory_ID)
    VALUES (p_Donation_ID, p_Donor_ID, p_Donated_BloodType, p_Donated_Quantity, p_Donation_Date, p_Recipient_ID, p_Inventory_ID);
END;
/
CREATE OR REPLACE PROCEDURE DeleteDonation (p_Donation_ID INT) AS
BEGIN
    DELETE FROM Donation
    WHERE Donation_ID = p_Donation_ID;
END;
/
CREATE OR REPLACE PROCEDURE UpdateDonation (
    p_Donation_ID INT,
    p_Donated_Quantity INT
) AS
BEGIN
    UPDATE Donation
    SET Donated_Quantity = p_Donated_Quantity
    WHERE Donation_ID = p_Donation_ID;
END;
/

--Transfusion Table Procedures
CREATE OR REPLACE PROCEDURE InsertTransfusion (
    p_Transfusion_ID INT,
    p_Recipient_ID INT,
    p_Requested_BloodType VARCHAR,
    p_Requested_Component VARCHAR,
    p_Requested_Quantity INT,
    p_Request_Date DATE,
    p_Exchange_Type VARCHAR,
    p_Exchange_Donor_ID INT,
    p_Donation_ID INT,
    p_Inventory_ID INT
) AS
BEGIN
    INSERT INTO Transfusion (Transfusion_ID, Recipient_ID, Requested_BloodType, Requested_Component, Requested_Quantity, Request_Date, Exchange_Type, Exchange_Donor_ID, Donation_ID, Inventory_ID)
    VALUES (p_Transfusion_ID, p_Recipient_ID, p_Requested_BloodType, p_Requested_Component, p_Requested_Quantity, p_Request_Date, p_Exchange_Type, p_Exchange_Donor_ID, p_Donation_ID, p_Inventory_ID);
END;
/
CREATE OR REPLACE PROCEDURE DeleteTransfusion (p_Transfusion_ID INT) AS
BEGIN
    DELETE FROM Transfusion
    WHERE Transfusion_ID = p_Transfusion_ID;
END;
/
CREATE OR REPLACE PROCEDURE UpdateTransfusion (
    p_Transfusion_ID INT,
    p_Requested_Quantity INT
) AS
BEGIN
    UPDATE Transfusion
    SET Requested_Quantity = p_Requested_Quantity
    WHERE Transfusion_ID = p_Transfusion_ID;
END;
/


