from flask import Flask
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



if __name__=="__main__":
    app.run(debug=True)