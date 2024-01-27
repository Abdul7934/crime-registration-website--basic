from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

users = [
    {'username': 'admin', 'password': generate_password_hash('admin')},
]

complaints = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        users.append({'username': username, 'password': hashed_password})
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        complaint_text = request.form['complaint']
        complaints.append({'username': session['username'], 'complaint': complaint_text})
        return render_template('complaint_success.html')

    return render_template('home.html')

@app.route('/complaint_status')
def complaint_status():
    return render_template('complaint_status.html', complaints=complaints)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
