import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import sqlite3
from dotenv import load_dotenv
import threading

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



app = Flask(__name__)
#cors
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500"], 
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})



def save_to_db(nama, umur, gender, hubungan, rahasia, pesan):
    conn = sqlite3.connect("data.db")
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


@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return jsonify({"status" : "ok"}), 200
    
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
     app.run(debug=True)