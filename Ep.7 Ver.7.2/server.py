from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///studentbd.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = b'dfgfbxvnkfbhkla'
db = SQLAlchemy()
db.init_app(app)

class Student(db.Model):
  sid = db.Column(db.String, primary_key=True)
  sname = db.Column(db.String, nullable=False)
  smobile = db.Column(db.String, nullable=False)
  sfaculty = db.Column(db.String, nullable=False)
  # simg = db.Column(db.String, nullable=True)
  

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
    
@app.route('/students/<sid>/delete',methods=['GET', 'POST'])
def delete_student(sid):
    student = Student.query.all()
    for s in student:
            if s.sid == sid:
              db.session.delete(s)
              db.session.commit()
              break
    return redirect(url_for('show_all_students'))

@app.route('/student/<sid>/update',methods=['GET','POST'])
def update_student(sid):
    students = Student.query.all()
    if request.method == 'POST':
        for s in students:
            if s.sid == sid:
                s.sname, s.smobile, s.sfaculty = request.form['sname'], request.form['smobile'], request.form['sfaculty']
                
                db.session.commit()
        return redirect(url_for('show_all_students'))
      
    std = None
    for s in students:
        if s.sid==sid:
          std = s
    return render_template('/student/update_student.html',std=std,title= 'update student')

@app.route('/student/show_all_studetns/search', methods=['POST'])
def search_student():
  if request.method == 'POST':
    students = Student.query.all()
    search = request.form['search']
    data = []
    t= None
    for s in students:
      if search.upper() in s.sname.upper() :
        data.append(s)
        t = 'search student'
      else:
        t = 'not found 400'
    
    return render_template('/student/show_all_students.html', students=data,title= t)


if __name__=='__main__':
  app.run(debug=True)