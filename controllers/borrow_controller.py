"""
Borrow Controller — Business logic for lending and returning books.
"""

from flask import request, render_template, redirect, url_for, flash, session
from models.borrow_model import BorrowModel
from models.book_model import BookModel
from models.student_model import StudentModel

class BorrowController:

    @staticmethod
    def index():
        status = request.args.get('status', '')
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)

        # Auto-mark overdue records
        BorrowModel.mark_overdue()

        # --- الجزء المعدل: جلب البيانات للقوائم المنسدلة ---
        # جلب جميع الكتب المتاحة والطلاب لعرضهم في صفحة الاستعارة
        books = BookModel.get_all() # يمكنك استخدام BookModel.get_all_available() إذا كانت موجودة
        students = StudentModel.get_all()
        # --------------------------------------------------

        records = BorrowModel.get_all(status=status or None, search=search, page=page)
        total = BorrowModel.count(status=status or None)

        # تمرير المتغيرات الجديدة (books و students) للقالب
        return render_template('borrow.html', records=records,
                               status=status, search=search,
                               page=page, total=total, per_page=20,
                               books=books, students=students)

    @staticmethod
    def lend():
        """Process a new book lending."""
        student_id = request.form.get('student_id', type=int)
        book_id = request.form.get('book_id', type=int)
        borrow_days = request.form.get('borrow_days', 14, type=int)

        if not student_id or not book_id:
            flash('Please select both a student and a book.', 'error')
            return redirect(url_for('borrow.index'))

        # Check student exists
        student = StudentModel.get_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('borrow.index'))

        # Check borrowing limit
        active = StudentModel.get_active_borrow_count(student_id)
        if active >= student['max_books']:
            flash(f'Student has reached the maximum borrowing limit ({student["max_books"]} books).', 'error')
            return redirect(url_for('borrow.index'))

        # Check book availability
        book = BookModel.get_by_id(book_id)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('borrow.index'))

        if book['available_copies'] <= 0:
            flash('No copies available for this book.', 'error')
            return redirect(url_for('borrow.index'))

        # Create record and update book availability
        librarian_id = session.get('user_id')
        BorrowModel.create(student_id, book_id, librarian_id, borrow_days)
        BookModel.update_available_copies(book_id, -1)

        flash(f'Book "{book["title"]}" lent to {student["first_name"]} {student["last_name"]}.', 'success')
        return redirect(url_for('borrow.index'))

    @staticmethod
    def return_book(record_id):
        """Process a book return."""
        record = BorrowModel.get_by_id(record_id)
        if not record:
            flash('Borrow record not found.', 'error')
            return redirect(url_for('borrow.index'))

        if record['status'] == 'returned':
            flash('This book has already been returned.', 'error')
            return redirect(url_for('borrow.index'))

        result = BorrowModel.return_book(record_id)
        BookModel.update_available_copies(record['book_id'], +1)

        if result['fine'] > 0:
            flash(f'Book returned with a fine of ${result["fine"]:.2f} for overdue days.', 'warning')
        else:
            flash('Book returned successfully!', 'success')

        return redirect(url_for('borrow.index'))