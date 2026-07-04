import os
import logging
from flask import Flask, render_template_string, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-and-secure-key-12345'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'uploads'


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


logging.basicConfig(filename='website_errors.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VideoMetadataForm(FlaskForm):
    title = StringField('Video Title', validators=[DataRequired()])
    filename = StringField('Filename (as uploaded via FTP)', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Register Video')


BASE_HTML = 



@app.route('/')
def index():
    videos = Video.query.all()
    return render_template_string(BASE_HTML + , videos=videos)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! You can now login.')
            return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Registration error: {e}")
            flash('Username already exists.')
    return render_template_string(BASE_HTML + , form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password.')
    return render_template_string(BASE_HTML + , form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_video', methods=['GET', 'POST'])
@login_required
def add_video():
    form = VideoMetadataForm()
    if form.validate_on_submit():
        
        new_video = Video(title=form.title.data, filename=form.filename.data, description=form.description.data)
        db.session.add(new_video)
        db.session.commit()
        flash('Video metadata added successfully!')
        return redirect(url_for('index'))
    return render_template_string(BASE_HTML + , form=form)

@app.route('/watch/<int:video_id>')
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    return render_template_string(BASE_HTML + , video=video)

@app.route('/uploads/<filename>')
def serve_video(filename):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.errorhandler(404)
def not_found_error(error):
    return "This page does not exist.", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logging.error(f"Server Error: {error}")
    return "An internal server error occurred.", 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    
    app.run(debug=True)