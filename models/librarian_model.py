"""
Librarian Model — Authentication and user management.
"""

import bcrypt
from database.connection import execute_query


class LibrarianModel:

    @staticmethod
    def get_by_username(username):
        result = execute_query("SELECT * FROM librarians WHERE username = %s AND is_active = 1", (username,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_by_id(id):
        result = execute_query("SELECT id, username, email, full_name, role, is_active FROM librarians WHERE id = %s", (id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Check a plain-text password against its bcrypt hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        """Generate a bcrypt hash for a password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def create(data):
        query = """
            INSERT INTO librarians (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        hashed = LibrarianModel.hash_password(data['password'])
        return execute_query(query, (
            data['username'], data['email'], hashed,
            data['full_name'], data.get('role', 'librarian')
        ), commit=True)

    @staticmethod
    def get_all():
        return execute_query(
            "SELECT id, username, email, full_name, role, is_active, created_at FROM librarians ORDER BY created_at DESC",
            fetch=True
        )
