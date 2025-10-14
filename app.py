from flask import Flask,request,render_template,redirect
from models.model import *


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/",methods=["GET","POST"])
def registration():
    if request.method=="POST":
        patient_name=request.form.get("PatientName")
        patient_username=request.form.get("PatientUsername")
        patient_password=request.form.get("PatientPassword")

        patient_details=Patient(patient_password=patient_password,patient_name=patient_name,patient_username=patient_username)
        patient_data=Patient.query.filter_by(patient_username=patient_username).first() 

        doctor_data=Doctor.query.filter_by(doctor_username=patient_username).first()
        adminname=[1]
        if patient_name=="Admin" or patient_name=="admin" or patient_username=="admin@123" or patient_username=="Admin@123":
            return render_template("registration.html",adminname=adminname)
        
        alldata=[1]
        if patient_data and patient_data.patient_username==patient_username:
            return render_template("registration.html",alldata=alldata)
        
        emptyfield=[1]
        if len(patient_name)==0 or len(patient_username)==0 or len(patient_password)==0:
            return render_template("registration.html",emptyfield=emptyfield)
        
        alreadyregistered=[1]
        if doctor_data:
            return render_template('registration.html',alreadyregistered=alreadyregistered)
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

        if username=="Admin123" and password=="Admin123":
            return render_template("admin.html")
        
        emptyfield=[1]
        if len(username)==0 or len(password)==0:
            return render_template("login.html",emptyfield=emptyfield)

        if patient_data and username==patient_data.patient_username and password==patient_data.patient_password:
            return render_template("patient.html",patient_data=patient_data)
        
        if doctor_data and username==doctor_data.doctor_username and password==doctor_data.doctor_password:
            return render_template("doctor.html",doctor_data=doctor_data)
        
        alldata=[1]
        return render_template("login.html",alldata=alldata)
    return render_template("login.html")


#ADMIN PAGE WORK HERE --


@app.route("/adddoctor",methods=["GET","POST"])
def adddoctor():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password=request.form.get("password")
        department=request.form.get("department")

        doctor_details=Doctor(doctor_name=name,doctor_username=username,doctor_password=password ,department_name=department)
        doctor_data=Doctor.query.filter_by(doctor_username=username).first()
        
        lenghtprob=[1]
        if len(username)==0 or len(password)==0 or len(department)==0 or len(name)==0:
            return render_template("adddoctor.html",lenghtprob=lenghtprob)
        
        reg_doc=[1]
        if doctor_data and doctor_details.doctor_username==username:
            return render_template("adddoctor.html",reg_doc=reg_doc)
        
        db.session.add(doctor_details)
        db.session.commit()
        return render_template("admin.html")

    return render_template("adddoctor.html")

@app.route("/doctorregistered",methods=["GET","POST"])
def doctorregistered():
    doctor_data=Doctor.query.all()
    if doctor_data :
        return render_template("doctorregistered.html",doctor_data=doctor_data)
    else:
        nodata=[1]
        return render_template("doctorregistered.html",nodata=nodata)
    
@app.route("/deletedoctor/<int:doctor_id>")
def deletedoctor(doctor_id):
    doctor_data=Doctor.query.filter_by(doctor_id=doctor_id).first()
    db.session.delete(doctor_data)
    db.session.commit()
    return redirect("/doctorregistered")

@app.route("/updatedoctor/<int:doctor_id>",methods=["GET","POST"])
def updatedoctor(doctor_id):
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password= request.form.get("password")
        department= request.form.get("department")

        doctor_data=Doctor.query.filter_by(doctor_id=doctor_id).first()
        doctor_data.doctor_name=name 
        doctor_data.doctor_username=username
        doctor_data.doctor_password=password 
        doctor_data.department_name=department 

        db.session.add(doctor_data)
        db.session.commit()
        return redirect("/doctorregistered")
    
    doctor_data=Doctor.query.filter_by(doctor_id=doctor_id).first()
    return render_template("updatedoctor.html",doctor_data=doctor_data)

@app.route("/patientregistered",methods=["GET","POST"])
def patientregistered():
    patient_data=Patient.query.all()
    if patient_data :
        return render_template("patientregistered.html",patient_data=patient_data)
    else:
        nodata=[1]
        return render_template("patientregistered.html",nodata=nodata)

