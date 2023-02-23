from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///stdsystem.sqlite'
db = SQLAlchemy()
db.init_app(app)

class Department(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  dname = db.Column(db.String(50), unique=True, nullable=False)
  students = db.relationship('Student', backref='department')

  def  __str__(self):
    return self.dname

class Student(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  sid = db.Column(db.String(11), unique=True, nullable=False)
  sname = db.Column(db.String(50), nullable=False)
  smobile = db.Column(db.String(12), unique=True, nullable=False)
  simage = db.Column(db.String(50), default='default.png')
  did = db.Column(db.Integer(), db.ForeignKey('department.id'))
  def  __str__(self):
    return self.sname
  

  @app.route('/')
  def index():
      return render_template('index.html', title='Home Page')
      

if __name__ == '__main__':
  app.run(debug=True)