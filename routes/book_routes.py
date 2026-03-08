"""
Book Routes — URL routing for book management.
"""

from flask import Blueprint
from controllers.book_controller import BookController
from controllers.auth_controller import login_required

book_bp = Blueprint('books', __name__, url_prefix='/books')

# All routes require login



@book_bp.route('/')
@login_required
def index():
    return BookController.index()


@book_bp.route('/create', methods=['POST'])
@login_required
def create():
    return BookController.create()


@book_bp.route('/update/<int:book_id>', methods=['POST'])
@login_required
def update(book_id):
    return BookController.update(book_id)


@book_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete(book_id):
    return BookController.delete(book_id)


@book_bp.route('/api/search')
@login_required
def api_search():
    return BookController.api_search()
