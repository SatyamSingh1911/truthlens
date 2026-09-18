from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import sqlite3
from datetime import datetime, timezone
import re

app = Flask(__name__)
DB = "truthlens.db"

CATEGORIES = ["Politics", "Health", "Finance", "Other"]
PLATFORMS = ["WhatsApp", "X", "Instagram", "Other"]
STATUSES = ["Unverified", "Verified True", "False", "Misleading"]

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            platform TEXT NOT NULL,
            category TEXT NOT NULL,
            source_url TEXT,
            flags TEXT NOT NULL DEFAULT '',
            risk TEXT NOT NULL DEFAULT 'Low Risk',
            status TEXT NOT NULL DEFAULT 'Unverified',
            reviewer_note TEXT NOT NULL DEFAULT '',
            submitted_at TEXT NOT NULL,
            reviewed_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def calculate_flags(text, source_url):
    flags = []
    lower = text.lower()
    if any(phrase in lower for phrase in ["breaking", "shocking", "share before deleted"]):
        flags.append("Sensational")
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.50:
        flags.append("Shouting")
    if not source_url or not source_url.strip():
        flags.append("Unsourced")
    return flags, ("High Risk" if len(flags) >= 2 else "Low Risk")

@app.route("/")
def index():
    category = request.args.get("category", "")
    status = request.args.get("status", "")
    query = "SELECT * FROM claims WHERE 1=1"
    params = []
    if category in CATEGORIES:
        query += " AND category = ?"
        params.append(category)
    if status in STATUSES:
        query += " AND status = ?"
        params.append(status)
    # DP1: risk-first, then recency. This makes potentially problematic claims easy
    # to find while keeping the newest items prominent within each risk level.
    query += """ ORDER BY CASE risk WHEN 'High Risk' THEN 0 ELSE 1 END,
                 datetime(submitted_at) DESC"""
    conn = db()
    claims = conn.execute(query, params).fetchall()
    conn.close()
    return render_template("index.html", claims=claims, category=category, status=status,
                           categories=CATEGORIES, statuses=STATUSES)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        platform = request.form.get("platform", "")
        category = request.form.get("category", "")
        source_url = request.form.get("source_url", "").strip()
        if not text or platform not in PLATFORMS or category not in CATEGORIES:
            return render_template("submit.html", platforms=PLATFORMS, categories=CATEGORIES,
                                   error="Please complete the required fields.")
        flags, risk = calculate_flags(text, source_url)
        conn = db()
        cur = conn.execute("""
            INSERT INTO claims
            (text, platform, category, source_url, flags, risk, status, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, 'Unverified', ?)
        """, (text, platform, category, source_url, ", ".join(flags), risk,
              datetime.now(timezone.utc).isoformat()))
        conn.commit()
        claim_id = cur.lastrowid
        conn.close()
        return redirect(url_for("detail", claim_id=claim_id))
    return render_template("submit.html", platforms=PLATFORMS, categories=CATEGORIES)

@app.route("/claim/<int:claim_id>")
def detail(claim_id):
    conn = db()
    claim = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    conn.close()
    if not claim:
        abort(404)
    return render_template("detail.html", claim=claim)

@app.route("/claim/<int:claim_id>/review", methods=["POST"])
def review(claim_id):
    status = request.form.get("status")
    note = request.form.get("reviewer_note", "").strip()
    if status not in STATUSES or status == "Unverified":
        abort(400)
    conn = db()
    conn.execute("""
        UPDATE claims SET status=?, reviewer_note=?, reviewed_at=? WHERE id=?
    """, (status, note, datetime.now(timezone.utc).isoformat(), claim_id))
    conn.commit()
    conn.close()
    return redirect(url_for("detail", claim_id=claim_id))

@app.route("/api/claims")
def api_claims():
    conn = db()
    claims = [dict(r) for r in conn.execute("SELECT * FROM claims ORDER BY datetime(submitted_at) DESC").fetchall()]
    conn.close()
    return jsonify(claims)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
