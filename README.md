# 📚 Library Management System

A production-ready, full-stack Library Management System built for educational institutions.

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Auth:** Session-based with bcrypt password hashing

## Features

- 📖 **Book Management** — Add, edit, delete, search, filter books
- 🎓 **Student Management** — Register students, view borrowing history
- 🔄 **Lending & Returning** — Lend books, auto due dates, overdue detection, fines
- 📊 **Dashboard** — Analytics, stats, low-stock alerts, overdue tracking
- 🔐 **Authentication** — Role-based (Admin, Librarian, Assistant)
- 🎨 **Modern UI** — Responsive, sidebar navigation, modals, color-coded status

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 5.7+ or 8.0+
- pip

### 1. Clone & Install Dependencies

```bash
cd library-system
pip install flask mysql-connector-python bcrypt
```

### 2. Configure Database

Edit `database/connection.py` or set environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=library_db
```

### 3. Run the Application

```bash
python app.py
```

The app will:
1. Create the database if it doesn't exist
2. Run the schema (create tables)
3. Seed sample data
4. Start on `http://localhost:5000`

### 4. Login

- **Username:** `admin`
- **Password:** `admin123`

## Folder Structure

```
library-system/
├── app.py                  # Main entry point
├── database/
│   ├── connection.py       # MySQL connection pool & helpers
│   ├── schema.sql          # Table definitions
│   └── seed.sql            # Sample data
├── models/
│   ├── book_model.py       # Book CRUD operations
│   ├── student_model.py    # Student CRUD operations
│   ├── borrow_model.py     # Borrow/return operations
│   ├── librarian_model.py  # Auth & user management
│   └── category_model.py   # Category operations
├── controllers/
│   ├── book_controller.py
│   ├── student_controller.py
│   ├── borrow_controller.py
│   ├── auth_controller.py
│   └── dashboard_controller.py
├── routes/
│   ├── book_routes.py
│   ├── student_routes.py
│   ├── borrow_routes.py
│   ├── auth_routes.py
│   └── dashboard_routes.py
├── views/
│   ├── layout.html         # Base template with sidebar
│   ├── login.html
│   ├── dashboard.html
│   ├── books.html
│   ├── students.html
│   └── borrow.html
├── public/
│   ├── css/style.css       # All styles
│   └── js/app.js           # Client-side JavaScript
└── README.md
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | MySQL host |
| `DB_PORT` | 3306 | MySQL port |
| `DB_USER` | root | MySQL username |
| `DB_PASSWORD` | (empty) | MySQL password |
| `DB_NAME` | library_db | Database name |
| `SECRET_KEY` | (default) | Flask session secret |
| `PORT` | 5000 | Server port |
| `FLASK_DEBUG` | True | Debug mode |

## Deployment on Replit

1. Create a new Python Replit
2. Upload all files maintaining the folder structure
3. In the Shell, run: `pip install flask mysql-connector-python bcrypt`
4. Set up a MySQL database (use Replit's database or an external MySQL service)
5. Set environment variables in Replit's Secrets tab
6. Click Run

## License

MIT