@app.route("/deletepatient/<int:patient_id>")
def deletepatient(patient_id):
    patient_data=Patient.query.filter_by(patient_id=patient_id).first()
    db.session.delete(patient_data)
    db.session.commit()
    return redirect("/patientregistered")


@app.route("/updatepatient/<int:patient_id>",methods=["GET","POST"])
def updatepatient(patient_id):
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password= request.form.get("password")
        department= request.form.get("department")

        patient_data=Patient.query.filter_by(patient_id=patient_id).first()
        patient_data.patient_name=name 
        patient_data.patient_username=username
        patient_data.patient_password=password 
        patient_data.patient_department=department 

        db.session.add(patient_data)
        db.session.commit()
        return redirect("/patientregistered")
    
    patient_data=Patient.query.filter_by(patient_id=patient_id).first()
    return render_template("updatepatient.html",patient_data=patient_data)


@app.route('/allappointments')
def allappointments():
    appointment=Appointment.query.all()
    if appointment :
        return render_template("allappointments.html",appointment=appointment)
    else:
        nodata=[1]
        return render_template("allappointments.html",nodata=nodata)

# SEARCH FUNCTIONALITY (DOTOR SEARCH AND PATIENT SEARCH)
@app.route('/doctorsearch',methods=["GET","POST"])
def doctorsearch():
    if request.method=="POST":
        searched=request.form.get("searched")
        doctor_data=Doctor.query.filter_by(doctor_name=searched).all()
        if doctor_data:
            return render_template("doctorsearch.html",doctor_data=doctor_data)
        nodata=[1]
        return render_template("doctorsearch.html",nodata=nodata)
    return render_template('doctorregistered.html')

@app.route('/patientsearch',methods=["GET","POST"])
def patientsearch():
    if request.method=="POST":
        searched=request.form.get("searched")
        patient_data=Patient.query.filter_by(patient_name=searched).all()
        if patient_data:
            return render_template("patientsearch.html",patient_data=patient_data)
        nodata=[1]
        return render_template("patientsearch.html",nodata=nodata)
    return render_template('patientregistered.html')

@app.route('/appointmentsearch',methods=["GET","POST"])
def appointmentsearch():
    if request.method=="POST":
        searched=request.form.get("searched")
        appointment=Appointment.query.filter_by(doctor_username=searched).all()
        if appointment:
            return render_template('appointmentsearch.html',appointment=appointment)
        nodata=[1]
        return render_template("appointmentsearch.html",nodata=nodata)
    return render_template('allappointments.html')
    

#DOCTOR PAGE started--

@app.route("/provideavailability/<doctor_username>")
def avalibility(doctor_username):
    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
    return render_template("provideavailability.html",doctor_data=doctor_data)

@app.route('/doctoravailable/<doctor_username>',methods=["GET","POST"])
def doctordateandtime(doctor_username):
    if request.method=="POST":
        date1=request.form.get("date1")
        date2=request.form.get("date2")
        date3=request.form.get("date3")
        date4=request.form.get("date4")
        date5=request.form.get("date5")
        date6=request.form.get("date6")
        date7=request.form.get("date7")

        morning1=request.form.get("morning1")
        morning2=request.form.get("morning2")
        morning3=request.form.get("morning3")
        morning4=request.form.get("morning4")
        morning5=request.form.get("morning5")
        morning6=request.form.get("morning6")
        morning7=request.form.get("morning7")

        doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()

        available_data=Availibility(doctor_username=doctor_username,date1=date1,date2=date2,date3=date3,date4=date4,date5=date5,date6=date6,date7=date7,morning1=morning1,morning2=morning2,morning3=morning3,morning4=morning4,morning5=morning5,morning6=morning6,morning7=morning7)
        doctor_availability=Availibility.query.filter_by(doctor_username=doctor_username).first()
        
        lenzero=[1]
        if len(date1)==0 or len(date2)==0 or len(date3)==0 or len(date4)==0 or len(date5)==0 or len(date6)==0 or len(date7)==0 or len(morning1)==0 or len(morning2)==0 or len(morning3)==0 or len(morning4)==0 or len(morning5)==0 or len(morning6)==0 or len(morning7)==0 :
            return render_template('provideavailability.html',lenzero=lenzero,doctor_data=doctor_data)
        havedata=[1]
        if doctor_availability:
            return render_template('provideavailability.html',havedata=havedata,doctor_data=doctor_data)

        db.session.add(available_data)
        db.session.commit()
        return render_template("doctor.html",doctor_data=doctor_data)
    return render_template("provideavailability.html")


