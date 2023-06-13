from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
database = 'blog.db'

@app.route('/')
def index():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT posts.id, title, content, username FROM posts INNER JOIN users ON posts.user_id = users.id')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/signup', methods=['GET, POSTS'])
def signup():
    #TODO: IMPLEMENT LOGIC
    return render_template('signup.html')

@app.route('/login', methods=['GET, POST'])
def login():
    # Implement user login logic
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Implement user logout logic
    return redirect('/')

@app.route('/create', methods=['GET', 'POST'])
def create():
    #Implement post creation logic
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
