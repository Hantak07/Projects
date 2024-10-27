import os
from flask import Flask, render_template_string
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
path = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(path, 'database.sqlite3')
db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

def check_roll_no_exists(roll_no: str) -> bool:
    result = Student.query.where(Student.roll_number == roll_no).one_or_none()
    if result is None:
        return False
    else:
        return True

@app.route('/')
def index():
    students = Student.query.all()
    if len(students) == 0:
        return render_template("empty_index.html")
    else:
        return render_template("index.html", students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template("add_student.html")
    elif request.method == 'POST':
        """Extracting Form Data"""
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        checkbox = request.form.getlist("courses")
        print(first_name, last_name, checkbox)

        if check_roll_no_exists(roll_number):
            return render_template("student_exist.html")
        else:
            return render_template_string("testing")

@app.route("/student/<int:student_id>/update")
def update_student(student_id):
    return render_template_string("update_student page")

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    return render_template_string("delete_student page")

@app.route('/student/<int:student_id>', methods=['GET'])
def show_student(student_id):
    if request.method == 'GET':
        student = Student.query.filter_by(student_id=student_id).first()
        enrollments = Enrollments.query.filter_by(estudent_id=student_id)
        return render_template("student_page.html", student=student, enroll=enrollments)


if __name__=='__main__':
    app.run(debug=True)