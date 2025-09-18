from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
db=SQLAlchemy(app)

class Doctor(db.Model):
    doctor_name=db.Column(db.String())
    doctor_username=db.Column(db.String(),primary_key=True)
    doctor_password=db.Column(db.String(),nullable=False)

class Patient(db.Model):
    patient_name=db.Column(db.String())
    patient_username=db.Column(db.String(),primary_key=True)
    patient_password=db.Column(db.String(),nullable=False)

class Treatment(db.Model):

class Appointment(db.Model):

if __name__=="__main__":
    app.run(debug=True)