from flask import request, render_template, redirect, url_for, flash, jsonify
from models.book_model import BookModel
from models.category_model import CategoryModel
import os
import barcode
from barcode.writer import ImageWriter

class BookController:
    @staticmethod
    def index():
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        available_only = request.args.get('available_only') == '1'
        page = request.args.get('page', 1, type=int)
        
        books = BookModel.get_all(search=search, category_id=category_id, available_only=available_only, page=page)
        total = BookModel.count(search=search, category_id=category_id, available_only=available_only)
        categories = CategoryModel.get_all()
        
        return render_template('books.html', books=books, categories=categories, search=search, 
                               category_id=category_id, available_only=available_only, 
                               page=page, total=total, per_page=20)

    @staticmethod
    def create():
        if request.method == 'POST':
            book_data = {
                'title': request.form.get('title'),
                'author': request.form.get('author'),
                'isbn': request.form.get('isbn'),
                'category_id': request.form.get('category_id'),
                'edition': request.form.get('edition'),
                'publisher': request.form.get('publisher'),
                'publish_year': request.form.get('publish_year'),
                'total_copies': request.form.get('total_copies'),
                'description': request.form.get('description')
            }
            try:
                BookModel.create(book_data)
                flash('Book added successfully!', 'success')
            except Exception as e:
                flash(f'ُError: {str(e)}', 'error')
        return redirect(url_for('books.index'))

    @staticmethod
    def update(book_id):
        if request.method == 'POST':
            book_data = {
                'title': request.form.get('title'),
                'author': request.form.get('author'),
                'isbn': request.form.get('isbn'),
                'category_id': request.form.get('category_id'),
                'edition': request.form.get('edition'),
                'publisher': request.form.get('publisher'),
                'publish_year': request.form.get('publish_year'),
                'total_copies': request.form.get('total_copies'),
                'description': request.form.get('description')
            }
            try:
                BookModel.update(book_id, book_data)
                flash('Updated successfully!', 'success')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('books.index'))

    @staticmethod
    def delete(book_id):
        try:
            filename = f"book_{book_id}.png"
            barcode_path = os.path.join('public', 'barcodes', filename)
            if os.path.exists(barcode_path):
                os.remove(barcode_path)
            
            BookModel.delete(book_id)
            flash('Deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('books.index'))
        
    @staticmethod
    def generate_barcode(book_id):
        book = BookModel.get_by_id(book_id)
        if not book:
            flash('Book not found!', 'error')
            return redirect(url_for('books.index'))
            
        barcode_folder = os.path.join('public', 'barcodes')
        if not os.path.exists(barcode_folder):
            os.makedirs(barcode_folder)
            
        # التأكد من أن الـ ISBN طوله مناسب للـ EAN13
        raw_code = str(book.get('isbn', book_id)).replace('-', '').zfill(12)[:12]
        try:
            ean = barcode.get('ean13', raw_code, writer=ImageWriter())
            file_path = os.path.join(barcode_folder, f"book_{book_id}")
            ean.save(file_path)
            flash('Barcode generated successfully!', 'success')
        except Exception as e:
            flash(f'Error! {str(e)}', 'error')
        return redirect(url_for('books.index'))

    @staticmethod
    def search_api():
        """API endpoint for live searching books."""
        query = request.args.get('q', '')
        # البحث في الكتب باستخدام دالة get_all المتاحة في الموديل
        books = BookModel.get_all(search=query)
        
        # تحويل البيانات إلى JSON لتتمكن صفحة borrow.html من قراءتها
        results = [
            {
                'id': b.get('id'), 
                'title': b.get('title'), 
                'author': b.get('author', 'Unknown'), 
                'available_copies': b.get('available_copies', 0)
            } for b in books
        ]
        return jsonify(results)