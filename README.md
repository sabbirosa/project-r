# project-r

## Featuers and Contributions

### Sabbir Bin Abdul Latif (21201200)

    - Dynamic Navbar
    - Dashboard
    - Manage Requests (Handle)
    - User Report
    - Manage Donations (Handle)
    - Manage Reports (Handle)
    - Add Donation
    - Forget Password

### Sultan Mehedi Masud (22101071)

    - Request Donation
    - Manage Users
    - Manage Reports
    - Manage Donations
    - Manage Requests
    - History
    - Current Requests

### Susmita Biswas (22101380)

    - Registration (Except Diseases)
    - Login
    - Logout
    - Change Password
    - Edit Profile (Except Diseases)
    - Edit User
    - Delete User
    - User Profile

### Project Feature
Dynamic Navbar: The navbar on the site changes based on the user role and session status. If a donor is logged in the navbar changes according to donor features. And if an admin logged in navbar contains some more menu items like manage donations, manage requests, etc. Also, a drop-down menu with the user’s first name appears after a successful login.
Registration: Users can register on this platform with basic information. Initially, a registered user will be a donor. A super admin will be added to the database with command line operation. After that, the admin can change the role of other registered users and can assign them as an admin or staff. During registration, the process will go through some validations like if the email or phone number is already registered in the platform, if the password is strong, etc. The password entered by the user will be converted and stored as a hashed password to the database.
Login: Users can log in to the dashboard with their registered email and password. If the email and password are matched they will have access to the dashboard. During the login process, the stored hashed password will be converted again into normal form and checked. If the user is banned they will be unable to login.
Logout: By clicking the logout button the user will be logged out.
Forget Password: If the user forgets the password they can verify their information with their email, phone number, and date of birth. If all the details are correct then they will be redirected to the reset password page where they can change their password.
Dashboard: After login users will be redirected here. If the user is an admin/staff they will see total users, total pending donations, total requests, and total reports here. All the cards are clickable. So if the admin/staff click on the card they will be redirected to the respective pages. And then all the requests based on some criteria will be visible here. 
The criteria are, if the user is 18+, hasn’t donated blood in the last 3 months, hasn’t any blood diseases, and matches the requested blood group. Failing one of these criteria will be the reason for not showing any blood requests to the dashboard. And user’s requests will be not shown on the dashboard either.
And this section is for all the users (admin, staff, donors).
Request Donation: Users can request blood donations here with contact information, hospital, and location. 
Add Donation: On this page, users can add their donation information. If they accept a request from the dashboard some fields that match with the request will be automatically filled and the user will have to add the donation date and proof of donation.
Change Password: Users can change the password. For that, they will have to enter their current password and new password. If the current password is correct then they can only change the password.
Edit Profile: Users can edit their profile information. The page with a form will be initially filled with the existing information of the user. Here they can change their information.
User Profile: All of the user’s information will be visible here along with their user ID. And a button to redirect to the edit user page.
History: All the donations and requests of donation history of the users will be shown here with the updated status.
Report User: A user can report a user based on any anomaly. If the user knows the violator’s id they can add the violator’s id. But if not they can report that with proper proof and explanation. They can report anything suspicious on the website too.
Current Requests: On this page all the pending requests by the user will be listed. If the request is completed then the user can complete the request by clicking the action button.
Manage Users: This is an admin/staff-accessible only page. All the users will be listed here and a staff or admin can search them by their name, edit them, and delete them.
Edit User: This is an admin/staff-accessible-only feature. An admin/staff can change the information of the users. They can ban or unban a user. Although staff can’t change the details of an admin.
Delete User: This is an admin/staff-accessible-only feature. An admin/staff can perform this operation. By clicking the user delete button a user will be entirely deleted with their existing records to the other tables. But the staff can’t delete an admin.
Manage Donations: This is an admin/staff-accessible only page. All the fulfilled donations by the users will be listed here. After verifying the proof document admin/staff will take action about the donation. And all the completed donations will be still there with a view button. By clicking the button admin/staff will be able to see the details of the donation.
Manage Donation (Action): This is an admin/staff-accessible only feature. On the manage_donations page, each of the pending donations will have two buttons. If the donation is verified and if it is fulfilled through the website's blood request then the blood request will be marked as completed, and the user's last donation date will be updated to the donated date. Otherwise, only the last donation date of the user will be updated [user may donate blood outside of the platform]. And if the donation is rejected and was processed by the website the request will be again set to incomplete and it will reappear on the dashboard. And user's last donation date will be the previous donated date in the user's table if any. If not it will be set to null. Also, the admin/staff’s donation will be approved automatically. 
Manage Requests: This is an admin/staff-accessible only page. All the requests by the user will be visible here. If the donation is fulfilled admin/staff can change the status from here.
Manage Request (Action): Admin/staff can complete the donation request by clicking the done button of each of the requests.
Manage Reports: This is an admin/staff-accessible only page. All the pending reports by the users will be listed here. If a user reports another user with violator_user_id then after checking, admin/staff can directly ban the violator with the ban button. But if the violator’s ID is not available then the admin/staff will look into the matter and will ban the violator from the manage_users page manually and after that, they will mark the report as resolved. And all the completed reports will be still there with a view button. By clicking the button admin/staff will be able to see the details of the report.
Manage Reports (Action): This is an admin/staff-accessible only feature. Based on the type of reports, admin/staff will be able to take action. If a violator ID is given, the admin/staff can ban the violator directly. But if the violator ID is not available then the the admin/staff will look into the matter and will ban the violator from the manage_users page manually and after that, they will mark the report as resolved.

