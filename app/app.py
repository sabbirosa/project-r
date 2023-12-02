from datetime import datetime, timedelta

from config import Config
from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from helpers import is_strong_password, save_file
from mysql.connector import connect
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = '\x99\xc9\x8d@\xb9\xc4t\xdbw\x16C\x03\xb3\xbe\x12g\x829X\x1d\x9fQ\xcb\x12'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_config = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'host': Config.DB_HOST,
    'database': Config.DB_NAME,
    'port': Config.DB_PORT,
    'raise_on_warnings': Config.DB_RAISE_ON_WARNINGS
}

def get_db_connection():
    return connect(**db_config)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


def get_user_by_id(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()
    db.close()

    if user_data:
        user = User()
        user.id = user_data['user_id']
        user.email = user_data['email']
        user.user_type = user_data['user_type']
        user.name = user_data['first_name'] + ' ' + user_data['last_name']
        return user

    return None


class User(UserMixin):
    pass


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about_us():
    return render_template('about_us.html')


@app.route('/contact')
def contact_us():
    return render_template('contact_us.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = {
            'first_name': request.form.get("first_name"), 'last_name': request.form.get("last_name"), 'dob': request.form.get("dob"), 'gender': request.form.get("gender"), 'email': request.form.get("email"), 'phone': request.form.get("phone"), 'password': request.form.get("password"), 'confirmation': request.form.get("confirmation"), 'blood_group': request.form.get("blood_group"), 'location': request.form.get("location"),
        }

        if not is_strong_password(form_data['password']):
            flash("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character", "warning")
            return render_template("registration.html", form=form_data)

        required_fields = ["first_name", "last_name", "dob", "gender", "email",
                           "phone", "password", "confirmation", "blood_group", "location"]

        if not all(form_data[field] for field in required_fields):
            flash("All required fields must be filled", "warning")
            return render_template("registration.html", form=form_data)

        if form_data['password'] != form_data['confirmation']:
            flash("Passwords do not match", "warning")
            return render_template("registration.html", form=form_data)

        hashed_password = generate_password_hash(form_data['password'])

        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM users WHERE phone_number = %s OR email = %s", (form_data['phone'], form_data['email']))

        if cursor.fetchone():
            flash("Phone or email already exists", "warning")
            return render_template("registration.html", form=form_data)

        cursor.execute("INSERT INTO users (first_name, last_name, date_of_birth, gender, email, phone_number, password, blood_group, location, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (form_data['first_name'], form_data['last_name'], form_data['dob'], form_data['gender'], form_data['email'], form_data['phone'], hashed_password, form_data['blood_group'], form_data['location'], 'Donor'))
        db.commit()
        
        user_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO donors (user_id, last_donation_date) VALUES (%s, NULL)", (cursor.lastrowid,))
        db.commit()
        
        blood_diseases = []

        for key in request.form:
            if key.startswith('blood_diseases_'):
                value = request.form[key].strip()
                if value and value != 'None':
                    blood_diseases.append(value)

        for disease in blood_diseases:
            cursor.execute("SELECT disease_id FROM diseases WHERE disease_name = %s", (disease,))
            disease_record = cursor.fetchone()

            if disease_record:
                disease_id = disease_record[0]
            else:
                cursor.execute("INSERT INTO diseases (disease_name) VALUES (%s)", (disease,))
                db.commit()
                disease_id = cursor.lastrowid
            
            cursor.execute("INSERT INTO user_diseases (user_id, disease_id) VALUES (%s, %s)", (user_id, disease_id))
            db.commit()
        
        db.close()
        
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template("registration.html", form=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        db.close()

        if user_data and check_password_hash(user_data['password'], password):
            
            if user_data['status'] == 'Banned':
                flash("Your account has been banned.", "danger")
                return render_template("login.html")
            
            user = User()
            user.id = user_data['user_id']
            user.email = user_data['email']
            user.user_type = user_data['user_type']
            user.first_name = user_data['first_name']

            login_user(user, remember=remember_me)

            session['user_first_name'] = user.first_name
            session['user_role'] = user.user_type

            return redirect(url_for('dashboard'))
        
        else:
            flash("Invalid email and/or password", "warning")

    return render_template('login.html')


@app.route('/logout')
def logout():
    
    session.clear()
    
    return redirect(url_for('index'))


@app.route("/user/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not current_password or not new_password or not confirmation:
            flash("All fields are required", "warning")
            return render_template("change_password.html")

        if new_password != confirmation:
            flash("Passwords do not match", "warning")
            return render_template("change_password.html")

        if not is_strong_password(new_password):
            flash("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character", "warning")
            return render_template("change_password.html")

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE user_id = %s", (current_user.id,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], current_password):
            hashed_password = generate_password_hash(new_password)

            update_query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(update_query, (hashed_password, current_user.id))
            db.commit()

            flash("Password changed successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid password", "warning")

        db.close()
        
    return render_template("change_password.html")


@app.route("/request_donation", methods=["GET", "POST"])
@login_required
def request_donation():
    
    if request.method == "GET":
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (current_user.id,))
        user_data = cursor.fetchone()
        
        return render_template("request_donation.html", form={}, user_data=user_data)
    
    if request.method == "POST":
        form_data = {
            'name': request.form.get("name"),
            'phone': request.form.get("phone"),
            'hospital_name': request.form.get("hospital_name"),
            'blood_group': request.form.get("blood_group"),
            'location': request.form.get("location"),
            'need_by_date': request.form.get("need_by_date"),
            'reason': request.form.get("reason"),
            'urgency_level': request.form.get("urgency_level")
        }

        required_fields = ["name", "phone", "hospital_name", "blood_group", "location", "reason", "need_by_date", "urgency_level"]
        if not all(form_data[field] for field in required_fields):
            flash("All required fields must be filled", "warning")
            return render_template("request_donation.html", form=form_data)

        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("INSERT INTO blood_requests (user_id, requested_blood_group, request_date, location, reason, is_fulfilled, contact_information, hospital_name, need_by_date, urgency_level, name) VALUES (%s, %s, DATE(%s), %s, %s, %s, %s, %s, %s, %s, %s)", (current_user.id, form_data['blood_group'], datetime.now(), form_data['location'], form_data['reason'], 0, form_data['phone'], form_data['hospital_name'], form_data['need_by_date'], form_data['urgency_level'], form_data['name']))
        
        db.commit()

        flash("Request submitted successfully!", "success")
        return redirect(url_for('dashboard'))


@app.route('/admin/manage_users')
@login_required
def manage_users():
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    db.close()

    return render_template('manage_users.html', users=users)


@app.route('/admin/manage_requests')
@login_required
def manage_requests():
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM blood_requests ORDER BY is_fulfilled ASC")
    blood_requests = cursor.fetchall()
    print(blood_requests)
    db.close()

    return render_template('manage_requests.html', requests=blood_requests)


@app.route('/admin/manage_requests/<int:request_id>/<action>')
@login_required
def handle_request_action(request_id, action):
    
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)
        
    print(request_id, action)
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM blood_requests WHERE request_id = %s", (request_id,))
    blood_request = cursor.fetchone()

    if action == 'fulfill':
        cursor.execute("UPDATE blood_requests SET is_fulfilled = TRUE WHERE request_id = %s", (request_id,))
        db.commit()
        
        cursor.execute("UPDATE donations SET donated_date = %s WHERE donation_id = %s", (datetime.now().date(), blood_request['user_id']))
        db.commit()
        
    db.close()
    
    return redirect(url_for('manage_requests'))


@app.route('/dashboard')
@login_required
def dashboard():
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
            
    if current_user.user_type not in ['Donor', 'Admin', 'Staff']:
        abort(403)
        
    if current_user.user_type in ['Donor', 'Staff', 'Admin']:
        cursor.execute("SELECT blood_group FROM users WHERE user_id = %s", (current_user.id,))
        donor_info = cursor.fetchone()

        if not donor_info:
            flash("Donor information not found.", "danger")
            return redirect(url_for('index'))

        donor_blood_group = donor_info['blood_group']

        cursor.execute("SELECT * FROM blood_requests WHERE requested_blood_group = %s AND is_fulfilled = FALSE AND user_id != %s ", (donor_blood_group, current_user.id))
        matching_requests = cursor.fetchall()
        
        cursor.execute("SELECT donated_date FROM donations WHERE donor_id = %s AND status = 'Processed' ORDER BY donated_date DESC LIMIT 1", (current_user.id,))
        last_donation_date = cursor.fetchone()
        last_donated = (last_donation_date and (datetime.now().date() - last_donation_date['donated_date']).days) if last_donation_date else 90
        
        cursor.execute("SELECT disease_id FROM user_diseases WHERE user_id = %s", (current_user.id,))
        diseases = cursor.fetchall()
        
        cursor.execute("SELECT date_of_birth FROM users WHERE user_id = %s", (current_user.id,))
        date_of_birth = cursor.fetchone()
        age = datetime.now().year - date_of_birth['date_of_birth'].year
        
        if diseases or last_donated < 90 or age < 18:
            matching_requests = []
        
        db.close()

    if current_user.user_type in ['Admin', 'Staff']:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_users FROM Users")
        total_users = cursor.fetchone()['total_users']

        cursor.execute("SELECT COUNT(*) AS pending_donations FROM Donations WHERE status = 'Unprocessed'")
        pending_donations = cursor.fetchone()['pending_donations']

        cursor.execute("SELECT COUNT(*) AS pending_requests FROM blood_requests WHERE is_fulfilled = FALSE")
        pending_requests = cursor.fetchone()['pending_requests']
        
        cursor.execute("SELECT COUNT(*) AS pending_reports FROM violation_reports WHERE is_resolved = FALSE")
        pending_reports = cursor.fetchone()['pending_reports']

        db.close()

    if current_user.user_type == 'Donor':
        return render_template('dashboard.html', matching_requests=matching_requests, session=session)
    
    else:
        return render_template('dashboard.html', total_users=total_users,
                                pending_donations=pending_donations, pending_requests=pending_requests, pending_reports=pending_reports, session=session, matching_requests=matching_requests)


@app.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (current_user.id,))
        user_data = cursor.fetchone()
        
        cursor.execute("SELECT disease_id, disease_name FROM diseases WHERE disease_id IN (SELECT disease_id FROM user_diseases WHERE user_id = %s)", (current_user.id,))
        diseases = cursor.fetchall()
        user_data['diseases'] = [disease['disease_name'] for disease in diseases]

        if not user_data:
            flash("User not found.", "danger")
            return redirect(url_for('dashboard'))

        return render_template('edit_profile.html', user=user_data)

    elif request.method == 'POST':
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        email = request.form.get('email').strip()
        phone = request.form.get('phone').strip()
        location = request.form.get('location').strip()

        error = None
        if not first_name or not last_name:
            error = 'First and last name are required.'
        elif not email or '@' not in email:
            error = 'A valid email is required.'
        elif not phone or len(phone) < 10:
            error = 'A valid phone number is required.'

        if error:
            flash(error, "danger")
            return render_template('edit_profile.html', user=request.form)

        cursor.execute("SELECT user_id FROM users WHERE (email = %s OR phone_number = %s) AND user_id != %s", (email, phone, current_user.id))
        user = cursor.fetchone()
        if user:
            flash("Email or phone number already in use by another account.", "danger")
            return render_template('edit_profile.html', user=request.form)

        update_query = """
            UPDATE users SET first_name = %s, last_name = %s, email = %s, phone_number = %s, location = %s
            WHERE user_id = %s
        """
        
        cursor.execute(update_query, (first_name, last_name, email, phone, location, current_user.id))
        db.commit()
        
        cursor.execute("DELETE FROM user_diseases WHERE user_id = %s", (current_user.id,))
        db.commit()

        for key, value in request.form.items():
            if key.startswith('blood_diseases_'):
                disease_name = value.strip()
                if disease_name and disease_name != 'None':
                    cursor.execute("SELECT disease_id FROM diseases WHERE disease_name = %s", (disease_name,))
                    disease_record = cursor.fetchone()

                    if disease_record:
                        disease_id = disease_record['disease_id']
                    else:
                        cursor.execute("INSERT INTO diseases (disease_name) VALUES (%s)", (disease_name,))
                        db.commit()
                        disease_id = cursor.lastrowid

                    cursor.execute("INSERT INTO user_diseases (user_id, disease_id) VALUES (%s, %s)", (current_user.id, disease_id))
                    db.commit()
                    
        flash("Profile updated successfully.", "success")
        return redirect(url_for('dashboard'))
    
    db.close()


@app.route('/user/history')
@login_required
def history():
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Donations WHERE donor_id = %s", (current_user.id,))
    donations = cursor.fetchall()
    
    cursor.execute("SELECT * FROM blood_requests WHERE user_id = %s", (current_user.id,))
    requests = cursor.fetchall()

    db.close()

    return render_template('history.html', donations=donations, requests=requests)


@app.route('/user/report', methods=['GET', 'POST'])
@login_required
def report():
    db = get_db_connection()
    cursor = db.cursor()
    
    if request.method == 'POST':
        violator_id = request.form.get('violator_id')
        violation_reason = request.form.get('violation_reason')
        
        if violator_id:
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (violator_id,))
            violator = cursor.fetchone()

        report_date = datetime.date(datetime.now())
        
        if violator:
            cursor.execute("""
                INSERT INTO violation_reports (violator_id, reporter_id, report_date, is_resolved, violation_reason)
                VALUES (%s, %s, %s, %s, %s)
            """, (violator_id, current_user.id, report_date, 0, violation_reason))
            db.commit()
        else:
            cursor.execute("""
                INSERT INTO violation_reports (reporter_id, report_date, is_resolved, violation_reason)
                VALUES (%s, %s, %s, %s)
            """, (current_user.id, report_date, 0, violation_reason))
            db.commit()

        flash('Report submitted successfully!', 'success')
        return redirect(url_for('report'))

    db.close()
    
    return render_template('report.html', user=current_user)


