import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from models import db, User, Post, Media

# ─────────────────────────────────────────────
# APP CONFIG
# ─────────────────────────────────────────────
app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)
bcrypt = Bcrypt(app)

# ─────────────────────────────────────────────
# LOGIN MANAGER
# ─────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(
            request.form.get('password')
        ).decode('utf-8')

        user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))

    flash('Invalid credentials', 'danger')

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ─────────────────────────────────────────────
# POSTS
# ─────────────────────────────────────────────
@app.route('/posts')
@login_required
def posts():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('posts/list.html', posts=posts)


@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts'))

    return render_template('posts/create.html')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.updated_at = datetime.utcnow()

        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('posts/edit.html', post=post)


@app.route('/posts/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('posts'))


# ─────────────────────────────────────────────
# FILE UPLOAD (LOCAL)
# ─────────────────────────────────────────────
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(path)

            media = Media(
                filename=filename,
                s3_url=path,
                file_type=file.content_type,
                user_id=current_user.id
            )

            db.session.add(media)
            db.session.commit()

            flash('File uploaded!')

    return render_template('posts/upload.html')


@app.route('/media')
@login_required
def media():
    files = Media.query.filter_by(user_id=current_user.id).all()
    return render_template('posts/media.html', files=files)


# ─────────────────────────────────────────────
# ADMIN PANEL
# ─────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return "Access Denied"

    stats = {
        "total_users": User.query.count(),
        "total_posts": Post.query.count(),
        "total_media": Media.query.count()
    }

    return render_template('admin/dashboard.html', stats=stats)


@app.route('/admin/users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        return "Access Denied"

    users = User.query.all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:id>/toggle-role', methods=['POST'])
@login_required
def toggle_role(id):
    user = User.query.get(id)

    if user.role == 'user':
        user.role = 'admin'
    else:
        user.role = 'user'

    db.session.commit()
    return redirect(url_for('manage_users'))


# ─────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ─────────────────────────────────────────────
# RUN APP
# ─────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)