"""
Dashboard Routes — URL routing for the dashboard.
"""

from flask import Blueprint, jsonify
from controllers.dashboard_controller import DashboardController
from controllers.auth_controller import login_required
from database.connection import get_connection

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    return DashboardController.index()


@dashboard_bp.route('/chart-data/months')
def chart_months():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            MONTH(borrow_date) AS month,
            COUNT(*) AS borrow_count
        FROM borrow_records
        GROUP BY MONTH(borrow_date)
        ORDER BY MONTH(borrow_date)
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


# الرابط الذي سيتصل به الجافاسكريبت لجلب بيانات الشارتات كاملة
@dashboard_bp.route('/dashboard-data')
@login_required # يفضل إضافته للأمان
def dashboard_data():
    return DashboardController.get_dashboard_data()