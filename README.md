# 🦷 Dental Clinic Management System

This is a web application built using **Flask** and **MySQL** to manage dental clinics, doctors, patients, and appointments. It has a nice and colorful dashboard and a clean user interface.

---

## 🚀 Features

- Add and view Clinics
- Add and view Doctors
- Add and view Patients
- Add and view Appointments
- Dashboard showing total counts
- Styled using a custom color theme

---

## 🛠️ Tech Used

- Python
- Flask
- Postgresql
- HTML / CSS
- Bootstrap

---

## 🎨 Theme Colors Used

`D9ED92, B5E48C, 99D98C, 76C893, 52B69A, 34A0A4, 168AAD, 1A759F, 1E6091, 184E77`

---

## ⚙️ How to Run

1. Clone the repository:
https://github.com/yourusername/dental-clinic-management.git

2. Install the required Python libraries:

pip install flask


pip install chatterbot chatterbot_corpus


3. Make sure you have a postgresql database and tables created.

4. Update the database connection part in your `app.py` file:

conn = psycopg2.connect(
    host="localhost",
    database="dental_clinic",
    user="your_username",
    password="your_password"
)
python app.py

