"""
Student Model — CRUD operations for the students table.
"""

from database.connection import execute_query


class StudentModel:

    @staticmethod
    def get_all(search=None, page=1, per_page=20):
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if search:
            query += " AND (student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR department LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like, like])

        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        return execute_query(query, tuple(params), fetch=True)

    @staticmethod
    def count(search=None):
        query = "SELECT COUNT(*) AS total FROM students WHERE 1=1"
        params = []
        if search:
            query += " AND (student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])
        result = execute_query(query, tuple(params), fetch=True)
        return result[0]['total'] if result else 0

    @staticmethod
    def get_by_id(id):
        result = execute_query("SELECT * FROM students WHERE id = %s", (id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_by_student_id(student_id):
        result = execute_query("SELECT * FROM students WHERE student_id = %s", (student_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(data):
        query = """
            INSERT INTO students (student_id, first_name, last_name, email, phone, department, class_name, max_books)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return execute_query(query, (
            data['student_id'], data['first_name'], data['last_name'],
            data.get('email'), data.get('phone'),
            data.get('department'), data.get('class_name'),
            data.get('max_books', 3)
        ), commit=True)

    @staticmethod
    def update(id, data):
        query = """
            UPDATE students SET first_name=%s, last_name=%s, email=%s,
            phone=%s, department=%s, class_name=%s, max_books=%s
            WHERE id=%s
        """
        return execute_query(query, (
            data['first_name'], data['last_name'],
            data.get('email'), data.get('phone'),
            data.get('department'), data.get('class_name'),
            data.get('max_books', 3), id
        ), commit=True)

    @staticmethod
    def delete(id):
        return execute_query("DELETE FROM students WHERE id = %s", (id,), commit=True)

    @staticmethod
    def get_active_borrow_count(student_id):
        """Count active (non-returned) borrows for a student."""
        result = execute_query(
            "SELECT COUNT(*) AS cnt FROM borrow_records WHERE student_id = %s AND status != 'returned'",
            (student_id,), fetch=True
        )
        return result[0]['cnt'] if result else 0

    @staticmethod
    def get_top_borrowers(limit=5):
        query = """
            SELECT s.id, s.student_id, s.first_name, s.last_name, s.department,
                   COUNT(br.id) AS borrow_count
            FROM students s
            JOIN borrow_records br ON s.id = br.student_id
            GROUP BY s.id
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch=True)
