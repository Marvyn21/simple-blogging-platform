from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_migrate import upgrade as db_upgrade
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect('/signup')

        new_user = User(username=username)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        flash('Sign up successful. Please log in.', 'success')
        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            session['user_id'] = user.id  # Store the user's session or token for authentication
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect('/login')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user's session or token
    return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = 'John'  # Replace with the actual author, either from the session or the currently logged-in user

        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')

    return render_template('create.html')


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/post/{}'.format(post_id))

    return render_template('edit_post.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db_upgrade()
        app.run(debug=True)