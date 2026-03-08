from flask import request, render_template, redirect, url_for, flash, session
from models.librarian_model import LibrarianModel
from functools import wraps

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


# --- Auth Controller ---
class AuthController:

    # ---------------- LOGIN ----------------
    @staticmethod
    def login_page():
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return render_template('login.html')

    @staticmethod
    def login():
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return redirect(url_for('auth.login'))

        user = LibrarianModel.get_by_username(username)

        if not user or not LibrarianModel.verify_password(password, user['password_hash']):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['user_role'] = user['role']

        flash(f'Welcome back, {user["full_name"]}!', 'success')
        return redirect(url_for('dashboard.index'))


    # ---------------- LOGOUT ----------------
    @staticmethod
    def logout():
        session.clear()
        flash('You have been logged out.', 'success')
        return redirect(url_for('auth.login'))


    # ---------------- SIGNUP ----------------
    @staticmethod
    def signup_page():
        return render_template('signup.html')

    @staticmethod
    def signup():
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # --- Validation ---
        if not full_name or not email or not username or not password or not confirm_password:
            flash("جميع الحقول مطلوبة!", "danger")
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash("كلمات المرور غير متطابقة!", "danger")
            return redirect(url_for('auth.signup'))

        # Check if username exists
        if LibrarianModel.get_by_username(username):
            flash("اسم المستخدم مستخدم بالفعل!", "danger")
            return redirect(url_for('auth.signup'))

        # --- Prepare data for model ---
        data = {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
            'role': 'librarian'
        }

        # --- Insert into DB ---
        LibrarianModel.create(data)

        flash("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.", "success")
        return redirect(url_for('auth.login'))