from operator import methodcaller
from django.shortcuts import render
from flask import Flask, flash,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager, login_required,logout_user,current_user 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='project'
db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)


class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder": "Username"})

    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder": "Password"})

    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        u=User.query.filter_by(username=username.data).first()
        
        if u:
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder": "Username"})

    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder": "Password"})

    submit=SubmitField('Sign Up')



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html',form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/previous-year-records',methods=['GET','POST'])
@login_required
def previous_year_records():
    return render_template('previous.html')

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    return redirect(url_for('login'))

@app.route('/placement',methods=['GET','POST'])
@login_required
def placements():
    return render_template('placement.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    def v(username):
        u=User.query.filter_by(username=username.data).first()
        if u:
            return False
        return True
    if not v(form.username):
        return "Username already taken"
    if form.validate_on_submit():
        new_user=User(username=form.username.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

if(__name__=='__main__'):
    app.run(debug=True)

