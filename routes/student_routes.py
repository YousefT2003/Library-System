"""
Student Routes — URL routing for student management.
"""

from flask import Blueprint
from controllers.student_controller import StudentController
from controllers.auth_controller import login_required

student_bp = Blueprint('students', __name__, url_prefix='/students')


@student_bp.route('/')
@login_required
def index():
    return StudentController.index()


@student_bp.route('/create', methods=['POST'])
@login_required
def create():
    return StudentController.create()


@student_bp.route('/update/<int:student_id>', methods=['POST'])
@login_required
def update(student_id):
    return StudentController.update(student_id)


@student_bp.route('/delete/<int:student_id>', methods=['POST'])
@login_required
def delete(student_id):
    return StudentController.delete(student_id)


@student_bp.route('/history/<int:student_id>')
@login_required
def history(student_id):
    return StudentController.history(student_id)


@student_bp.route('/api/search')
@login_required
def api_search():
    return StudentController.api_search()
