"""
Auth Routes — Login, logout, and authentication.
"""

from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET'])
def login():
    return AuthController.login_page()


@auth_bp.route('/login', methods=['POST'])
def login_post():
    return AuthController.login()


@auth_bp.route('/logout')
def logout():
    return AuthController.logout()

# مسار عرض صفحة إنشاء الحساب
@auth_bp.route('/signup', methods=['GET'])
def signup():
    return AuthController.signup_page()

# مسار معالجة بيانات إنشاء الحساب (الضغط على زر التسجيل)
@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    return AuthController.signup()