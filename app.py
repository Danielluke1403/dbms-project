from flask import Flask, render_template, request, redirect, url_for
from db_config import connect_db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_clinic', methods=['GET', 'POST'])
def add_clinic():
    if request.method == 'POST':
        location = request.form['location']
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO clinic (location) VALUES (%s)", (location,))
        conn.commit()
        conn.close()
        return redirect(url_for('show_clinics'))
    return render_template('add_clinic.html')

@app.route('/clinics')
def show_clinics():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clinic")
    clinics = cur.fetchall()
    conn.close()
    return render_template('show_clinics.html', clinics=clinics)
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    conn = connect_db()
    cur = conn.cursor()
    if request.method == 'POST':
        doc_id=request.form["doc_id"]
        name = request.form['name']
        specialization = request.form['specialization']
        phone = request.form['phone_no']
        clinic_id = request.form['clinic_id']
        cur.execute(
            "INSERT INTO doctor (doc_id,name, specialization, phone_no, clinic_id) VALUES (%s,%s, %s, %s, %s)",
            (doc_id,name, specialization, phone_no, clinic_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('show_doctors'))
    
    # GET request: show form with clinic options
    cur.execute("SELECT * FROM clinic")
    clinics = cur.fetchall()
    conn.close()
    return render_template('add_doctor.html', clinics=clinics)

@app.route('/doctors')
def show_doctors():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctor")
    doctors = cur.fetchall()
    conn.close()
    return render_template('show_doctors.html', doctors=doctors)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    conn = connect_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone_no']
        medical_history = request.form['medical_history']
        doc_id = request.form['doc_id']
        cur.execute(
            "INSERT INTO patient (name, age, gender, phone_no, medical_history, doc_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, age, gender, phone_no, medical_history, doc_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('show_patients'))

    cur.execute("SELECT * FROM doctor")
    doctors = cur.fetchall()
    conn.close()
    return render_template('add_patient.html', doctors=doctors)

@app.route('/patients')
def show_patients():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patient")
    patients = cur.fetchall()
    conn.close()
    return render_template('show_patients.html', patients=patients)

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doc_id = request.form['doc_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']

        cur.execute(
            "INSERT INTO appointment (patient_id, doc_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)",
            (patient_id, doc_id, appointment_date, appointment_time)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('show_appointments'))

    cur.execute("SELECT * FROM patient")
    patients = cur.fetchall()
    cur.execute("SELECT * FROM doctor")
    doctors = cur.fetchall()
    conn.close()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

@app.route('/appointments')
def show_appointments():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointment")
    appointments = cur.fetchall()
    conn.close()
    return render_template('show_appointments.html', appointments=appointments)


if __name__ == '__main__':
    app.run(debug=True)
