"""
Library Management System — Main Application Entry Point
=========================================================
A production-ready Flask application for managing books,
students, and lending operations in an educational institution.
"""

import os
from flask import Flask
from database.connection import init_database, seed_database

# Import route blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.book_routes import book_bp
from routes.student_routes import student_bp
from routes.borrow_routes import borrow_bp


def create_app():
    """Application factory — creates and configures the Flask app."""
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='public',
        static_url_path='/static'
    )

    # Configuration
    app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(borrow_bp)

    return app


if __name__ == '__main__':
    # Initialize database and seed data
    print("=" * 50)
    print(" Library Management System")
    print("=" * 50)

    try:
        init_database()
        seed_database()
    except Exception as e:
        print(f"[WARNING] Database setup failed: {e}")
        print("Make sure MySQL is running and credentials are correct.")

    app = create_app()
    
    # Run the development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
