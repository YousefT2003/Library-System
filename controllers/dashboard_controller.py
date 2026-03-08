"""
Dashboard Controller — Analytics and overview data.
"""

from flask import render_template
from models.book_model import BookModel
from models.student_model import StudentModel
from models.borrow_model import BorrowModel


class DashboardController:

    @staticmethod
    def index():
        # Summary stats
        total_books = BookModel.count()
        total_students = StudentModel.count()
        total_borrowed = BorrowModel.count(status='borrowed')
        total_overdue = BorrowModel.count(status='overdue')

        # Analytics
        most_borrowed = BookModel.get_most_borrowed(limit=5)
        top_borrowers = StudentModel.get_top_borrowers(limit=5)
        low_stock = BookModel.get_low_stock(threshold=2)
        overdue_records = BorrowModel.get_overdue_records()
        stats = BorrowModel.get_stats_by_period('daily')

        return render_template('dashboard.html',
                               total_books=total_books,
                               total_students=total_students,
                               total_borrowed=total_borrowed,
                               total_overdue=total_overdue,
                               most_borrowed=most_borrowed,
                               top_borrowers=top_borrowers,
                               low_stock=low_stock,
                               overdue_records=overdue_records,
                               stats=stats)
