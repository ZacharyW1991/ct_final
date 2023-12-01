from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, KanjiSearchForm
from app.models import User
import requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignUpForm()
    if form.validate_on_submit():
        print('validated')
        username=form.username.data
        password=form.password.data

        check_user=db.session.execute(db.select(User).where( (User.username==username))).scalars().all()
        if check_user:
            flash('A user with that username already exists')
            return redirect(url_for('signup'))
        new_user=User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash(f"{new_user.username} has been created!")

        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user=db.session.execute(db.select(User).where(User.username==username)).scalar()

        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} has successfully logged in.")
            return redirect(url_for('login'))
        else:
            flash('Incorrect username and/or password')
            return redirect(url_for('favorites'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.route('/search')
def search_kanji():

    return render_template('search.html')

@app.route('/favorite/<character>')
@login_required
def favorite_kanji(character):

    headers = {
	"X-RapidAPI-Key": "4c9fcfd817msh939e3bd498d9e5ap164e4fjsn8ff062b62217",
	"X-RapidAPI-Host": "kanjialive-api.p.rapidapi.com"
    }
    
    response=requests.get(f'https://kanjialive-api.p.rapidapi.com/api/public/kanji/{character}', headers=headers)

    data=response.json()
    print(data)
    current_faves=eval(current_user.favorites)
    current_faves.append(data)
    current_user.favorites=str(current_faves)
    db.session.commit()
    return render_template('search.html')

@app.route('/delete-kanji/<character>')
@login_required
def delete_kanji(character):

    headers = {
	"X-RapidAPI-Key": "4c9fcfd817msh939e3bd498d9e5ap164e4fjsn8ff062b62217",
	"X-RapidAPI-Host": "kanjialive-api.p.rapidapi.com"
    }

    response=requests.get(f'https://kanjialive-api.p.rapidapi.com/api/public/kanji/{character}', headers=headers)
    data=response.json()

    # def del_filter(kanji):
    #     if kanji==data:
    #         return False
    #     else:
    #         return True
        
    current_faves=eval(current_user.favorites)
    current_faves.remove(data)
    # current_faves2=filter(lambda k:k!=data, current_faves)
    current_user.favorites=str(current_faves)
    db.session.commit()
    return render_template('index.html')



@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/favorites')
@login_required
def favorites():
    e_fave=eval(current_user.favorites)
    return render_template('favorites.html', e_fave=e_fave)