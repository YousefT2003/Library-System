"""
Dashboard Controller — Analytics and overview data.
"""

from flask import render_template, jsonify
from database.connection import get_connection
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

        return render_template(
            'dashboard.html',
            total_books=total_books,
            total_students=total_students,
            total_borrowed=total_borrowed,
            total_overdue=total_overdue,
            most_borrowed=most_borrowed,
            top_borrowers=top_borrowers,
            low_stock=low_stock,
            overdue_records=overdue_records,
            stats=stats
        )

    @staticmethod
    def get_dashboard_data():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # PIE CHART
        cursor.execute("""
            SELECT c.name AS category, COUNT(*) AS borrow_count
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN categories c ON b.category_id = c.id
            GROUP BY c.name
        """)
        pie_data = cursor.fetchall()

        # BAR CHART
        cursor.execute("""
            SELECT DATE_FORMAT(br.borrow_date, '%b') AS month, COUNT(*) AS borrow_count
            FROM borrow_records br
            GROUP BY month
            ORDER BY MONTH(STR_TO_DATE(month, '%b'))
        """)
        bar_data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"pie": pie_data, "bar": bar_data})