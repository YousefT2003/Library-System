"""
Book Controller — Business logic for book operations.
"""

from flask import request, jsonify, render_template, redirect, url_for, flash
from models.book_model import BookModel
from models.category_model import CategoryModel


class BookController:

    @staticmethod
    def index():
        """Render books page with filters."""
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        available_only = request.args.get('available_only') == '1'
        page = request.args.get('page', 1, type=int)

        books = BookModel.get_all(search=search, category_id=category_id,
                                   available_only=available_only, page=page)
        total = BookModel.count(search=search, category_id=category_id,
                                 available_only=available_only)
        categories = CategoryModel.get_all()

        return render_template('books.html',
                               books=books, categories=categories,
                               search=search, category_id=category_id,
                               available_only=available_only,
                               page=page, total=total, per_page=20)

    @staticmethod
    def create():
        """Handle book creation from form POST."""
        data = {
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'category_id': request.form.get('category_id', type=int),
            'edition': request.form.get('edition', '').strip(),
            'publisher': request.form.get('publisher', '').strip(),
            'publish_year': request.form.get('publish_year', type=int),
            'total_copies': request.form.get('total_copies', 1, type=int),
            'cover_image': request.form.get('cover_image', '').strip(),
            'description': request.form.get('description', '').strip(),
        }

        # Validation
        if not data['title'] or not data['author'] or not data['isbn']:
            flash('Title, Author, and ISBN are required.', 'error')
            return redirect(url_for('books.index'))

        if len(data['isbn']) > 20:
            flash('ISBN must be 20 characters or fewer.', 'error')
            return redirect(url_for('books.index'))

        # Check duplicate ISBN
        existing = BookModel.get_by_isbn(data['isbn'])
        if existing:
            flash('A book with this ISBN already exists.', 'error')
            return redirect(url_for('books.index'))

        BookModel.create(data)
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def update(book_id):
        """Handle book update."""
        book = BookModel.get_by_id(book_id)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('books.index'))

        data = {
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'category_id': request.form.get('category_id', type=int),
            'edition': request.form.get('edition', '').strip(),
            'publisher': request.form.get('publisher', '').strip(),
            'publish_year': request.form.get('publish_year', type=int),
            'total_copies': request.form.get('total_copies', 1, type=int),
            'cover_image': request.form.get('cover_image', '').strip(),
            'description': request.form.get('description', '').strip(),
        }

        if not data['title'] or not data['author'] or not data['isbn']:
            flash('Title, Author, and ISBN are required.', 'error')
            return redirect(url_for('books.index'))

        # Check duplicate ISBN (but not own)
        existing = BookModel.get_by_isbn(data['isbn'])
        if existing and existing['id'] != book_id:
            flash('Another book with this ISBN already exists.', 'error')
            return redirect(url_for('books.index'))

        BookModel.update(book_id, data)
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def delete(book_id):
        """Delete a book."""
        BookModel.delete(book_id)
        flash('Book deleted.', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def api_search():
        """JSON API for AJAX book search."""
        search = request.args.get('q', '')
        books = BookModel.get_all(search=search, per_page=10)
        return jsonify([{
            'id': b['id'], 'title': b['title'],
            'author': b['author'], 'isbn': b['isbn'],
            'available_copies': b['available_copies']
        } for b in books])
