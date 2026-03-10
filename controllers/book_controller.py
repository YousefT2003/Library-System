"""
Book Controller — Business logic for book operations.
"""

from flask import request, jsonify, render_template, redirect, url_for, flash
from models.book_model import BookModel
from models.category_model import CategoryModel
# --- إضافات الباركود ---
import os
from barcode import EAN13
from barcode.writer import ImageWriter
# -----------------------

class BookController:

    @staticmethod
    def index():
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
        BookModel.create(data)
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def update(book_id):
        data = {
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'category_id': request.form.get('category_id', type=int),
            'edition': request.form.get('edition', '').strip(),
            'publisher': request.form.get('publisher', '').strip(),
            'publish_year': request.form.get('publish_year', type=int),
            'total_copies': request.form.get('total_copies', 1, type=int),
            'description': request.form.get('description', '').strip(),
        }
        BookModel.update(book_id, data)
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def delete(book_id):
        BookModel.delete(book_id)
        flash('Book deleted.', 'success')
        return redirect(url_for('books.index'))

    @staticmethod
    def generate_barcode(book_id):
        """توليد باركود وحفظه باستخدام EAN13."""
        book = BookModel.get_by_id(book_id)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('books.index'))

        # ضبط مسار المجلد
        barcode_folder = os.path.join('public', 'barcodes')
        if not os.path.exists(barcode_folder):
            os.makedirs(barcode_folder)
            
        # تجهيز رقم الباركود
        raw_code = str(book.get('isbn', book_id)).replace('-', '')
        code_str = raw_code.zfill(12)[:12]
        
        try:
            # التوليد
            my_barcode = EAN13(code_str, writer=ImageWriter())
            file_path = os.path.join(barcode_folder, f"book_{book_id}")
            my_barcode.save(file_path)
            flash(f'Barcode generated successfully for {book["title"]}!', 'success')
        except Exception as e:
            flash(f'Error generating barcode: {str(e)}', 'error')
            
        return redirect(url_for('books.index'))