@app.route("/viewavailability/<doctor_username>")
def viewavailability(doctor_username):

    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
    available_data=Availibility.query.filter_by(doctor_username=doctor_username).first()

    if available_data:
        return render_template('viewavailability.html',available_data=available_data,doctor_data=doctor_data)
    else:
        nodata=[1]
        return render_template("viewavailability.html",nodata=nodata,available_data=available_data,doctor_data=doctor_data)


@app.route("/deleteavailability/<doctor_username>",methods=["GET","POST"])
def deleteavailability(doctor_username):
    available_data=Availibility.query.filter_by(doctor_username=doctor_username).first()
    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()

    if request.method=="POST" and available_data and doctor_username!="":
        db.session.delete(available_data)
        db.session.commit()
        return render_template("doctor.html",doctor_data=doctor_data)
    return render_template("doctor.html",doctor_data=doctor_data)

@app.route("/uadoctor/<doctor_username>" ,methods=["GET","POST"])
def uadoctor(doctor_username):
    appointment=Appointment.query.all()
    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
    nodata=[1]
    if request.method=="POST":
        appointment=Appointment.query.all()
        doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
        if appointment:
            return render_template("uadoctor.html",appointment=appointment,doctor_data=doctor_data,nodata=nodata)
    return render_template("uadoctor.html",appointment=appointment,doctor_data=doctor_data)

@app.route("/canceluadoctor/<int:id>")
def canceluadoctor(id,):
    appointment=Appointment.query.filter_by(id=id).first()
    doctor_data=Doctor.query.filter_by(doctor_username=appointment.doctor_username).first()
    db.session.delete(appointment)
    db.session.commit()
    return render_template("doctor.html",doctor_data=doctor_data)

@app.route("/updatehistory/<int:id>",methods=["GET","POST"])
def updateaptienthistory(id):
    doctor_data=Doctor.query.filter_by(doctor_id=id).first()
    patient_data=Appointment.query.filter_by(id=id).first()
    if request.method=="POST":
        patient_data=Appointment.query.filter_by(id=id).first()
        patient_username=patient_data.patient_username
        doctor_username=patient_data.doctor_username
        dignosis=request.form.get("dignosis")
        prescription=request.form.get("prescription")
        testdone=request.form.get("testdone")

        treatments=Treatment(doctor_username=doctor_username,dignosis=dignosis,prescription=prescription,testdone=testdone,patient_username=patient_username)

        db.session.add(treatments)
        db.session.commit()
        done=[1]
        return render_template("updatehistory.html",patient_data=patient_data,doctor_data=doctor_data,done=done)
    return render_template("updatehistory.html",patient_data=patient_data,doctor_data=doctor_data)

@app.route("/complete/<doctor_username>",methods=["GET","POST"])
def markascomplete(doctor_username):
    if request.method=="GET":
        appointment=Appointment.query.filter_by(doctor_username=doctor_username).first()
        doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
        return render_template("doctor.html",doctor_data=doctor_data)
    return render_template("doctor.html",doctor_data=doctor_data)

@app.route("/assignedpatient/<doctor_username>")
def assignedpatient(doctor_username):
    appointments=Appointment.query.all()
    appointment=Appointment.query.filter_by(doctor_username=doctor_username).first()
    error=[1]
    if appointment:
        return render_template("assignedpatient.html",appointments=appointments)
    return render_template("assignedpatient.html",error=error)


#PATIENT PAGE started ...

@app.route('/departments')
def departments():
    return render_template('departments.html')

@app.route('/surgery')
def surgery():
    doctor_data=Doctor.query.filter_by(department_name="Surgery").all()
    if doctor_data:
        return render_template('surgery.html',doctor_data=doctor_data)
    return render_template("surgery.html",doctor_data=doctor_data)

@app.route('/general')
def general():
    doctor_data=Doctor.query.filter_by(department_name="General").all()
    if doctor_data:
        return render_template('general.html',doctor_data=doctor_data)
    return render_template("general.html",doctor_data=doctor_data)

