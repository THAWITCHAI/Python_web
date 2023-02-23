from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

my_contacts = [
  {'id':'1', 'name':'Netherland', 'mobile':'Europe'},
  {'id':'2', 'name':'Argentina', 'mobile':'South America'},
  {'id':'3', 'name':'Croatia', 'mobile':'Europe'},
  {'id':'4', 'name':'Brazil', 'mobile':'South America'},
  {'id':'5', 'name':'England', 'mobile':'Europe'},
  {'id':'6', 'name':'France', 'mobile':'Europe'},
  {'id':'7', 'name':'Morocco', 'mobile':'Africa'},
  {'id':'8', 'name':'Portugat', 'mobile':'Europe'},
]

@app.context_processor
def get_curen_year():
  return {'date':datetime.utcnow()}

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/contacts')
def contacts():
  return render_template('contacts.html', contacts=my_contacts)

@app.route('/contacts/<id>/detail')
def contact_detail(id): 
  friend = None
  for c in my_contacts:
    if c['id'] == id:
     friend = c
     break
  return render_template('detail.html', contact=friend)  

@app.route('/contacts/new_contact', methods=['GET', 'POST'])
def new_contact():
  if request.method == 'POST':
    id = request.form['id']
    name = request.form['name']
    mobile = request.form['mobile']
    #print(id, name, mobile)
    contact = {'id':id, 'name':name, 'mobile':mobile}

    my_contacts.append(contact)
    return redirect(url_for('contacts'))

  return render_template('new_contacts.html', title='New Contact')

@app.route('/contact/<id>/update', methods=['GET','POST'])
def update_contact(id):
  if request.method == 'Post':
    for c in my_contacts:
      if c['id'] == id:
        c['name'] = request.form['name']
        c['mobile'] = request.form['mobile']
        break

    return redirect(url_for('contacts'))

  contact = None
  for c in my_contacts:
    if c['id'] == id:
     contact = c
     break
  return render_template('update_contacts.html',contact=contact, title='Update Contact')

@app.route('/contact/<id>/deltet')
def delete_contact(id):
  for c in my_contacts:
    if c['id'] == id:
      my_contacts.remove(c)
      break

  return redirect(url_for('contacts')) 

@app.route('/contact/search', methods=['POST'])
def search_contact():
  if request.method == 'POST':
    search = request.form['search']
    friends = []
    for c in my_contacts:
      if search.upper() in c['name'].upper():
        friends.append(c)
    
    return render_template('contacts.html', contacts=friends)


if __name__ == '__main__':
  app.run(debug=True)