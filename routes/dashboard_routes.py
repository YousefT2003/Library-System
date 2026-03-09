"""
Dashboard Routes — URL routing for the dashboard.
"""

from flask import Blueprint
from controllers.dashboard_controller import DashboardController
from controllers.auth_controller import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    return DashboardController.index()

@dashboard_bp.route('/chart-data/months')
def chart_months():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            MONTH(borrow_date) AS month,
            COUNT(*) AS borrow_count
        FROM borrow_records
        GROUP BY MONTH(borrow_date)
        ORDER BY MONTH(borrow_date)
    """)
    data = cursor.fetchall()
    return jsonify(data)