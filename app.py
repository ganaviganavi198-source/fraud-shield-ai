from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


# ==============================
# DATABASE SETUP
# ==============================

def init_db():
    conn = sqlite3.connect("fraudshield.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            risk_score INTEGER,
            status TEXT,
            transaction_time TEXT,
            failed_attempts INTEGER,
            location_changed INTEGER,
            reasons TEXT
        )
    """)

    conn.commit()
    conn.close()


# Create database when application starts
init_db()


# ==============================
# HOME PAGE + FRAUD DETECTION
# ==============================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        amount = float(request.form["amount"])
        hour = int(request.form["hour"])
        failed_attempts = int(request.form["failed_attempts"])
        location_changed = int(request.form["location_changed"])

        risk_score = 0
        reasons = []

        # Check transaction amount
        if amount > 50000:
            risk_score += 30
            reasons.append("High transaction amount")

        # Check transaction time
        if hour < 6 or hour > 23:
            risk_score += 20
            reasons.append("Unusual transaction time")

        # Check failed attempts
        if failed_attempts >= 3:
            risk_score += 20
            reasons.append("Multiple failed attempts")

        # Check location
        if location_changed == 1:
            risk_score += 30
            reasons.append("Unusual location detected")

        # Maximum risk score = 100
        risk_score = min(risk_score, 100)

        # Risk level
        if risk_score <= 30:
            status = "Safe Transaction"

        elif risk_score <= 60:
            status = "Medium Risk"

        else:
            status = "High Risk"

        # ==============================
        # SAVE TRANSACTION
        # ==============================

        transaction_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        reasons_text = ", ".join(reasons)

        conn = sqlite3.connect("fraudshield.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (
                amount,
                risk_score,
                status,
                transaction_time,
                failed_attempts,
                location_changed,
                reasons
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            amount,
            risk_score,
            status,
            transaction_time,
            failed_attempts,
            location_changed,
            reasons_text
        ))

        conn.commit()
        conn.close()

        # Show result page
        return render_template(
            "result.html",
            risk_score=risk_score,
            status=status,
            reasons=reasons
        )

    return render_template("fraud_detection.html")


# ==============================

# ==============================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("fraudshield.db")
    cursor = conn.cursor()

    # Get total transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    # Get safe transactions
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE status = ?",
        ("Safe Transaction",)
    )
    safe = cursor.fetchone()[0]

    # Get medium-risk transactions
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE status = ?",
        ("Medium Risk",)
    )
    medium = cursor.fetchone()[0]

    # Get high-risk transactions
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE status = ?",
        ("High Risk",)
    )
    high = cursor.fetchone()[0]

    # Get latest 10 transactions
    cursor.execute("""
        SELECT id, amount, risk_score, status, transaction_time
        FROM transactions
        ORDER BY id DESC
        LIMIT 10
    """)

    transactions = cursor.fetchall()
    # ==============================
    # REAL TIMELINE DATA
    # ==============================

    cursor.execute("""
        SELECT
            strftime('%H:00', transaction_time) AS hour,
            COUNT(*) AS transaction_count,
            AVG(risk_score) AS average_risk
        FROM transactions
        GROUP BY hour
        ORDER BY hour
    """)

    timeline_data = cursor.fetchall()

    timeline_labels = [row[0] for row in timeline_data]
    timeline_counts = [row[1] for row in timeline_data]
    timeline_risks = [round(row[2], 2) for row in timeline_data]

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        safe=safe,
        medium=medium,
        high=high,
        transactions=transactions,
        timeline_labels=timeline_labels,
        timeline_counts=timeline_counts,
        timeline_risks=timeline_risks
     )


# ==============================
# START FLASK
# ==============================

if __name__ == "__main__":
    app.run(debug=True)