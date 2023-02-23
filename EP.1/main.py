from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    a = '<a href="/home">home</a>'
    return a
@app.route('/home')
def index2():
    link_home = '<a href="/">index</a>'
    input1 = '<input type="text">'
    a = "<h1>thawitchai</h1>"
    return link_home,a

if __name__ =='__main__':
    app.run(debug=True)