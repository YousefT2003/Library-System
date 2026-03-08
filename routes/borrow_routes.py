"""
Borrow Routes — URL routing for lending and returning.
"""

from flask import Blueprint
from controllers.borrow_controller import BorrowController
from controllers.auth_controller import login_required

borrow_bp = Blueprint('borrow', __name__, url_prefix='/borrow')


@borrow_bp.route('/')
@login_required
def index():
    return BorrowController.index()


@borrow_bp.route('/lend', methods=['POST'])
@login_required
def lend():
    return BorrowController.lend()


@borrow_bp.route('/return/<int:record_id>', methods=['POST'])
@login_required
def return_book(record_id):
    return BorrowController.return_book(record_id)
