# Blood Bank Management System

A comprehensive *Blood Bank Management System* built as a database project with a minimalistic Python-based user interface. The application ensures efficient management of donor, recipient, and blood inventory data while offering role-based access to admin, staff, donors, and recipients.

The backend utilizes Oracle SQL for robust and reliable data storage, leveraging advanced database features such as triggers, procedures, and primary operations.


## Introduction

This project simulates a Blood Bank system catering to a hospital's needs. It keeps track of:

* Donors, their medical history, and donation records.
* Recipients and their transfusion records.
* Blood inventory, including donations and expired blood.
* Staff details and their access levels.

The system provides secure, role-based access:

* **Admin**: Full access to all records. Admins can add, edit, or delete records after logging in with a password.
* **Staff**: Limited access to add medical records.
* **Donor/Recipient**: View-only access to their respective records by entering their ID.

The application is designed to streamline daily blood bank operations and ensure data integrity.

## Project Overview 

Here is the Entity Relationship Diagram of the Blood Bank Management System.

![Entity Relationship Diagram](ERD.png)


## Features

* **Role-Based Access**:
  Secure login with role-specific permissions.
* **Data Management**:
  * Add, edit, and delete donor and recipient records.
  * Maintain blood inventory and medical history.
  * Store information on expired blood.
* **Daily Reports**:
  Automatically generates daily transaction and inventory report.
* **Database Operations**:
  * Advanced use of triggers for rule-based data insertion.
  * Frequently accessed tables have pre-defined procedures for efficient operation.
* **Minimalistic User Interface**: Simple and intuitive navigation.


## Technologies Used

* **Frontend**: Python (Tkinter for GUI)
* **Backend Database**: Oracle SQL


## Setup and Installation

1. Clone this repository.
2. Install required Python libraries.
3. Configure Oracle Database by importing the SQL script.
4. Update the database connection in the Python application.
5. Run the application.


## Screenshots

<div style="display: flex; gap: 25px;">
  <img src="./Screenshots/Home%20Tab.png" alt="Home Tab" width="400"/>
  <img src="./Screenshots/Role%20based%20view.png" alt="Donor ID Access" width="400"/>
  <img src="./Screenshots/Record%20View.png" alt="Record View" width="400"/>
  <img src="./Screenshots/Admin%20Tab.png" alt="Admin Tab" width="400"/>
  <img src="./Screenshots/Admin%20Authentication.png" alt="Admin Authentication" width="400"/>
  <img src="./Screenshots/Admin%20Panel.png" alt="Admin Panel" width="400"/>
  <img src="./Screenshots/Insertion%20form.png" alt="Insertion Form" width="400"/>
  <img src="./Screenshots/Triggered%20an%20event.png" alt="Event Trigger" width="400"/>
  <img src="./Screenshots/Updation%20Window.png" alt="Updation Window" width="400"/>
  <img src="./Screenshots/Performing%20Updation.png" alt="Update" width="400"/>
  <img src="./Screenshots/Successful%20Update%20Alert.png" alt="Update Successful" width="400"/>
  <img src="./Screenshots/Table%20View%20with%20modification%20options.png" alt="Table View" width="400"/>
  <img src="./Screenshots/Staff%20Login.png" alt="Staff Login" width="400"/>
  <img src="./Screenshots/Staff%20View%20restricted.png" alt="Staff View" width="400"/>
</div>


## Future Improvements

We aim to improve our system by adding some features:

* *Notification alerts*:
  Add a notification system for low stock alerts.
* *AI enhancements*:
  Integrate machine learning for donor recommendation.
* *System Expansion*:
  Develop a web-based version for remote access.
* *Data Visualization*:
  Include graphical representations of stock and donor statistics.


## Contribution

This application was developed as a semester project for our Database Systems course and is the result of a collaborative effort between my friend and me. We are working on improvements and welcome any contributions from your side.



