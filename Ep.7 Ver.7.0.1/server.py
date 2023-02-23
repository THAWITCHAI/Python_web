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

@app.route('/')
def index():
    return render_template('student/index.html',title = 'Home Page')

@app.route('/students')
def show_all_students():
    students = Student.query.all()
    return render_template('student/show_all_students.html',title = 'Show All Students', students=students)
  
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

      flash('Add New Student Successfully','success')
      return redirect(url_for('show_all_students'))
    return render_template('student/new_student.html',title= 'add new student')
    

if __name__=='__main__':
  app.run(debug=True)