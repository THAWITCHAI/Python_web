from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///studentbd.sqlite"
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
    return render_template('student/index.html', title='Home Page')


if __name__ == '__main__':
  app.run(debug=True)
