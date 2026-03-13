"""
Book Model — CRUD operations for the books table.
"""

from database.connection import execute_query

class BookModel:
    """Handles all database operations for books."""

    @staticmethod
    def get_all(search=None, category_id=None, available_only=False, page=1, per_page=20):
        query = """
            SELECT b.*, c.name AS category_name
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (b.title LIKE %s OR b.author LIKE %s OR b.isbn LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])
        if category_id:
            query += " AND b.category_id = %s"
            params.append(category_id)
        if available_only:
            query += " AND b.available_copies > 0"
        query += " ORDER BY b.created_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        return execute_query(query, tuple(params), fetch=True)

    @staticmethod
    def count(search=None, category_id=None, available_only=False):
        query = "SELECT COUNT(*) AS total FROM books b WHERE 1=1"
        params = []
        if search:
            query += " AND (b.title LIKE %s OR b.author LIKE %s OR b.isbn LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])
        if category_id:
            query += " AND b.category_id = %s"
            params.append(category_id)
        if available_only:
            query += " AND b.available_copies > 0"
        result = execute_query(query, tuple(params), fetch=True)
        return result[0]['total'] if result else 0

    @staticmethod
    def get_by_id(book_id):
        query = """
            SELECT b.*, c.name AS category_name
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.id = %s
        """
        result = execute_query(query, (book_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_by_isbn(isbn):
        result = execute_query("SELECT * FROM books WHERE isbn = %s", (isbn,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(data):
        query = """
        INSERT INTO books (title, author, isbn, category_id, edition, publisher, publish_year, total_copies, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['title'], data['author'], data['isbn'], data.get('category_id'),
            data.get('edition'), data.get('publisher'), data.get('publish_year'),
            data.get('total_copies'), data.get('description')
        )
        return execute_query(query, params, commit=True)

    @staticmethod
    def update(book_id, data):
        query = """
            UPDATE books SET title=%s, author=%s, isbn=%s, category_id=%s,
            edition=%s, publisher=%s, publish_year=%s, total_copies=%s,
            cover_image=%s, description=%s
            WHERE id=%s
        """
        params = (
            data['title'], data['author'], data['isbn'],
            data.get('category_id'), data.get('edition'),
            data.get('publisher'), data.get('publish_year'),
            data.get('total_copies', 1),
            data.get('cover_image'), data.get('description'),
            book_id
        )
        return execute_query(query, params, commit=True)

    @staticmethod
    def delete(book_id):
        return execute_query("DELETE FROM books WHERE id = %s", (book_id,), commit=True)

    @staticmethod
    def update_available_copies(book_id, change):
        query = "UPDATE books SET available_copies = available_copies + %s WHERE id = %s AND available_copies + %s >= 0"
        return execute_query(query, (change, book_id, change), commit=True)

    @staticmethod
    def get_most_borrowed(limit=5):
        query = """
            SELECT b.id, b.title, b.author, b.isbn, COUNT(br.id) AS borrow_count
            FROM books b
            JOIN borrow_records br ON b.
            id = br.book_id
            GROUP BY b.id
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch=True)

    @staticmethod
    def get_low_stock(threshold=2):
        query = """
            SELECT b.*, c.name AS category_name
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.available_copies <= %s
            ORDER BY b.available_copies ASC
        """
        return execute_query(query, (threshold,), fetch=True)