@app.route('/admin/manage_donations')
@login_required
def manage_donations():
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Donations ORDER BY status ASC")
    donations = cursor.fetchall()
    
    for donation in donations:
        cursor.execute("SELECT first_name, last_name, blood_group FROM users WHERE user_id = %s", (donation['donor_id'],))
        donor = cursor.fetchone()
        donation['donor_name'] = donor['first_name'] + ' ' + donor['last_name']
        donation['donor_blood_group'] = donor['blood_group']
    
    db.close()

    return render_template('manage_donations.html', donations=donations)


@app.route('/admin/manage_donations/<int:donation_id>/<action>')
@login_required
def handle_donation_action(donation_id, action):
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM donations WHERE donation_id = %s", (donation_id,))
    donation = cursor.fetchone()
    
    if not donation:
        flash("Donation not found.", "danger")
        return redirect(url_for('manage_donations'))
    
    if donation['status'] == 'Processed':
        flash("Donation has already been processed.", "danger")
        return redirect(url_for('manage_donations'))
    
    if action == 'reject':
        
        cursor.execute("UPDATE donations SET status = 'Rejected' WHERE donation_id = %s", (donation_id,))
        db.commit()
        
        cursor.execute("UPDATE blood_requests SET is_fulfilled = FALSE WHERE request_id = %s", (donation['request_id'],))
        db.commit()
        
        cursor.execute("SELECT donated_date FROM donations WHERE donor_id = %s AND status = 'Processed' ORDER BY donated_date DESC LIMIT 1, 1", (donation['donor_id'],))
        second_last_donation_date = cursor.fetchone()

        if second_last_donation_date:
            cursor.execute("UPDATE donations SET donated_date = %s WHERE donation_id = %s", (second_last_donation_date['donated_date'], donation['donor_id']))
            db.commit()
        else:
            cursor.execute("UPDATE donations SET donated_date = NULL WHERE donation_id = %s", (donation['donor_id'],))
            db.commit()
                           
    elif action == 'process':
        cursor.execute("UPDATE donations SET status = 'Processed' WHERE donation_id = %s", (donation_id,))
        db.commit()
        
        cursor.execute("UPDATE blood_requests SET is_fulfilled = TRUE WHERE request_id = %s", (donation['request_id'],))
        db.commit()
        
        cursor.execute("UPDATE donations SET donated_date = %s WHERE donation_id = %s", (donation['donated_date'], donation['donor_id']))
        db.commit()
        
    db.close()
    return redirect(url_for('manage_donations'))


