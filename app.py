from flask import Flask, render_template, request, flash, redirect
import pickle
import numpy as np
from csv import reader
from PIL import Image
from tensorflow.keras.models import load_model
from flask import make_response
import pdfkit
import os
import predict as predict_

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


@app.route("/")
def home():
    return render_template('dataset.html')


@app.route("/datasetPage", methods=['GET', 'POST'])
def datasetPage():
    return render_template('dataset.html')


@app.route("/analysisPage", methods=['GET', 'POST'])
def analysisPage():
    return render_template('analysis.html')


@app.route("/accuraccyPage", methods=['GET', 'POST'])
def accuraccyPage():
    return render_template('accuraccy.html')


@app.route("/cancerPage", methods=['GET', 'POST'])
def cancerPage():
    return render_template('breastcancer.html')


import mysql.connector as con
import mysql

db = con.connect(
    host="localhost",
    user="root",
    password="",
    database="Breast_cancer"
)


def insert_data(name, email, mobile, age, gender, problem, pred):
    cur = db.cursor()
    cur.execute('INSERT INTO patient VALUES (NULL, %s, %s, %s,%s, %s,%s, %s)',
                (name, email, mobile, age, gender, problem, pred,))
    db.commit()
    return True


@app.route("/predictPage", methods=['POST', 'GET'])
def predictPage():
    try:
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        gender = request.form['gender']
        age = request.form['age']
        problem = request.form['problem']
        target = os.path.join(APP_ROOT, 'static/test/')
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file']
        namefile_ = 'test.jpg'
        destination = "/".join([target, namefile_])
        print(destination)
        file.save(destination)
        pred = 1
        # render_template_to_pdf('test.html', download=True, save=False, param='hello')
        pred = predict_.predict_cancer()
        insert_data(name, email, mobile, age, gender, problem, pred)

        return render_template('report.html', details=[name, email, mobile, age, gender, problem, pred])
    except Exception as ex:
        print(ex)
        message = "Please enter valid Data"
        return render_template("home.html", message=message)


@app.route("/report")
def report():
    filename = "receipt.pdf"
    pdf = pdfkit.from_file('templates/accuraccy.html', configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response


if __name__ == '__main__':
    app.run(debug=True)
