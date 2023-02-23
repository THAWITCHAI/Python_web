from flask import Flask,render_template
app = Flask(__name__)

my_contact = [
  {'id':'64122420210','name':'Nayhoitamin','mobile':'0652974104'},
  {'id':'64122420209','name':'Aun Tony','mobile':'0921911669'},
  {'id':'64122420207','name':'Tat onetat','mobile':'0921111541'},
  {'id':'64122420204','name':'Phubouwan','mobile':'0835157887'},
  {'id':'64122420209','name':'Phujoi','mobile':'0625457888'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html',contacts=my_contact)

@app.route('/contacts/<id>/detail')
def contact_detail(id):
  friend = None
  for c in my_contact:
    if c['id'] == id:
      friend =c
      break
  return render_template('detail.html',contact=friend)

if __name__=="__main__":
  app.run(debug=True)