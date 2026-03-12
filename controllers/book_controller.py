from flask import request, render_template, redirect, url_for, flash
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
        
        return render_template('books.html', books=books, categories=categories, search=search, category_id=category_id, available_only=available_only, page=page, total=total, per_page=20)

    @staticmethod
    def generate_barcode(book_id):
        book = BookModel.get_by_id(book_id)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('books.index'))
        
        barcode_folder = os.path.join('public', 'barcodes')
        if not os.path.exists(barcode_folder):
            os.makedirs(barcode_folder)
            
        raw_code = str(book.get('isbn', book_id)).replace('-', '').zfill(12)[:12]
        
        try:
            # الحل: التأكد من استدعاء الكلاس بالطريقة الصحيحة
            ean = barcode.get('ean13', raw_code, writer=ImageWriter())
            file_path = os.path.join(barcode_folder, f"book_{book_id}")
            ean.save(file_path)
            flash('Barcode generated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            
        return redirect(url_for('books.index'))