from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect

app = Flask(__name__)

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mealitpal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)

class Meal(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    date_stored=db.Column(db.Date, nullable=False)
    expiry_date=db.Column(db.Date, nullable=False)
    protein=db.Column(db.Float, nullable=False)
    carb=db.Column(db.Float, nullable=False)
    fat=db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return {"message": "Hello World"}

# ... your existing imports
from flask import render_template, request, redirect # ... 

# ... other routes

@app.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == "POST":
        # Get form data, validate, and store the user in the database (hash password!)
        return redirect('/') # Redirect to home after successful registration 
    else:
        return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    # Similar structure as register - authenticate user
    return render_template('login.html') 

@app.route('/add_meal', methods=["GET", "POST"])
def add_meal():
    # Similar structure -  get meal info, store in database 
    return render_template('add_meal.html')








