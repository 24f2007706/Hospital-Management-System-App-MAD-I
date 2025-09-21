from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from models.model import *
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
db.init_app(app)

    
@app.route("/",methods=["GET","POST"])
def registration():
    if request.method=="POST":
        patient_name=request.form.get("PatientName")
        patient_username=request.form.get("PatientUsername")
        patient_password=request.form.get("PatientPassword")

        patient_details=Patient(patient_password=patient_password,patient_name=patient_name,patient_username=patient_username)
        patient_data=Patient.query.filter_by(patient_username=patient_username).first() 

        adminname=[1]
        if patient_name=="Admin" or patient_name=="admin" or patient_username=="admin@123" or patient_username=="Admin@123":
            return render_template("registration.html",adminname=adminname)
        
        alldata=[1]
        if patient_data and patient_data.patient_username==patient_username:
            return render_template("registration.html",alldata=alldata)
        
        emptyfield=[1]
        if len(patient_name)==0 or len(patient_username)==0 or len(patient_password)==0:
            return render_template("registration.html",emptyfield=emptyfield)

        db.session.add(patient_details)
        db.session.commit()
        return render_template("login.html")
    return render_template("registration.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("Username")
        password=request.form.get("Password")
        
        doctor_data=Doctor.query.filter_by(doctor_username=username).first()
        patient_data=Patient.query.filter_by(patient_username=username).first()

        if username=="Admin@123" and password=="Admin@123":
            return render_template("admin.html")
        
        emptyfield=[1]
        if len(username)==0 or len(password)==0:
            return render_template("login.html",emptyfield=emptyfield)

        if patient_data and username==patient_data.patient_username and password==patient_data.patient_password:
            return render_template("patient.html")
        
        if doctor_data and username==doctor_data.doctor_username and password==doctor_data.doctor_password:
            return render_template("doctor.html")
        
        alldata=[1]
        return render_template("login.html",alldata=alldata)
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)