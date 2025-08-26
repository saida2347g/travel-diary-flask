from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_diary.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ----------------- MODELS -----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    cost = db.Column(db.Float)
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- ROUTES -----------------
@app.route('/')
def index():
    travels = Travel.query.order_by(Travel.date_created.desc()).all()
    return render_template("index.html", travels=travels)

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна!")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for("index"))
        else:
            flash("Неверные данные")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/add', methods=["GET","POST"])
def add_travel():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        location = request.form["location"]
        cost = request.form["cost"]
        description = request.form["description"]

        # загрузка картинки
        file = request.files["image"]
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        travel = Travel(
            user_id=session["user_id"],
            title=title,
            location=location,
            cost=float(cost) if cost else None,
            description=description,
            image=filename
        )
        db.session.add(travel)
        db.session.commit()
        flash("Путешествие добавлено!")
        return redirect(url_for("index"))
    return render_template("add_travel.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
