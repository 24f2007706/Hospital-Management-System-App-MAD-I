from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
db=SQLAlchemy(app)

class Doctor(db.Model):


    doctor_id=db.Column(db.Integer(),primary_key=True)
    doctor_name=db.Column(db.String())
    doctor_username=db.Column(db.String(),unique=True)
    doctor_password=db.Column(db.String(),nullable=False)
    patient=db.relationship("Patient",backref="doctor")
    appointment=db.relationship('Appointment',backref="doctor")

class Patient(db.Model):

    patient_id=db.Column(db.Integer(),primary_key=True)
    patient_name=db.Column(db.String())
    patient_username=db.Column(db.String(),unique=True)
    patient_password=db.Column(db.String(),nullable=False)
    doctor_id=db.Column(db.Integer(),db.ForeignKey("doctor.doctor_id"))
    appointment=db.relationship('Appointment',backref="patient")

class Appointment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    patient_id=db.Column(db.Integer(),db.ForeignKey("patient.patient_id"))
    doctor_id=db.Column(db.Integer(),db.ForeignKey("doctor.doctor_id"))
    date=db.Column(db.Date(),nullable=False)
    time=db.Column(db.Time(),nullable=False)
    status=db.Column(db.String(),nullable=False)
    appointment_id=db.Column(db.Integer(),db.ForeignKey('treatment.appointment_id'))

class Treatment(db.Model):
    appointment_id=db.Column(db.Integer(),primary_key=True)
    diagnosis=db.Column(db.String(),nullable=False)
    prescription=db.Column(db.String(),nullable=False)
    notes=db.Column(db.String(),nullable=False)
    appointment=db.relationship('Appointment',backref='treatment')

class Department(db.Model):
    department_id=db.Column(db.Integer(),primary_key=True)
    department_name=db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=False)
    doctors_registered=db.Column(db.Integer(),nullable=False)

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