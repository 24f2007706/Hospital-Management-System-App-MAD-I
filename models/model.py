from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Doctor(db.Model):
    doctor_id=db.Column(db.Integer(),primary_key=True)
    doctor_name=db.Column(db.String())
    doctor_username=db.Column(db.String(),unique=True)
    doctor_password=db.Column(db.String(),nullable=False)
    department_name=db.Column(db.String(),nullable=False)
    appointment=db.relationship('Appointment',backref='doctor')
    Availibility=db.relationship("Availibility",backref="doctor")
    treatmentdone=db.relationship("Treatment",backref="doctor")

class Patient(db.Model):
    patient_id=db.Column(db.Integer(),primary_key=True)
    patient_name=db.Column(db.String())
    patient_username=db.Column(db.String(),unique=True)
    patient_password=db.Column(db.String(),nullable=False)
    appointment=db.relationship('Appointment',backref='patient')
    treatment=db.relationship('Treatment',backref='patient')
    availablepatient=db.relationship("PAvailability",backref="patient")


class Appointment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    doctor_username=db.Column(db.String(),db.ForeignKey("doctor.doctor_username"))
    patient_username=db.Column(db.String(),db.ForeignKey("patient.patient_username"))
    date=db.Column(db.String(),nullable=False)
    time=db.Column(db.String(),nullable=False)

    
class Availibility(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    doctor_username=db.Column(db.String(),db.ForeignKey('doctor.doctor_username'))
    date1=db.Column(db.String(),nullable=False)
    date2=db.Column(db.String(),nullable=False)
    date3=db.Column(db.String(),nullable=False)
    date4=db.Column(db.String(),nullable=False)
    date5=db.Column(db.String(),nullable=False)
    date6=db.Column(db.String(),nullable=False)
    date7=db.Column(db.String(),nullable=False)
    morning1=db.Column(db.String(),nullable=False)
    morning2=db.Column(db.String(),nullable=False)
    morning3=db.Column(db.String(),nullable=False)
    morning4=db.Column(db.String(),nullable=False)
    morning5=db.Column(db.String(),nullable=False)
    morning6=db.Column(db.String(),nullable=False)
    morning7=db.Column(db.String(),nullable=False)

class PAvailability(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    patient_username=db.Column(db.String(),db.ForeignKey('patient.patient_username'))
    patientdate=db.Column(db.String(),nullable=False)
    patienttime=db.Column(db.String(),nullable=False)

class Treatment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    doctor_username=db.Column(db.String(),db.ForeignKey('doctor.doctor_username'))
    patient_username=db.Column(db.String(),db.ForeignKey('patient.patient_username'))
    dignosis=db.Column(db.String(),nullable=False)
    prescription=db.Column(db.String(),nullable=False)
    testdone=db.Column(db.String(),nullable=False)