@app.route('/admin/manage_reports')
@login_required
def manage_reports():
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM violation_reports ORDER BY is_resolved ASC")
    reports = cursor.fetchall()
    print(reports)

    db.close()

    return render_template('manage_reports.html', reports=reports)


@app.route('/admin/manage_reports/<int:report_id>/<action>')
@login_required
def handle_report_action(report_id, action):
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM violation_reports WHERE report_id = %s", (report_id,))
    report = cursor.fetchone()
    
    violator = get_user_by_id(report['violator_id'])
    
    if current_user.id == report['violator_id']:
        flash("You cannot resolve your own report.", "danger")
        return redirect(url_for('manage_reports'))
    
    if current_user.user_type == 'Staff' and violator.user_type == 'Admin':
        flash("Staff users cannot resolve reports against Admin users.", "danger")
        return redirect(url_for('manage_reports'))
        
    if action == 'resolve':
        cursor.execute("UPDATE violation_reports SET is_resolved = TRUE WHERE report_id = %s", (report_id,))
        db.commit()
        
    elif action == 'ban' and violator:
        cursor.execute("UPDATE users SET status = 'Banned' WHERE user_id = %s", (report['violator_id'],))
        db.commit()
        cursor.execute("UPDATE violation_reports SET is_resolved = TRUE WHERE report_id = %s", (report_id,))
        db.commit()
        
    db.close()
    return redirect(url_for('manage_reports'))


