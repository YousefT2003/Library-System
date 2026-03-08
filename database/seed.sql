-- ============================================
-- Seed Data for Library Management System
-- ============================================

-- Default categories
INSERT IGNORE INTO categories (name, description) VALUES
('Fiction', 'Novels, short stories, and literary fiction'),
('Non-Fiction', 'Factual and informational books'),
('Science', 'Physics, chemistry, biology, and more'),
('Mathematics', 'Algebra, calculus, statistics, and more'),
('History', 'Historical accounts and analysis'),
('Computer Science', 'Programming, algorithms, and technology'),
('Literature', 'Classic and modern literary works'),
('Engineering', 'Mechanical, electrical, civil engineering'),
('Philosophy', 'Philosophical texts and discourse'),
('Art & Design', 'Visual arts, design principles, and creativity');

-- Default admin user (password: admin123 — bcrypt hashed)
INSERT IGNORE INTO librarians (username, email, password_hash, full_name, role) VALUES
('admin', 'admin@library.edu', '$2b$12$LJ3m4ys3Lz0YOV9FP1X5/.VmE4L2UXfOjZKbYhEFmVqBXVz2GKWC6', 'System Administrator', 'admin');

-- Sample books
INSERT IGNORE INTO books (title, author, isbn, category_id, edition, publisher, publish_year, total_copies, available_copies) VALUES
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 6, '3rd', 'MIT Press', 2009, 5, 5),
('Clean Code', 'Robert C. Martin', '978-0132350884', 6, '1st', 'Prentice Hall', 2008, 3, 3),
('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 1, '1st', 'Harper Perennial', 1960, 4, 4),
('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 3, '1st', 'Bantam', 1998, 2, 2),
('Calculus: Early Transcendentals', 'James Stewart', '978-1285741550', 4, '8th', 'Cengage', 2015, 6, 6),
('The Art of War', 'Sun Tzu', '978-1599869773', 5, '1st', 'Filiquarian', 2007, 3, 3),
('Design Patterns', 'Gang of Four', '978-0201633610', 6, '1st', 'Addison-Wesley', 1994, 2, 2),
('1984', 'George Orwell', '978-0451524935', 1, '1st', 'Signet Classic', 1949, 5, 5),
('Physics for Scientists', 'Serway & Jewett', '978-1133947271', 3, '9th', 'Cengage', 2013, 4, 4),
('The Republic', 'Plato', '978-0140455113', 9, '1st', 'Penguin Classics', 2007, 2, 2);

-- Sample students
INSERT IGNORE INTO students (student_id, first_name, last_name, email, phone, department, class_name) VALUES
('STU001', 'Ahmed', 'Al-Rashid', 'ahmed@university.edu', '+1234567890', 'Computer Science', 'CS-301'),
('STU002', 'Sara', 'Mohammed', 'sara@university.edu', '+1234567891', 'Mathematics', 'MATH-201'),
('STU003', 'Omar', 'Hassan', 'omar@university.edu', '+1234567892', 'Engineering', 'ENG-401'),
('STU004', 'Fatima', 'Ali', 'fatima@university.edu', '+1234567893', 'Literature', 'LIT-101'),
('STU005', 'Yusuf', 'Ibrahim', 'yusuf@university.edu', '+1234567894', 'Science', 'SCI-202');
