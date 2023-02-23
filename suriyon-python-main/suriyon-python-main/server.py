from ssl import ALERT_DESCRIPTION_INTERNAL_ERROR
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

my_contacts = [
    {'id': '01',
     'name': 'MOHAMED SALAH',
     'position': 'rw',
     'team': 'liverpool',
     'Personal_Information': 'Born June 15, 1992'},

    {'id': '02', 
	'name': 'Sadio Mané',
     'position': 'lw',
     'team': 'liverpool',
     'Personal_Information': 'born 10 April 1992'},

    {'id': '03',
     'name': 'Diogo José Teixeira da Silva',
     'position': 'cf',
     'team': 'liverpool',
     'Personal_Information': 'born 4 December 1996'},

    {'id': '04',
     'name': 'Jordan Brian Henderson MBE',
     'position': 'cm',
     'team': 'liverpool',
     'Personal_Information': 'born 17 June 1990'},

    {'id': '05',
     'name': 'Alexander Mark David Oxlade-Chamberlain',
     'position': 'cm',
     'team': 'liverpool',
     'Personal_Information': 'born 15 August 1993'},

    {'id': '06',
     'name': 'Fábio Henrique Tavares',
     'position': 'dm',
     'team': 'liverpool',
     'Personal_Information': 'born 23 October 1993'},

    {'id': '08',
     'name': 'Andrew Henry Robertson MBE',
     'position': 'lb',
     'team': 'liverpool',
     'Personal_Information': 'born 11 March 1994'},

    {'id': '09',
     'name': 'Virgil van Dijk',
     'position': 'cb',
     'team': 'liverpool',
     'Personal_Information': 'born 8 July 1991'},

    {'id': '10',
     'name': 'Job Joël André Matip ',
     'position': 'cb',
     'team': 'liverpool',
     'Personal_Information': 'born 8 August 1991'},

    {'id': '11',
     'name': 'Trent John Alexander-Arnold',
     'position': 'rb',
     'team': 'liverpool',
     'Personal_Information': 'born 7 October 1998'},

    {'id': '12',
     'name': 'Álisson Ramsés Becker',
     'position': 'gk',
     'team': 'liverpool',
     'Personal_Information': 'born 2 October 1992'},


]


@app.context_processor
def get_current_year():
    return {'date': datetime.utcnow()}


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html", contacts=my_contacts)


@app.route('/contacts/<id>/detail')
def contact_detail(id):
    friend = None
    for c in my_contacts:
        if c['id'] == id:
            friend = c
            break
    return render_template("detail.html", contacts=friend)


@app.route('/contacts/new_contact', methods=['GET', 'POST'])
def new_contact():
    if request.method == 'POST':
        contact = {'id': request.form['id'], 'name': request.form['name'], 'position': request.form['position'],
                   'team': request.form['team'], 'Personal_Information': request.form['Personal_Information']}
        if contact == my_contacts:
            my_contacts.append(contact)
        else:
            return render_template('error.html')
        return redirect(url_for('contacts'))
    return render_template('new_contact.html', title='New Contact')


@app.route('/contacts/<id>/update', methods=['GET', 'POST'])
def update_contact(id):
    if request.method == 'POST':
        for c in my_contacts:
            if c['id'] == id:
                c['name'], c['position'], c['team'], c['Personal_Information'] = request.form[
                    'name'], request.form['position'], request.form['team'], request.form['Personal_Information']
                break
        return redirect(url_for('contacts'))
    contact = None
    for c in my_contacts:
        if c['id'] == id:
            contact = c
            break
    return render_template('update_contact.html', contact=contact, title='Update Contact')


@app.route('/contacts/<id>/delete', methods=["GET", "POST"])
def delete_contact(id):
    for c in my_contacts:
        if c["id"] == id:
            my_contacts.remove(c)
            break
    return redirect(url_for("contacts"))


@app.route('/contacts/search', methods=["POST"])
def search_contact():
    search = request.form["search"]
    friend = []
    for c in my_contacts:
        if search.lower() in c["name"].lower():
            friend.append(c)
    return render_template('contacts.html', contacts=friend)


if __name__ == '__main__':

    app.run(debug=True)
