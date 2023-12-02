<p float="left">
  <img alt="HTML" src="https://img.shields.io/badge/HTML-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/>
  <img alt="CSS" src="https://img.shields.io/badge/CSS-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/>
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
  <img alt="jQuery" src="https://img.shields.io/badge/jQuery-%230175C2.svg?&style=for-the-badge&logo=jquery&logoColor=white"/>
  <img alt="Bootstrap" src="https://img.shields.io/badge/Bootstrap-%2302569B.svg?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
  <img alt="Apache" src="https://img.shields.io/badge/Apache-%23D42029.svg?&style=for-the-badge&logo=apache&logoColor=white"/>
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-%2300f.svg?&style=for-the-badge&logo=mysql&logoColor=white"/>
  <img alt="Heroku" src="https://img.shields.io/badge/Heroku-%23430098.svg?&style=for-the-badge&logo=heroku&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge"/>
</p>

# Project R: A Blood Donation Website 🩸

This is the final project of our CSE370 course (Database Systems) The idea is, users can register and request for blood donation and donate bloods, and Admin/ Staffs can approve, reject, or confirm their donations. The general purpose of this project is to make the blood donation process easier for everyone, have a database of donation seekers and donors, and last but not the least, keep track of donations. The frontend is built using HTML, CSS, Bootstrap, JavaScript, jQuery the backend using Flask, and the database using MySQL.

## ER Diagram 🔗

<img src="documentation/database/Project R EER.png" alt="drawing"/>

## Schema Diagram 📑

<img src="documentation/database/Project R Schema.png" alt="drawing"/>

## Featuers and Contributions

### Sabbir Bin Abdul Latif (21201200)

    - [x] Dynamic Navbar
    - [x] Dynamic Dashboard
    - [x] Manage Request (Action)
    - [x] User Report
    - [x] Manage Donation (Action)
    - [x] Manage Reports (Action)
    - [x] Add Donation
    - [x] Forget Password

### Sultan Mehedi Masud (22101071)

    - [x] Request Donation
    - [x] Manage Users
    - [x] Manage Reports
    - [x] Manage Donations
    - [x] Manage Requests
    - [x] History
    - [x] Current Requests

### Susmita Biswas (22101380)

    - [x] Registration (Except Diseases)
    - [x] Login
    - [x] Logout
    - [x] Change Password
    - [x] Edit Profile (Except Diseases)
    - [x] Edit User
    - [x] Delete User
    - [x] User Profile

🔗 [Live link of the Application](https://google.com/)

Although, if you want to run the application to your server you can do that too. To set up the Flask web application along with a MySQL database, you can follow these guidelines. I've included steps for setting up the application environment, installing dependencies from the requirements.txt file, and restoring a MySQL database backup. To run this app to your machine just download the repository and follow the steps.

## Setup Documentation 📑

#### Prerequisites

- Python installed on your system.
- MySQL Server installed and running.
- Flask application files on your machine (app.py and others).
- The requirements.txt file.
- A MySQL database backup file (usually .sql format).

#### Step 1: Setting Up a Virtual Environment

It's a good practice to use a virtual environment for Python projects. This isolates your project's dependencies from the system's Python environment.

1. Navigate to the project's app directory in the command line.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

#### Step 2: Installing Dependencies

Install the required packages using the requirements.txt file.

1. Ensure your virtual environment is activated.
2. Run:
   ```
   pip install -r requirements.txt
   ```

#### Step 3: Setting Up MySQL Database

1. Open MySQL command-line client or a GUI tool like MySQL Workbench/ PHP My Admin.
2. Create a new database for the application with name `project_r` in your machine.
3. Restore the backup into this new database. If using the command line:
   ```
   mysql -u [username] -p project_r < project_r_backup.sql
   ```

Replace [username] with your MySQL username, and the path to the backup file, respectively.

#### Step 4: Configuring Your Flask Application

1.  Create a `config.py` at the root folder of the application.
2.  Copy the following code to the file:

    ```
    import os
        class Config:
            DB_USER = os.getenv('DB_USER', 'your_username')
            DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
            DB_HOST = os.getenv('DB_HOST', 'localhost')
            DB_NAME = os.getenv('DB_NAME', 'project_r')
            DB_PORT = os.getenv('DB_PORT', '3306')
            DB_RAISE_ON_WARNINGS = os.getenv('DB_RAISE_ON_WARNINGS', True)
    ```

    Replace [your_username], and [your_password] with your MySQL username respectively.

#### Step 5: Running The Flask Application

1. In the command line, navigate to your project's directory.
2. Set the environment variable FLASK_APP to your main application file (usually app.py):

- On Windows:
  ```
  set FLASK_APP=app.py
  ```
- On macOS/Linux:
  ```
  export FLASK_APP=app.py
  ```

3. Run the Flask app:
   ```
   flask run
   ```

#### Step 6: Accessing the Application

- Open a web browser and navigate to http://127.0.0.1:5000 (or the URL provided in the terminal).

##### Additional Notes

- Always ensure your virtual environment is activated when working on the project.
- If you encounter any errors during the setup, check the error messages for guidance and ensure all prerequisites are met.

## Contributors ✨

Thanks goes to these wonderful people

<table>
  <tr>
    <td align="center"><a href="https://sabbir.co"><img src="app/static/images/team/Sabbir Bin Abdul Latif.jpeg" width="100px;" alt=""/>
    <br />
    <sub><b>Sabbir Bin Abdul Latif</b></sub></a>
    </td>
    <td align="center"><a href="#"><img src="app/static/images/team/Sultan Mehedi Masud.jpeg" width="100px;" alt=""/>
    <br />
    <sub><b>Sultan Mehedi Masud</b></sub></a>
    </td>
    <td align="center"><a href="#"><img src="app/static/images/team/Susmita Biswas.jpeg" width="100px;" alt=""/>
    <br />
    <sub><b>Susmita Biswas</b></sub></a>
    </td>
  </tr>
</table>

## Licenses 📃

[MIT](LICENSE)
