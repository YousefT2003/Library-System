"""
Book Routes — URL routing for book management.
"""

from flask import Blueprint
from controllers.book_controller import BookController
from controllers.auth_controller import login_required

# تأكد من أن اسم الـ Blueprint هو 'books' كما في كودك الأصلي
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

# المسار الجديد لتوليد الباركود
@book_bp.route('/generate-barcode/<int:book_id>')
@login_required
def generate_barcode(book_id):
    """
    مسار لتوليد صورة باركود للكتاب المختار
    """
    return BookController.generate_barcode(book_id)