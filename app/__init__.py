from flask import Flask, render_template,request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime


from app import routes

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)


migrate=Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name=db.Column(db.String(64), index=True, unique=True)
    expired_date = db.Column(db.Date, nullable=False)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carb = db.Column(db.Float)

    def __repr__(self):
        return f'<Food {self.id}>'



@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # Successful sign-in, redirect to add food form
            return redirect(url_for('add_food_form', user_id=user.id))
        else:
            # Invalid credentials, show error message or redirect to sign-in page
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/confirmationpage/<int:user_id>')
def confirmation_page(user_id):
    return render_template('confirmation_page.html', user_id=user_id)

@app.route('/viewmyfood/<int:user_id>')
def view_my_food(user_id):
    # Retrieve all food items associated with the user from the database
    foods = Food.query.filter_by(user_id=user_id).all()
    return render_template('viewmyfood.html', user_id=user_id, foods=foods)


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/add-food/<int:user_id>', methods=['GET', 'POST'])
def add_food_form(user_id):
    if request.method == 'POST':
        # Process the form data and add food to the database
        expired_date_str = request.form['expired_date']
        expired_date = datetime.strptime(expired_date_str, '%Y-%m-%d').date()
        name=request.form['name']
        protein = request.form['protein']
        fat = request.form['fat']
        carb = request.form['carb']
        
        # Create a new Food object and add it to the database
        food = Food(user_id=user_id, expired_date=expired_date,protein=protein, fat=fat, carb=carb,name=name)
        print(request.form)
        db.session.add(food)
        db.session.commit()

        # Redirect to a confirmation page or another route
        return redirect(url_for('confirmation_page', user_id=user_id))
    return render_template('addFoodForm.html', user_id=user_id)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Create a new User object and add it to the database
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('signup.html')


db.create_all()