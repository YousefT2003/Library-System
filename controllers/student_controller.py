"""
Student Controller — Business logic for student operations.
"""

from flask import request, render_template, redirect, url_for, flash, jsonify
from models.student_model import StudentModel
from models.borrow_model import BorrowModel


class StudentController:

    @staticmethod
    def index():
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)

        students = StudentModel.get_all(search=search, page=page)
        total = StudentModel.count(search=search)

        # Flag students with overdue books
        for s in students:
            active = StudentModel.get_active_borrow_count(s['id'])
            s['active_borrows'] = active

        return render_template('students.html', students=students,
                               search=search, page=page, total=total, per_page=20)

    @staticmethod
    def create():
        data = {
            'student_id': request.form.get('student_id', '').strip(),
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'department': request.form.get('department', '').strip(),
            'class_name': request.form.get('class_name', '').strip(),
            'max_books': request.form.get('max_books', 3, type=int),
        }

        if not data['student_id'] or not data['first_name'] or not data['last_name']:
            flash('Student ID, first name, and last name are required.', 'error')
            return redirect(url_for('students.index'))

        # Check duplicate student ID
        existing = StudentModel.get_by_student_id(data['student_id'])
        if existing:
            flash('A student with this ID already exists.', 'error')
            return redirect(url_for('students.index'))

        StudentModel.create(data)
        flash('Student registered successfully!', 'success')
        return redirect(url_for('students.index'))

    @staticmethod
    def update(student_id):
        student = StudentModel.get_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('students.index'))

        data = {
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'department': request.form.get('department', '').strip(),
            'class_name': request.form.get('class_name', '').strip(),
            'max_books': request.form.get('max_books', 3, type=int),
        }

        StudentModel.update(student_id, data)
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.index'))

    @staticmethod
    def delete(student_id):
        StudentModel.delete(student_id)
        flash('Student deleted.', 'success')
        return redirect(url_for('students.index'))

    @staticmethod
    def history(student_id):
        student = StudentModel.get_by_id(student_id)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('students.index'))

        records = BorrowModel.get_student_history(student_id)
        return render_template('students.html', student=student, history=records, view='history')

    @staticmethod
    def api_search():
        search = request.args.get('q', '')
        students = StudentModel.get_all(search=search, per_page=10)
        return jsonify([{
            'id': s['id'], 'student_id': s['student_id'],
            'name': f"{s['first_name']} {s['last_name']}",
            'department': s['department']
        } for s in students])
