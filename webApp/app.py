import numpy as np
import pandas as pd
from myProject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myProject.models import User
from myProject.forms import LoginForm, RegistrationForm
from myProject.extraction import GetData
from myProject.process import searchData
from werkzeug.security import generate_password_hash, check_password_hash


df = pd.read_csv("myProject/static/data_test_JAN24_2020.csv")
vals = df.values
# get specific values for each cell
data = []
for row in vals:
    strs = row[0].split('|')
    data.append(strs)
# generate a new dataframe
cols = df.columns.values[0].split('|')[1:]
cols.insert(0,"ID")
newDF = pd.DataFrame(data, columns=cols,index = None)





@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search',methods=['GET','POST'])
def search():

    return render_template('search.html')

@app.route('/getRes',methods=['POST'])
def getRes():
    choices = request.values.getlist("choices")
    result = searchData(newDF)(choices)
    numResult = result[0:5]
    dfResult = result[5]
    return render_template("showRes.html",numResult = numResult,dfResult = [dfResult.to_html(classes='data',formatters={'Name': lambda x: '<b>' + x + '</b>'})],titles = dfResult.columns.values)

@app.route("/downloadCSV",methods=['POST'])
@login_required
def downloadCSV():

    choices = request.values.getlist("choices")
    result = searchData(newDF)(choices)
    dfResult = result[5]
    return GetData(dfResult)()

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')


            next = url_for('search')
            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run()
