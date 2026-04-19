import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import sqlite3
from dotenv import load_dotenv
import threading

app = Flask(__name__, static_folder="../front-end")
CORS(app)

@app.route("/")

def home():
    return send_from_directory(app.static_folder, "index.html")

load_dotenv()

#fuction gmail
def send_email_async(nama, umur, gender, hubungan, rahasia, pesan):

    try:
        EMAIL = os.getenv("EMAIL_ADDRESS")
        PASSWORD = os.getenv("APP_PASSWORD")

        msg = EmailMessage()
        msg.set_content(f"""---
        Nama: {nama}
        Umur: {umur}
        Gender: {gender}
        Hubungan: {hubungan}
        \nRahasia:\n{rahasia}
        \nPesan:\n{pesan}
        """)
        msg["Subject"] = ("Pesan Baru dari Website 📩".upper())
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"Data dari {nama} Berhasil Dikirim")

    except Exception as e:
        print(f"Debug Email {e}")

def save_to_db(nama, umur, gender, hubungan, rahasia, pesan):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pesan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        umur TEXT,
        gender TEXT,
        hubungan TEXT,
        rahasia TEXT,
        pesan TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO pesan (nama, umur, gender, hubungan, rahasia, pesan) VALUES (?, ?, ?, ?, ?, ?)",
        (nama, umur, gender, hubungan, rahasia, pesan)
    )

    conn.commit()
    conn.close()


@app.route("/submit")
def submit()
    try:
        data = request.get_json(force=True, silent=True) or {}
       

        nama = data.get("nama", "-")
        umur = data.get("umur", "-")
        gender = data.get("gender", "-")
        hubungan = data.get("hubungan", "-")
        rahasia = data.get("rahasia", "-")
        pesan = data.get("pesan", "-")


        #Database (sqlite)
        save_to_db(nama, umur, gender, hubungan, rahasia, pesan)

        #Gmail
        email_threading = threading.Thread(
            target=send_email_async,
            args=(nama, umur, gender, hubungan, rahasia, pesan)
        )
        email_threading.start()
       
        return jsonify({
            "status": "success",       
            "message": "Pesan berhasil dikirim ✅\nZyy sudah mendapatkan pesan 📩"
        }), 200

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
     app.run()