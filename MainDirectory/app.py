from flask import Flask, render_template, redirect, url_for, request, session, flash
from users.db import init_db, create_user, verify_user, create_tournament, get_all_tournaments, join_tournament_db, get_user_tournaments
app = Flask(__name__)
app.secret_key = 'secret_key_random_string'

init_db()


@app.route('/')
def index():
    if 'username' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_home'))
        return redirect(url_for('user_home'))
    return render_template('index.html')


# ... (Login/Register/Logout залишаються без змін) ...
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = verify_user(request.form.get('username'), request.form.get('password'))
        if user:
            session['user_id'] = user['id']  # Зберігаємо ID для запису на турнір
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('admin_home' if user['role'] == 'admin' else 'user_home'))
        else:
            flash('Помилка входу', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if create_user(request.form.get('username'), request.form.get('password')):
            flash('Успішно! Увійдіть.', 'success')
            return redirect(url_for('login'))
        flash('Користувач існує', 'error')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# --- MVP ЛОГІКА ---

@app.route('/user_home')
def user_home():
    if 'username' not in session: return redirect(url_for('login'))
    # Показуємо список турнірів
    tournaments = get_all_tournaments()
    return render_template('user_home.html', username=session['username'], tournaments=tournaments)


@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    if session.get('role') != 'admin': return redirect(url_for('login'))

    if request.method == 'POST':
        # Створення турніру
        create_tournament(
            request.form.get('name'),
            request.form.get('game'),
            request.form.get('date'),
            request.form.get('description')
        )
        flash('Турнір створено!', 'success')

    return render_template('admin_home.html', username=session['username'])


@app.route('/join/<int:t_id>')
def join_tournament(t_id):
    if 'user_id' not in session: return redirect(url_for('login'))

    if join_tournament_db(session['user_id'], t_id):
        flash('Ви успішно зареєструвалися на турнір!', 'success')
    else:
        flash('Ви вже берете участь у цьому турнірі.', 'info')

    return redirect(url_for('user_home'))

@app.route('/my_tournaments')
def my_tournaments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    my_list = get_user_tournaments(session['user_id'])
    return render_template('my_tournaments.html', username=session['username'], tournaments=my_list)

if __name__ == '__main__':
    app.run(debug=True)