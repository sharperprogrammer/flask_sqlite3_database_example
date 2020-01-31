from flask import Flask, render_template, request, g, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('databases/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    db = get_db()
    results = db.execute('SELECT id, name, location FROM users').fetchall()
    resultString = ''
    # for result in results:
    #     resultString += '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(result['id'], result['name'], result['location']);
    return render_template('users.html', results=results)

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('adduser.html')
    elif request.method == 'POST':
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('INSERT INTO users (name, location) VALUES (?, ?)', [name, location])
        db.commit()

        # return f'<h1 style="text-align = center;">Form submitted! Hello, {name}. From {location}</h1>'
        return redirect('/users')

@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        db = get_db();
        result = db.execute(f'SELECT * FROM users WHERE id={user_id}').fetchall()
        # return f'<h1>User ID: {result[0]["name"]}</h1>'
        return render_template('edituser.html', result=result[0])
    elif request.method == 'POST':
        name = request.form["name"]
        location = request.form["location"]
        db = get_db()
        # myString = 
        # return f'<h1>ID: {user_id}, Name: {name}, Location: {location}</h1>'
        db.execute(f'UPDATE users SET name = "{name}", location = "{location}" WHERE id = {user_id}')
        db.commit()
        return redirect('/users')

if __name__ == '__main__':
    app.run()