@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('manage_users'))

        return render_template('edit_user.html', user=user)

    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        user_type = request.form.get('user_type')
        status = request.form.get('status')

        if current_user.user_type == 'Staff' and user_type == 'Admin':
            flash("Staff users cannot change the role to Admin.", "danger")
            return redirect(url_for('manage_users'))
        
        if current_user.id == user_id and user_type != 'Admin':
            flash("You cannot change your own role.", "danger")
            return redirect(url_for('manage_users'))
        
        if current_user.id == user_id and status == 'Banned':
            flash("You cannot ban your own account.", "danger")
            return redirect(url_for('manage_users'))

        update_query = """
            UPDATE users SET first_name = %s, last_name = %s, email = %s, phone_number = %s, user_type = %s, status = %s
            WHERE user_id = %s
        """
        cursor.execute(update_query, (first_name, last_name, email, phone, user_type, status, user_id))
        db.commit()

        if user_type in ['Admin', 'Staff']:
            cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_id,))
            staff = cursor.fetchone()
            
            if staff:
                cursor.execute("UPDATE staff SET role = %s WHERE user_id = %s", (user_type, user_id))
                db.commit()
            else:
                cursor.execute("INSERT INTO staff (user_id, role) VALUES (%s, %s)", (user_id, user_type))
                db.commit()
        
        else:
            cursor.execute("DELETE FROM staff WHERE user_id = %s", (user_id,))
            db.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for('manage_users'))

    db.close()


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.user_type not in ['Admin', 'Staff']:
        abort(403)

    db = get_db_connection()
    cursor = db.cursor()

    if current_user.id == user_id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for('manage_users'))

    if current_user.user_type == 'Staff':
        cursor.execute("SELECT user_type FROM users WHERE user_id = %s", (user_id,))
        user_type = cursor.fetchone()[0]
        
        if user_type != 'Donor':
            flash("Staff users cannot delete Admin or Staff accounts.", "danger")
            return redirect(url_for('manage_users'))
        
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    
    db.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for('manage_users'))


