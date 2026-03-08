"""
Borrow Model — CRUD operations for borrow_records table.
"""

from database.connection import execute_query
from datetime import date, timedelta


# Fine per overdue day in currency units
FINE_PER_DAY = 0.50
DEFAULT_BORROW_DAYS = 14


class BorrowModel:

    @staticmethod
    def get_all(status=None, search=None, page=1, per_page=20):
        query = """
            SELECT br.*, b.title AS book_title, b.isbn,
                   s.student_id AS student_code, s.first_name, s.last_name,
                   l.full_name AS librarian_name
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN students s ON br.student_id = s.id
            LEFT JOIN librarians l ON br.librarian_id = l.id
            WHERE 1=1
        """
        params = []

        if status:
            query += " AND br.status = %s"
            params.append(status)

        if search:
            query += " AND (b.title LIKE %s OR s.student_id LIKE %s OR s.first_name LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])

        query += " ORDER BY br.created_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        return execute_query(query, tuple(params), fetch=True)

    @staticmethod
    def count(status=None):
        query = "SELECT COUNT(*) AS total FROM borrow_records WHERE 1=1"
        params = []
        if status:
            query += " AND status = %s"
            params.append(status)
        result = execute_query(query, tuple(params), fetch=True)
        return result[0]['total'] if result else 0

    @staticmethod
    def get_by_id(id):
        query = """
            SELECT br.*, b.title AS book_title, b.isbn,
                   s.student_id AS student_code, s.first_name, s.last_name
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN students s ON br.student_id = s.id
            WHERE br.id = %s
        """
        result = execute_query(query, (id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(student_id, book_id, librarian_id=None, borrow_days=DEFAULT_BORROW_DAYS):
        """Create a new borrow record with automatic due date."""
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=borrow_days)
        query = """
            INSERT INTO borrow_records (student_id, book_id, librarian_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s, 'borrowed')
        """
        return execute_query(query, (student_id, book_id, librarian_id, borrow_date, due_date), commit=True)

    @staticmethod
    def return_book(record_id):
        """Mark a borrow record as returned, calculate fine if overdue."""
        record = BorrowModel.get_by_id(record_id)
        if not record:
            return None

        return_date = date.today()
        fine = 0.0

        if return_date > record['due_date']:
            overdue_days = (return_date - record['due_date']).days
            fine = overdue_days * FINE_PER_DAY

        query = """
            UPDATE borrow_records
            SET return_date = %s, status = 'returned', fine_amount = %s
            WHERE id = %s
        """
        execute_query(query, (return_date, fine, record_id), commit=True)
        return {'fine': fine, 'return_date': return_date}

    @staticmethod
    def mark_overdue():
        """Update all overdue records that are still marked as 'borrowed'."""
        query = """
            UPDATE borrow_records
            SET status = 'overdue'
            WHERE status = 'borrowed' AND due_date < CURDATE()
        """
        return execute_query(query, commit=True)

    @staticmethod
    def get_student_history(student_id):
        query = """
            SELECT br.*, b.title AS book_title, b.isbn
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.student_id = %s
            ORDER BY br.borrow_date DESC
        """
        return execute_query(query, (student_id,), fetch=True)

    @staticmethod
    def get_overdue_records():
        query = """
            SELECT br.*, b.title AS book_title, s.student_id AS student_code,
                   s.first_name, s.last_name, s.email,
                   DATEDIFF(CURDATE(), br.due_date) AS overdue_days
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN students s ON br.student_id = s.id
            WHERE br.status IN ('borrowed', 'overdue') AND br.due_date < CURDATE()
            ORDER BY overdue_days DESC
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_stats_by_period(period='daily'):
        """Get lending statistics grouped by period."""
        if period == 'daily':
            group = "DATE(borrow_date)"
        elif period == 'weekly':
            group = "YEARWEEK(borrow_date)"
        else:
            group = "DATE_FORMAT(borrow_date, '%%Y-%%m')"

        query = f"""
            SELECT {group} AS period, COUNT(*) AS total_borrows
            FROM borrow_records
            GROUP BY {group}
            ORDER BY {group} DESC
            LIMIT 30
        """
        return execute_query(query, fetch=True)
