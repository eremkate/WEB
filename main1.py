from flask import Flask
from flask import render_template, request, redirect, abort
import psycopg2
from psycopg2 import OperationalError


def connection(name, user, password, host, port):
    conn = None
    try:
        conn = psycopg2.connect(
        database=name,
        user=user,
        password=password,
        host=host,
        port=port,
        )
        print('Connected to database')
    except OperationalError:
        print('an operating error has occurred')
    return conn

connection('phonebook', 'postgres', '1br3485a', '127.0.0.1', '5432')

def insert(name, surname, city, phone_number):
    conn = connection('phonebook', 'postgres', '1br3485a', '127.0.0.1', '5432')
    insert = (f"INSERT INTO users (name, surname, telephone, age) "
              f"VALUES ('{name}', '{surname}', '{city}', '{phone_number}')")
    cursor = conn.cursor()
    cursor.execute(insert)
    conn.commit()

def listing():
    conn = connection('phonebook', 'postgres', '1br3485a', '127.0.0.1', '5432')
    cursor = conn.cursor()
    result = None
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    total = []
    for user in result:
        user = list(user)
        total1 = []
        for val in user:
            total1.append(val.strip())
        total.append(total1)
        listing = []
    for val in total:
        listing.append(
            {'username': val[0] + val[1], 'name': val[0], 'surname': val[1], 'city': val[2], 'phone_number': val[3]})
    return listing


def checking(value):
    conn = connection('phonebook', 'postgres', '1br3485a', '127.0.0.1', '5432')
    cursor = conn.cursor()
    result = None
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    total = []
    for user in result:
        user = list(user)
        total1 = []
        for val in user:
            total1.append(val.strip())
        total.append(total1)
    for st in total:
        if ' '.join(st) == value:
            return True
    return False

app = Flask(__name__)

@app.route('/', methods=['get'])
def index():
    return redirect('http://127.0.0.1:5000/users')

@app.route('/users', methods=['get', 'post'])
def users():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        city = request.form.get('city')
        phone_number = request.form.get('phone_number')
        if not checking(f'{name} {surname} {city} {phone_number}'):
            insert(name, surname, city, phone_number)
    return render_template('users.html', users=listing())

@app.route('/users/<username>')
def check(username):
    users = ''
    flag = []
    for i in listing():
        if username != i['username']:
            flag.append(False)
        else:
            flag.append(True)
    if any(flag) == False:
        abort(404)
    for i in listing():
        if username == i['username']:
            users = i
    return f'<h2>UserName:{users["username"]} </h2> <br>'\
           f'<h2>Name:{users["name"]} </h2> <br>'\
           f'<h2> Surname:{users["surname"]} </h2> <br>' \
           f'<h2>City:{users["city"]} </h2> <br>' \
           f'<h2>Phone_number:{users["phone_number"]} </h2> <br>'\

if __name__ == '__main__':
    app.run(debug=True)