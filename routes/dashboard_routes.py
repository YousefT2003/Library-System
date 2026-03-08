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
