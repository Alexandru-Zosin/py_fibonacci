from flask import Blueprint, request, render_template, request, redirect, url_for, flash, make_response
from app.Model.user_model import db, User
from sqlalchemy import text

auth_bp = Blueprint('auth', __name__, template_folder='../View')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.authenticate(request.form['username'],
                                 request.form['password'])
        if user:
            resp = make_response(redirect(url_for('auth.dashboard')))
            # store actual username (not just user-{id})
            resp.set_cookie('username', user.username, httponly=True)
            return resp

        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required', 'warning')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('That username is taken', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful – please log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@auth_bp.route('/logout')
def logout():
    # Clear the 'username' cookie and redirect to login page
    resp = make_response(redirect(url_for('auth.login')))
    resp.delete_cookie('username')
    return resp


@auth_bp.route('/history')
def history():
    username = request.cookies.get('username', 'anonymous')

    # run a straight SQL query that returns exactly (endpoint, timestamp) tuples
    result = db.session.execute(text(
        """
        SELECT endpoint, timestamp
          FROM logs
         WHERE username = :username
      ORDER BY timestamp DESC
      FETCH FIRST 100 ROWS ONLY
        """),
        {"username": username}
    )
    records = result.fetchall()  # List[tuple(endpoint, datetime)]

    return render_template('history.html', logs=records)