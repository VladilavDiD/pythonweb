from flask import Flask, render_template, redirect, url_for, request, session
from users.db import create_user, get_user_by_username
from werkzeug.security import check_password_hash
from users.db import init_db
init_db()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            error = "Користувач із таким логіном уже існує!"
        else:
            create_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html', error=error)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('main'))
        else:
            error = "Невірний логін або пароль"
    return render_template('login.html', error=error)

@app.route('/user_home')
def user_home():
    if session.get('role') == 'user':
        return render_template('user_home.html')
    return redirect(url_for('login'))

@app.route('/admin_home')
def admin_home():
    if session.get('role') == 'admin':
        return render_template('admin_home.html')
    return redirect(url_for('login'))

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)