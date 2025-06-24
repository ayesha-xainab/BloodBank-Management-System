--Expiry Date Trigger
CREATE OR REPLACE TRIGGER CheckBloodExpiry
BEFORE INSERT OR UPDATE ON BloodInventory
FOR EACH ROW
BEGIN
    IF :NEW.Expiry_Date < SYSDATE THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot insert or update. Blood is expired.');
    END IF;
END;
/

--Blood Quantity Trigger
CREATE OR REPLACE TRIGGER MonitorBloodQuantity
AFTER UPDATE ON BloodInventory
FOR EACH ROW
BEGIN
    IF :NEW.Quantity < 10 THEN
        DBMS_OUTPUT.PUT_LINE('Warning: Blood quantity is below the threshold.');
    END IF;
END;
/

--Check Last Donation Date should be more than 3 months
CREATE OR REPLACE TRIGGER check_donation_interval
BEFORE INSERT OR UPDATE ON Donation
FOR EACH ROW
DECLARE
    last_donation_date DATE;
BEGIN
    SELECT MAX(donation_date)
    INTO last_donation_date
    FROM Donation
    WHERE donor_id = :NEW.donor_id;

    IF last_donation_date IS NOT NULL AND last_donation_date > ADD_MONTHS(SYSDATE, -3) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Donor is not eligible to donate again within 3 months.');
    END IF;
END;
/

--Donor Medical Eligibility Trigger
CREATE OR REPLACE TRIGGER check_donor_eligibility
BEFORE INSERT OR UPDATE ON Donation
FOR EACH ROW
DECLARE
    eligibility_status VARCHAR2(20);
BEGIN
    SELECT eligibility_status
    INTO eligibility_status
    FROM Donor
    WHERE donor_id = :NEW.donor_id;

    IF eligibility_status != 'Eligible' THEN
        RAISE_APPLICATION_ERROR(-20002, 'The donor is not eligible for donation.');
    END IF;
END;
/

--Check Blood Types are compatible
CREATE OR REPLACE TRIGGER check_transfusion_blood_type
BEFORE INSERT OR UPDATE ON Transfusion
FOR EACH ROW
DECLARE
    donation_blood_type VARCHAR2(5);
    recipient_blood_type VARCHAR2(5);
BEGIN
    SELECT donated_bloodtype
    INTO donation_blood_type
    FROM Donation
    WHERE donation_id = :NEW.donation_id;

    SELECT recipient_bloodtype
    INTO recipient_blood_type
    FROM Recipient
    WHERE recipient_id = :NEW.recipient_id;

    IF donation_blood_type != recipient_blood_type THEN
        RAISE_APPLICATION_ERROR(-20004, 'The blood type of the donation and recipient must be the same.');
    END IF;
END;
/

--Validation of Medical Requirements of Donor
CREATE OR REPLACE TRIGGER validate_donor_eligibility
BEFORE INSERT OR UPDATE ON Donor
FOR EACH ROW
DECLARE
    positive_test_count NUMBER;
BEGIN
    -- Check if there are any positive test results for the donor
    SELECT COUNT(*)
    INTO positive_test_count
    FROM DonorScreening
    WHERE Donor_ID = :NEW.Donor_ID
      AND (
          UPPER(HIV_Test) = 'P' OR 
          UPPER(Hepatitis_Test) = 'P' OR 
          UPPER(Syphilis_Test) = 'P' OR 
          UPPER(Malaria_Test) = 'P'
      );

    -- If there is any positive test result, eligibility cannot be "Eligible"
    IF positive_test_count > 0 AND UPPER(:NEW.Eligibility_Status) = 'ELIGIBLE' THEN
        RAISE_APPLICATION_ERROR(-20005, 'Eligibility cannot be set to "Eligible" because one or more tests are positive in Donor Screening.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER validate_donor_screening
AFTER INSERT OR UPDATE ON DonorScreening
FOR EACH ROW
DECLARE
    donor_age INT;
BEGIN
    SELECT Donor_Age INTO donor_age 
    FROM Donor 
    WHERE Donor_ID = :NEW.Donor_ID;

    -- Check the HB levels Weight and Age of Donor
    IF :NEW.HB_Level < 13 OR :NEW.Weight < 50 OR donor_age > 50 THEN
        -- Update eligibility status to 'Not Eligible' if conditions fail
        UPDATE Donor
        SET Eligibility_Status = 'Not Eligible'
        WHERE Donor_ID = :NEW.Donor_ID;

        RAISE_APPLICATION_ERROR(-20006, 'Donor cannot be marked as Eligible due to failing screening conditions.');
    END IF;
END;
/




