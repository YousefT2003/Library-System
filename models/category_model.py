"""
Category Model — CRUD for book categories.
"""

from database.connection import execute_query


class CategoryModel:

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM categories ORDER BY name ASC", fetch=True)

    @staticmethod
    def get_by_id(id):
        result = execute_query("SELECT * FROM categories WHERE id = %s", (id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(name, description=None):
        return execute_query(
            "INSERT INTO categories (name, description) VALUES (%s, %s)",
            (name, description), commit=True
        )

    @staticmethod
    def update(id, name, description=None):
        return execute_query(
            "UPDATE categories SET name=%s, description=%s WHERE id=%s",
            (name, description, id), commit=True
        )

    @staticmethod
    def delete(id):
        return execute_query("DELETE FROM categories WHERE id = %s", (id,), commit=True)
