from flask import Flask, render_template, request, redirect, url_for
from db_config import connect_db
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import jsonify

clinic_bot = ChatBot(
    'ClinicBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbot_db.sqlite3'
)
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(clinic_bot)

trainer.train([
    "Hello",
    "Hi there! Welcome to the Dental Clinic. How can I help you today?",
    
    "Hi",
    "Hello! Need help with appointments or billing?",
    
    "What services do you offer?",
    "We offer general dentistry, orthodontics, root canals, teeth whitening, and pediatric dentistry.",
    
    "What are your clinic hours?",
    "Our clinics operate from 9 AM to 5 PM, Monday to Saturday.",
    
    "Are you open on Sundays?",
    "Our clinics are generally closed on Sundays.",
    
    "How do I book an appointment?",
    "You can book appointments through the website or call the clinic directly.",
    
    "Can I walk in without an appointment?",
    "Walk-ins are allowed, but appointments are recommended to avoid wait times.",
    
    "Do you accept new patients?",
    "Yes, we are accepting new patients. You can register online or visit the clinic.",
    
    "Do you have female dentists?",
    "Yes, we have both male and female dentists on staff.",
    
    "Where are your clinics located?",
    "We have clinics in Mumbai, Pune, and Delhi. Check the 'Clinics' section for full addresses.",
    
    "How can I reach your clinic?",
    "You can find directions on our website or search for us on Google Maps.",
    
    "How much does a checkup cost?",
    "A basic dental checkup costs ₹300.",
    
    "How much is cleaning?",
    "Teeth cleaning costs range from ₹500 to ₹1000 depending on the clinic and services used.",
    
    "What is the payment process?",
    "You can pay via cash, UPI, or card after your appointment at the billing counter.",
    
    "Can I cancel an appointment?",
    "Yes, appointments can be cancelled up to 24 hours in advance.",
    
    "Do you have emergency services?",
    "Yes, we provide emergency dental services. Call the clinic for immediate support.",
    
    "Is there parking available?",
    "Yes, all our clinics have free parking facilities for patients.",
    
    "Do you treat children?",
    "Yes, we have pediatric dentists for children’s dental care.",
    
    "What happens after I register?",
    "After registering, you can book an appointment or wait for our team to contact you.",
])

app = Flask(__name__)



@app.route('/chat-ajax', methods=['POST'])
def chat_ajax():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_reply = str(clinic_bot.get_response(user_message))
    return jsonify({'reply': bot_reply})

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
        phone_no = request.form["phone_no"]
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
        phone_no = request.form['phone_no']
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

@app.route('/chat-popup', methods=['POST'])
def chat_popup():
    user_input = request.form['user_input']
    response = clinic_bot.get_response(user_input)

    return render_template('home.html', response=response)
@app.route('/')
def dashboard():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM patient")
    total_patients = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM doctor")
    total_doctors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointment")
    total_appointments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM clinic")
    total_clinics = cur.fetchone()[0]

    conn.close()

    return render_template('home.html',
                           total_patients=total_patients,
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           total_clinics=total_clinics)

if __name__ == '__main__':
    app.run(debug=True)
