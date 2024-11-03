import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'asss' 
user_id=0
# Initialize the database
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS drivers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            driver_name TEXT NOT NULL,
                            driver_image TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )''')
        conn.commit()

# Route to display the login form
@app.route('/')
def home():
    return render_template('login.html')  # Ensure login.html is inside the templates folder

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Insert user data into the database
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            
            conn.commit()
            return render_template('home.html')  
    except sqlite3.IntegrityError:
        return "Error: User with this email already exists!"

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']

    # Check user credentials
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        return render_template('home.html')  # Render home.html after successful login
    else:
        return render_template('login.html', error="Invalid email or password.")




@app.route('/register')
def register():
    return render_template('registration.html') 




@app.route('/register_driver', methods=['POST'])

def register_driver():
    driver_name = request.form['driver_name']
    driver_image = request.files['driver_image']
    
    # Save the image to the server (you may want to adjust the path)
    image_path = f'static/images/{driver_image.filename}'
    driver_image.save(image_path)

   
    user_id = session.get('user_id')

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO drivers (user_id, driver_name, driver_image) VALUES (?, ?, ?)',
                       (user_id, driver_name, image_path))
        conn.commit()

    return render_template('home.html')
if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
