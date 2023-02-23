from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///studentbd.sqlite"
app.config['SECRET_KEY'] = b'dfgfbxvnkfbhkla'
db = SQLAlchemy()
db.init_app(app)



class Student(db.Model):
  
 # type: ignore  
  group = db.Column(db.String, nullable=False)
  name_team = db.Column(db.String, primary_key=True)
  race = db.Column(db.String, nullable=False)
  win = db.Column(db.String, nullable=False)
  draw = db.Column(db.String, nullable=False)
  lose = db.Column(db.String, nullable=False)
  gain = db.Column(db.String, nullable=False)
  broken = db.Column(db.String, nullable=False)
  different = db.Column(db.String, nullable=False)
  points = db.Column(db.String, nullable=False)
  #player



  # orm = object-rlational mapping
  def __str__(self):
    return self.race

@app.route('/')
def index():
    return render_template('world_football/index.html',title = 'world cup 2022')

@app.route('/wc2022')
def show_all_students():
    students = Student.query.all()
    return render_template('world_football/show_all_students.html',title = 'Show all 2022 World Cup teams', students=students)
  
@app.route('/wc2022/new_wc2022', methods=['GET','POST'])
def new_student():
    if request.method == 'POST':
      group = request.form['group']
      name_team = request.form['name_team']
      race = request.form['race']
      win = request.form['win']
      draw = request.form['draw']
      lose = request.form['lose']
      gain = request.form['gain']
      broken = request.form['broken']
      different = request.form['different']
      points = request.form['points']

      student = Student(name_team=name_team, race=race, win=win,draw=draw,lose=lose,gain=gain,broken=broken,different=different,points=points,group=group)
      db.session.add(student)
      db.session.commit()

      flash('Add New Student Successfully','success')
      return redirect(url_for('show_all_students'))
    return render_template('world_football/new_wc2022.html',title= 'add new student')
    
    
@app.route('/wc2022/<name_team>/delete',methods=['GET', 'POST'])
def delete_student(name_team):
    student = Student.query.all()
    for s in student:
            if s.name_team == name_team:
              db.session.delete(s)
              db.session.commit()
              break
    flash('Delete Student Successfully','.bg-danger')
    return redirect(url_for('show_all_students'))
  
  

@app.route('/world_football/<name_team>/update',methods=['GET','POST'])
def update_student(name_team):
    students = Student.query.all()
    if request.method == 'POST':
        for s in students:
            if s.name_team == name_team:
                s.race, s.win,s.draw,s.lose,s.gain,s.broken,s.different,s.points = request.form['race'], request.form['win'], request.form['draw'], request.form['lose'], request.form['gain'], request.form['broken'], request.form['different'], request.form['points']
                
                db.session.commit()
        flash('Update team foot ball Successfully','.bg-danger')  
        return redirect(url_for('show_all_students'))
      
    std = None
    for s in students:
        if s.name_team==name_team:
          std = s
    return render_template('/world_football/update_student.html',std=std,title= 'update student')
  
  
  
  
@app.route('/world_football/<name_team>/information',methods=['GET','POST'])
def information(name_team):
            
    students = Student.query.all()
    std = None
    for s in students:  
        if s.name_team==name_team:
          std = s
    return render_template('/world_football/information.html',std=std,title= 'INFORMATION')



@app.route('/world_football/show_all_wc2022/search', methods=['POST'])
def search_student():
  if request.method == 'POST':
    students = Student.query.all()
    search = request.form['search']
    data = []
    t= None
    for s in students:
      if search.upper() in s.name_team.upper() :
        data.append(s)
        t = 'search world football'
      else:
        t = 'not found'
    
    return render_template('/world_football/show_all_students.html', students=data,title= t)

if __name__=='__main__':
  app.run(debug=True)