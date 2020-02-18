import numpy as np
import os
import pandas as pd
from myProject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myProject.models import User
from myProject.forms import LoginForm, RegistrationForm
from myProject.extraction import GetData
from myProject.process import searchData
from werkzeug.security import generate_password_hash, check_password_hash
#from werkzeug import secure_filename


#newDF = pd.read_csv("myProject/static/file/data.csv")
#newDF['template'] = newDF['template'].str.upper()
'''
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
'''





@app.route('/',methods=['GET','POST'])
def search():
    newDF = pd.read_csv("myProject/static/file/data.csv")
    newDF['template'] = newDF['template'].str.upper()
    possibleTemplates = sorted(list(set(newDF['template'].values)))

    return render_template('search.html',length = len(possibleTemplates),possibleTemplates=possibleTemplates)

@app.route('/getRes',methods=['POST'])
def getRes():
    newDF = pd.read_csv("myProject/static/file/data.csv")
    newDF['template'] = newDF['template'].str.upper()
    choices_t = request.values.getlist("choices")
    startDate = request.values.getlist("StartDate")[0]
    endDate = request.values.getlist("EndDate")[0]
    result = searchData(newDF)(choices_t,startDate,endDate)
    numResult = result[0:5]
    dfResult = result[5]
    dfDay = result[6]
    return render_template("showRes.html",choices_t = choices_t,startDate=startDate,endDate=endDate,numTemp = len(choices_t),
    numResult = numResult,dfResult = [dfResult.to_html(classes='data',formatters={'Name': lambda x: '<b>' + x + '</b>'})],
    dfDay = [dfDay.to_html(classes='data',formatters={'Name': lambda x: '<b>' + x + '</b>'})],
    titles = dfResult.columns.values)

@app.route("/downloadCSV",methods=['POST'])
def downloadCSV():
    newDF = pd.read_csv("myProject/static/file/data.csv")
    newDF['template'] = newDF['template'].str.upper()
    choices_t = request.values.getlist("choices")
    startDate = request.values.getlist("StartDate")[0]
    endDate = request.values.getlist("EndDate")[0]
    result = searchData(newDF)(choices_t,startDate,endDate)
    dfResult = result[5]
    return GetData(dfResult)()


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    #filename = secure_filename(file.filename)
    filename = "data.csv"
    file.save("myProject/static/file/"+filename)
    flash("Upload Success!")
    return redirect(url_for('search'))

@app.route('/test')
def test():
    return render_template('test.html');

if __name__ == '__main__':
    app.run(debug=True)