@app.route('/add_donation', methods=['GET', 'POST'])
@login_required
def add_donation():
    db = get_db_connection()
    cursor = db.cursor()

    request_id = request.args.get('request_id')
    hospital_name = request.args.get('hospital_name')
    location = request.args.get('location')

    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name')
        location = request.form.get('location')
        proof_document = request.files.get('proof_document')
        donated_date = request.form.get('donated_date')
        request_id = request.form.get('request_id')
            
        if not (proof_document and donated_date):
            flash('All fields are required.', 'error')
        else:
            if donated_date:
                donated_date = datetime.strptime(donated_date, '%Y-%m-%d')
                current_date = datetime.now()
                three_months_ago = current_date - timedelta(days=90)

                if donated_date > current_date or donated_date < three_months_ago:
                    flash('Donated date should be within the last 3 months and not in the future.', 'warning')
                    return redirect(url_for('add_donation'))
                
                cursor.execute("SELECT disease_id FROM user_diseases WHERE user_id = %s", (current_user.id,))
                diseases = cursor.fetchall()
                
                cursor.execute("SELECT donated_date FROM donations WHERE donor_id = %s AND status = 'Processed' ORDER BY donated_date DESC LIMIT 1", (current_user.id,))
                last_donation_date = cursor.fetchone()
                last_donated = (last_donation_date and (datetime.now().date() - last_donation_date[0]).days) if last_donation_date else 90
                
                cursor.execute("SELECT date_of_birth FROM users WHERE user_id = %s", (current_user.id,))
                date_of_birth = cursor.fetchone()
                age = datetime.now().year - date_of_birth[0].year
                
                if diseases or last_donated < 90 or age < 18:
                    flash('You cannot donate blood at the moment.', 'warning')
                    return redirect(url_for('add_donation'))
            
            if current_user.user_type in ['Admin', 'Staff']:
                cursor.execute("""
                    INSERT INTO donations (donor_id, proof_document, donated_date, status, hospital_name, location)
                    VALUES (%s, %s, %s, 'Processed', %s, %s)
                """, (current_user.id, save_file(proof_document, current_user), donated_date, hospital_name, location))
                db.commit()

                cursor.execute("UPDATE donors SET last_donation_date = %s WHERE user_id = %s", (donated_date, current_user.id))
                db.commit()
            
            else:   
                cursor.execute("""
                    INSERT INTO donations (donor_id, proof_document, donated_date, status, hospital_name, location)
                    VALUES (%s, %s, %s, 'Unprocessed', %s, %s)
                """, (current_user.id, save_file(proof_document, current_user), donated_date, hospital_name, location))
                db.commit()
                
                cursor.execute("UPDATE donors SET last_donation_date = %s WHERE user_id = %s", (donated_date, current_user.id))
                db.commit()
            
            if request_id:
                cursor.execute("UPDATE blood_requests SET is_fulfilled = TRUE WHERE request_id = %s", (request_id,))
                db.commit()
                
                cursor.execute("SELECT donation_id FROM donations WHERE donor_id = %s ORDER BY donation_id DESC LIMIT 1", (current_user.id,))
                donation_id = cursor.fetchone()[0]
                cursor.execute("UPDATE donations SET request_id = %s WHERE donation_id = %s", (request_id, donation_id))
                db.commit()
    
            flash('Donation added successfully!', 'success')
            return redirect(url_for('add_donation'))

    db.close()

    return render_template('add_donation.html', request_id=request_id, hospital_name=hospital_name, location=location)


