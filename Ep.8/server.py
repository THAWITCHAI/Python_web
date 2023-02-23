from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///studentbd.sqlite"
app.config['SECRET_KEY'] = b'dfgfbxvnkfbhkla'
db = SQLAlchemy()
db.init_app(app)

class Student(db.Model):
  sid = db.Column(db.String, primary_key=True)
  sname = db.Column(db.String, nullable=False)
  smobile = db.Column(db.String, nullable=False)
  sfaculty = db.Column(db.String, nullable=False)

  # orm = object-rlational mapping
  def __str__(self):
    return self.sname


# web index
@app.route('/')
def index():
    return render_template('student/index.html',title = 'Home Page')


# show student
@app.route('/students')
def show_all_students():
    students = Student.query.all()
    return render_template('student/show_all_students.html',title = 'Show All Students', students=students)


# new student
@app.route('/students/new_student', methods=['GET','POST'])
def new_student():
    if request.method == 'POST':
      sid = request.form['sid']
      sname = request.form['sname']
      smobile = request.form['smobile']
      sfaculty = request.form['sfaculty']

      student = Student(sid=sid, sname=sname, smobile=smobile, sfaculty=sfaculty)
      db.session.add(student)
      db.session.commit()

      flash('Add New Student Successfully ','bg bg-success')
      return redirect(url_for('show_all_students'))
    return render_template('student/new_student.html',title= 'add new student')

# Update information
@app.route('/students/<sid>/update_student',methods=['GET','POST'])
def update_student(sid):
  # print(sid)
  student = Student.query.filter(Student.sid==sid).first()
  
  if request.method == 'POST':
      student.sname = request.form['sname']
      student.smobile = request.form['smobile']
      db.session.commit()
      flash('Update Student Successfully! ','bg bg-success')
      return redirect(url_for('show_all_students'))
  return render_template('/student/update_student.html',title = 'Update Student',student=student)
    

# Delete
@app.route('/students/<sid>/delete_student',methods=['GET','POST'])
def delete_student(sid):
    student = Student.query.filter(Student.sid==sid).first()
    db.session.delete(student)
    db.session.commit()
    flash('Delete Student Successfully! ','bg bg-success')
    return redirect(url_for('show_all_students'))


@app.route('/students/search_student', methods=['GET', 'POST'])
def search_student():
  if request.method == 'POST':
    search = request.form['search']
    search = '%{}%'.format(search)
    students = Student.query.filter(Student.sname.like(search))
    return render_template('student/show_all_students.html', title='Search Student', students=students)


if __name__=='__main__':
  app.run(debug=True)