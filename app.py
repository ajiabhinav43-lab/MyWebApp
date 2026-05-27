import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from config import DevelopmentConfig
from models import db, User, Post, Like, Comment

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# HOME
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid credentials', 'danger')

    return render_template('auth/login.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# CREATE POST
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        file = request.files.get('file')

        image_path = None
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join('static/uploads', filename)
            os.makedirs('static/uploads', exist_ok=True)
            file.save(path)
            image_path = '/' + path

        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            image=image_path,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('posts/create.html')


# LIKE ❤️
@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if not existing:
        db.session.add(Like(user_id=current_user.id, post_id=post_id))
        db.session.commit()

    return redirect(url_for('index'))


# COMMENT 💬
@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form.get('content')

    if content:
        new_comment = Comment(
            content=content,
            user_id=current_user.id,
            post_id=post_id
        )

        db.session.add(new_comment)
        db.session.commit()

    return redirect(url_for('index'))


# DELETE COMMENT
@app.route('/delete-comment/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)

    if comment.user_id != current_user.id:
        return "Unauthorized"

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('index'))


# PROFILE
@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template('profile.html', user=user, posts=posts)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
