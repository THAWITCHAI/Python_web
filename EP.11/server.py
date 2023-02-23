from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stdsystem.sqlite'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)


class Department(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  dname = db.Column(db.String(50), unique=True, nullable=False)

  students = db.relationship('Student', backref='department', cascade='all, delete')

  def __str__(self):
    return self.dname

class Student(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  sid = db.Column(db.String(11), unique=True, nullable=False)
  sname = db.Column(db.String(50), nullable=False)
  smobile = db.Column(db.String(12), unique=True, nullable=False)
  simage = db.Column(db.String(50), default='default.png')
  did = db.Column(db.Integer(), db.ForeignKey('department.id'))

  def __str__(self):
    return self.sname

def save_image(img):
  random_hex = secrets.token_hex(8)
  fname, fext = os.path.splitext(img.filename)
  img_name = random_hex + fext
  img_path = os.path.join(app.root_path, 'static/img', img_name)

  img.save(img_path)

  return img_name

@app.route('/')
def index():
  return render_template('index.html', title='Home Page')

@app.route('/department/all_departments')
def all_departments():
    departments = Department.query.all()
    return render_template('department/all_departments.html',
    title='Show All Departments', departments=departments)

@app.route('/department/new_department', methods=['GET', 'POST'])
def new_department():
  if request.method == 'POST':
    dname = request.form['dname']
    department = Department(dname=dname)

    db.session.add(department)
    db.session.commit()

    return redirect(url_for('all_departments'))

  return render_template('department/new_department.html',
  title='Add New Department')

@app.route('/department/<int:id>/update_department', methods=['GET', 'POST'])
def update_department(id):
  department = Department.query.get(id)
  if request.method == 'POST':
    department.dname = request.form['dname']
    db.session.commit()
  
    return redirect(url_for('all_departments'))

  return render_template('department/update_department.html',
  title='Update Department', department=department)

@app.route('/department/<int:id>/delete_department', methods=['GET', 'POST'])
def delete_department(id):
  department = Department.query.get(id)
  
  db.session.delete(department)
  db.session.commit()
  
  return redirect(url_for('all_departments'))

@app.route('/student/all_students')
def all_students():
  students = Student.query.all()
  return render_template('student/all_students.html', 
  title='Show All Students', students=students)
  
@app.route('/student/new_student', methods=['GET', 'POST'])
def new_student():
  departments = Department.query.all()
  if request.method == 'POST':
    sid = request.form['sid']
    sname = request.form['sname']
    smobile = request.form['smobile']
    dep_id = request.form['dep_id']

    std_img = request.files['simage']

    if std_img:
      simage = save_image(std_img)
      student = Student(sid=sid, sname=sname, 
      smobile=smobile, simage=simage,  did=dep_id)
    else:
      student = Student(sid=sid, sname=sname, 
      smobile=smobile, did=dep_id)
    
    db.session.add(student)
    db.session.commit()

    return redirect(url_for('all_students'))

  return render_template('student/new_student.html', 
  title='Add New Student', departments=departments)
@app.route('/student/<int:id>/update_student', methods=['GET', 'POST'])
def update_student(id):
  student = Student.query.get(id)
  departments = Department.query.all()

  if request.method == 'POST':
    sname = request.form['sname']
    smobile = request.form['smobile']
    dep_id = request.form['dep_id']
    department = Department.query.get(dep_id)

    simage  = request.files['simage']
    if simage:
      fn = save_image(simage)
      student.simage = fn
    student.sname = sname
    student.smobile = smobile
    student.department = department 
    db.session.commit()

    return redirect(url_for('all_students'))


  return render_template('student/update_student.html',title='Update Student',student=student,departments=departments)

@app.route('/student/<int:id>/delete_student', methods=['GET', 'POST'])
def delete_student(id):
  student = Student.query.get(id)
  db.session.delete(student)
  db.session.commit()
  return redirect(url_for('all_students'))


# if __name__ == '__main__':
#   app.run(debug=True)


if __name__=='__main__':
    app.run(debug=True)