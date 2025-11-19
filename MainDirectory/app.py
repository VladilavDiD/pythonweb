from flask import Flask, render_template, redirect, url_for, request, session, flash
from users.db import init_db, create_user, verify_user

app = Flask(__name__)
app.secret_key = 'secret_key_random_string'  # Обов'язково для сесій!

# Запуск БД
init_db()


@app.route('/')
def index():
    # Якщо вже увійшов - перекидаємо в кабінет, якщо ні - показуємо Лендінг
    if 'username' in session:
        return redirect(url_for('user_home'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = verify_user(username, password)

        if user:
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('user_home'))
        else:
            flash('Невірний логін або пароль!', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if create_user(username, password):
            flash('Акаунт створено успішно! Тепер увійдіть.', 'success')
            # Оце перенаправлення точно спрацює
            return redirect(url_for('login'))
        else:
            flash('Користувач з таким логіном вже існує.', 'error')

    return render_template('register.html')


@app.route('/user_home')
def user_home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('user_home.html', username=session['username'])


@app.route('/admin_home')
def admin_home():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_home.html', username=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)