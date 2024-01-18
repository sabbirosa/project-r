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

## EER Diagram 🔗

<img src="documentation/database/Project R EER.png" alt="EER Diagram"/>

## Schema Diagram 📑

<img src="documentation/database/Project R Schema.png" alt="Schema Diagram"/>

## Featuers 🔍

**Dynamic Navbar:** The navbar on the site changes based on the user role and session status. If a donor is logged in the navbar changes according to donor features. And if an admin logged in navbar contains some more menu items like manage donations, manage requests, etc. Also, a drop-down menu with the user’s first name appears after a successful login.

**Registration:** Users can register on this platform with basic information. Initially, a registered user will be a donor. A super admin will be added to the database with command line operation. After that, the admin can change the role of other registered users and can assign them as an admin or staff. During registration, the process will go through some validations like if the email or phone number is already registered in the platform, if the password is strong, etc. The password entered by the user will be converted and stored as a hashed password to the database.

**Login:** Users can log in to the dashboard with their registered email and password. If the email and password are matched they will have access to the dashboard. During the login process, the stored hashed password will be converted again into normal form and checked. If the user is banned they will be unable to login.

**Logout:** By clicking the logout button the user will be logged out.

**Forget Password:** If the user forgets the password they can verify their information with their email, phone number, and date of birth. If all the details are correct then they will be redirected to the reset password page where they can change their password.

**Dashboard:** After login users will be redirected here. If the user is an admin/staff they will see total users, total pending donations, total requests, and total reports here. All the cards are clickable. So if the admin/staff click on the card they will be redirected to the respective pages. And then all the requests based on some criteria will be visible here.
The criteria are, if the user is 18+, hasn’t donated blood in the last 3 months, hasn’t any blood diseases, and matches the requested blood group. Failing one of these criteria will be the reason for not showing any blood requests to the dashboard. And user’s requests will be not shown on the dashboard either.
And this section is for all the users (admin, staff, donors).

**Request Donation:** Users can request blood donations here with contact information, hospital, and location.

**Add Donation:** On this page, users can add their donation information. If they accept a request from the dashboard some fields that match with the request will be automatically filled and the user will have to add the donation date and proof of donation.

**Change Password:**
Users can change the password. For that, they will have to enter their current password and new password. If the current password is correct then they can only change the password.

**Edit Profile:** Users can edit their profile information. The page with a form will be initially filled with the existing information of the user. Here they can change their information.

**User Profile:** All of the user’s information will be visible here along with their user ID. And a button to redirect to the edit user page.

**History:** All the donations and requests of donation history of the users will be shown here with the updated status.

**Report User:** A user can report a user based on any anomaly. If the user knows the violator’s id they can add the violator’s id. But if not they can report that with proper proof and explanation. They can report anything suspicious on the website too.

**Current Requests:** On this page all the pending requests by the user will be listed. If the request is completed then the user can complete the request by clicking the action button.

**Manage Users:** This is an admin/staff-accessible only page. All the users will be listed here and a staff or admin can search them by their name, edit them, and delete them.

- **Edit User:** This is an admin/staff-accessible-only feature. An admin/staff can change the information of the users. They can ban or unban a user. Although staff can’t change the details of an admin.

- **Delete User:** This is an admin/staff-accessible-only feature. An admin/staff can perform this operation. By clicking the user delete button a user will be entirely deleted with their existing records to the other tables. But the staff can’t delete an admin.

**Manage Donations:** This is an admin/staff-accessible only page. All the fulfilled donations by the users will be listed here. After verifying the proof document admin/staff will take action about the donation. And all the completed donations will be still there with a view button. By clicking the button admin/staff will be able to see the details of the donation.

- **Manage Donation (Action):** This is an admin/staff-accessible only feature. On the manage_donations page, each of the pending donations will have two buttons. If the donation is verified and if it is fulfilled through the website's blood request then the blood request will be marked as completed, and the user's last donation date will be updated to the donated date. Otherwise, only the last donation date of the user will be updated [user may donate blood outside of the platform]. And if the donation is rejected and was processed by the website the request will be again set to incomplete and it will reappear on the dashboard. And user's last donation date will be the previous donated date in the user's table if any. If not it will be set to null. Also, the admin/staff’s donation will be approved automatically.

**Manage Requests:** This is an admin/staff-accessible only page. All the requests by the user will be visible here. If the donation is fulfilled admin/staff can change the status from here.

- **Manage Request (Action):** Admin/staff can complete the donation request by clicking the done button of each of the requests.

**Manage Reports:** This is an admin/staff-accessible only page. All the pending reports by the users will be listed here. If a user reports another user with violator_user_id then after checking, admin/staff can directly ban the violator with the ban button. But if the violator’s ID is not available then the admin/staff will look into the matter and will ban the violator from the manage_users page manually and after that, they will mark the report as resolved. And all the completed reports will be still there with a view button. By clicking the button admin/staff will be able to see the details of the report.

- **Manage Reports (Action):** This is an admin/staff-accessible only feature. Based on the type of reports, admin/staff will be able to take action. If a violator ID is given, the admin/staff can ban the violator directly. But if the violator ID is not available then the the admin/staff will look into the matter and will ban the violator from the manage_users page manually and after that, they will mark the report as resolved.

## Contributions 🧑🏻‍💻

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

🔗 [Live link of the Application](https://project-r.sabbir.co/)

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

Replace [username] with your MySQL username, and the path to the backup file, respectively. If you getting problem doing this you may also use SQL queries to create table of `documentation/database/schema.sql` to add the databse in your profile.

#### Step 4: Configuring Your Flask Application

1.  Create a `config.py` at the root folder of the application.
2.  Copy the following code to the file:

    ```python
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
- Register as a new user. Then make the user admin with the following queries:

```SQL
UPDATE users SET user_type = 'Admin' WHERE user_id = 1;
INSERT INTO staff (user_id, role) VALUES (1, 'Admin');
```

Now the first user is set as an admin and you are ready to explore the website.

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

## [Licenses](LICENSE) 📃
