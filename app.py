from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///mealitpal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

@app.route('/')
def index():
    return "Welcome to MealitPal!"

if __name__ == '__main__':
    app.run(debug=True)

class User(db.Model):
    id=db.Column(db.Interger,primary_key= True)
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

