from flask import Blueprint, request, render_template, redirect, url_for, session, abort
from models import SessionLocal, User
import bcrypt
import pyotp
import qrcode
import io
import base64

bp = Blueprint('auth', __name__)

def current_user(db):
    uid = session.get('user_id')
    if not uid:
        return None
    return db.query(User).filter_by(id=uid).first()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    db = SessionLocal()

    if request.method == 'GET':
        return render_template('register.html')

    email = request.form['email'].strip().lower()
    pw = request.form['password']

    if len(pw) < 8:
        return "Passwort zu kurz", 400

    existing = db.query(User).filter_by(email=email).first()
    if existing:
        return "User existiert bereits", 400

    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(pw.encode(), salt).decode()

    user = User(email=email, password_hash=pwd_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    secret = pyotp.random_base32()
    user.totp_secret = secret
    db.commit()

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name="SecureWebApp")

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    qr_data_uri = "data:image/png;base64," + img_b64

    return render_template("show_qr.html", qr=qr_data_uri)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    db = SessionLocal()

    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email'].strip().lower()
    pw = request.form['password']
    code = request.form.get('totp')

    user = db.query(User).filter_by(email=email).first()
    if not user:
        return "Unauthorized", 401

    if not bcrypt.checkpw(pw.encode(), user.password_hash.encode()):
        return "Unauthorized", 401
    
    if user.totp_secret:
        totp = pyotp.TOTP(user.totp_secret)
        if not code or not totp.verify(code, valid_window=1):
            return "2FA required or invalid", 401

    session.clear()
    session['user_id'] = user.id

    return redirect(url_for('dashboard'))

@bp.route('/delete_account', methods=['POST'])
def delete_account():
    db = SessionLocal()
    user = current_user(db)

    if not user:
        return render_template("unauthorized.html"), 401

    db.delete(user)
    db.commit()

    session.clear()
    return "Account deleted", 200