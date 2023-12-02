import os
import re
from datetime import datetime

from flask import current_app
from werkzeug.utils import secure_filename


def save_file(file, current_user):
    if file:
        uploads_folder = 'static/uploads'
        os.makedirs(uploads_folder, exist_ok=True)
        file_extension = file.filename.split('.')[-1]
        
        file.filename = f"{current_user.id}-{current_user.name}-'donation-proof'-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.{file_extension}"

        filename = secure_filename(file.filename)

        file_path = os.path.join(uploads_folder, filename)
        file.save(file_path)
        return file_path[7:]

    return None

def is_strong_password(password):
    if (len(password) < 8 or
        not re.search("[a-z]", password) or
        not re.search("[A-Z]", password) or
        not re.search("[0-9]", password) or
            not re.search("[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True