@app.route('/cardiology')
def cardiology():
    doctor_data=Doctor.query.filter_by(department_name="Cardiology").all()
    if doctor_data:
        return render_template('cardiology.html',doctor_data=doctor_data)
    return render_template("cardiology.html",doctor_data=doctor_data)

@app.route('/oncology')
def oncology():
    doctor_data=Doctor.query.filter_by(department_name="Oncology").all()
    if doctor_data:
        return render_template('oncology.html',doctor_data=doctor_data)
    return render_template("oncology.html",doctor_data=doctor_data)


@app.route('/viewdetails/<doctor_username>')
def viewdetails(doctor_username):
    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
    return render_template('viewdetails.html',doctor_data=doctor_data)

@app.route('/checkavailability/<doctor_username>',methods=["GET","POST"])
def checkavailability(doctor_username):
    doctor_data=Doctor.query.filter_by(doctor_username=doctor_username).first()
    available_data=Availibility.query.filter_by(doctor_username=doctor_username).first()
    if request.method=="POST":

        patientdate=request.form.get("patientdate")
        patienttime=request.form.get("patienttime")
        patientusername=request.form.get("patientusername")
        patient_data=PAvailability(patient_username=patientusername,patientdate=patientdate,patienttime=patienttime)

        appointmentissue=[1]
        if(patient_data.patienttime==available_data.morning1 or patient_data.patienttime==available_data.morning2 or patient_data.patienttime==available_data.morning3 or patient_data.patienttime==available_data.morning4 or patient_data.patienttime==available_data.morning5 or patient_data.patienttime==available_data.morning6 or patient_data.patienttime==available_data.morning7 )and (patient_data.patientdate==available_data.date1 or patient_data.patientdate==available_data.date2 or patient_data.patientdate==available_data.date3 or patient_data.patientdate==available_data.date4 or patient_data.patientdate==available_data.date5 or patient_data.patientdate==available_data.date6 or patient_data.patientdate==available_data.date7):

            appointment_data=Appointment(doctor_username=doctor_username,patient_username=patientusername,date=patientdate,time=patienttime)
            db.session.add(appointment_data)
            db.session.commit()
            return render_template("patient.html",patient_data=patient_data)
        return render_template('checkavailability.html',doctor_data=doctor_data,available_data=available_data,appointmentissue=appointmentissue)
        
    if available_data:
        return render_template('checkavailability.html',available_data=available_data,doctor_data=doctor_data)

    else:
        nodata=[1]
        return render_template('checkavailability.html',available_data=available_data,nodata=nodata,doctor_data=doctor_data)

@app.route("/upcommingappointments/<patient_username>")
def uppcommingappointments(patient_username):
    patient_data=Patient.query.filter_by(patient_username=patient_username).first()
    appointment=Appointment.query.all()
    appointments=Appointment.query.filter_by(patient_username=patient_username).all()
    empty=[1]
    if appointments:
        return render_template("upcommingappointments.html",appointment=appointment,patient_data=patient_data)
    return render_template("upcommingappointments.html",empty=empty)

@app.route("/cancelappointment/<int:id>")
def cancelappointment(id):
    appointment=Appointment.query.filter_by(id=id).first()
    db.session.delete(appointment)
    db.session.commit()
    return redirect("/upcommingappointments")

@app.route('/editpatient/<patient_username>',methods=["GET","POST"])
def editpatient(patient_username):

    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password= request.form.get("password")

        patient_data=Patient.query.filter_by(patient_username=username).first()
        patient_data.patient_name=name 
        patient_data.patient_username=username
        patient_data.patient_password=password 

        db.session.add(patient_data)
        db.session.commit()

        changed=[1]
        return render_template("editpatient.html",patient_data=patient_data,changed=changed)
    
    patient_data=Patient.query.filter_by(patient_username=patient_username).first()
    return render_template("editpatient.html",patient_data=patient_data)

@app.route("/patienthistory/<patient_username>")
def patienthistory(patient_username):
    patient_data=Patient.query.filter_by(patient_username=patient_username).first()
    treatment=Treatment.query.filter_by(patient_username=patient_username).all()
    if treatment:
        return render_template("patienthistory.html",patient_data=patient_data,treatment=treatment)
    error=[1]
    return render_template('patienthistory.html',error=error)

#PATIENT WORK DONE.
#DOCTOR WORK DONE.
#ADMIN WORK DONE.

if __name__=="__main__":
    app.run(debug=True)