@app.route('/user/profile')
@login_required
def user_profile():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (current_user.id,))
    user_data = cursor.fetchone()

    if not user_data:
        flash("User not found.", "danger")
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT disease_id, disease_name FROM diseases WHERE disease_id IN (SELECT disease_id FROM user_diseases WHERE user_id = %s)", (current_user.id,))
    diseases = cursor.fetchall()
    user_data['diseases'] = [disease['disease_name'] for disease in diseases]

    db.close()

    return render_template('user_profile.html', user=user_data)


@app.route('/current_requests', methods=['GET', 'POST'])
def current_requests():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM blood_requests WHERE user_id = %s AND is_fulfilled = FALSE", (current_user.id,))
    blood_requests = cursor.fetchall()
    
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        cursor.execute("UPDATE blood_requests SET is_fulfilled = TRUE WHERE request_id = %s", (request_id,))
        db.commit()
        
        flash("Request fulfilled successfully!", "success")
        return redirect(url_for('current_requests'))

    db.close()
    
    return render_template('current_requests.html', requests=blood_requests)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT phone_number, date_of_birth FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            if phone != user['phone_number'] or date_of_birth != str(user['date_of_birth']):
                flash("Invalid phone number or date of birth.", "danger")
                return redirect(url_for('forget_password'))

            session['reset_password_email'] = email

            return redirect(url_for('reset_password'))
        
        else:
            flash("Email not found.", "danger")
            return redirect(url_for('forget_password'))
        
        db.close()
        
    return render_template('forget_password.html', form=None)



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    
    email = session.get('reset_password_email')

    if not email:
        flash("Email not found.", "danger")
        return redirect(url_for('forget_password'))

    if request.method == 'POST':
        
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return render_template('reset_password.html')
        
        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character", "warning")
            return render_template("reset_password.html")
        
        hashed_password = generate_password_hash(password)
        
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        db.commit()

        flash("Password changed successfully!", "success")
        
        session.pop('reset_password_email', None)

    return render_template('reset_password.html', form=None)


@app.route("/diseases", methods=["GET"])
def get_diseases():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT disease_name FROM Diseases")
    diseases = cursor.fetchall()
    return jsonify([disease[0] for disease in diseases])


@app.route("/locations", methods=["GET"])
def get_locations():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT location FROM Users")
    locations = cursor.fetchall()
    
    return jsonify(list(set([location[0] for location in locations])))


@app.errorhandler(403)
def forbidden_error(error):
    code_msg = "403 - Forbidden"
    msg = "You do not have permission to access this page."
    return render_template('error.html', code_msg=code_msg, msg=msg), 403


@app.errorhandler(404)
def not_found_error(error):
    code_msg = "404 - Not Found"
    msg = "The page you are looking for does not exist."
    return render_template('error.html', code_msg=code_msg, msg=msg), 404


@app.errorhandler(500)
def internal_error(error):
    code_msg = "500 - Internal Server Error"
    msg = "Something went wrong on our end. Please try again later."
    return render_template('error.html', code_msg=code_msg, msg=msg), 500


if __name__ == '__main__':
    app.run(debug=True)