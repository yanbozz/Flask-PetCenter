from flask import Flask, render_template, request, abort, flash
from flask import session, url_for, redirect
from form import SignupForm, LoginForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)

SECRET_KEY = 'b\x93j\xd6i\x1f\x9a\x15\xd0~\x07\xb2j'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# manage = Manage(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pets = db.relationship('Pet', backref='user')


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


db.create_all()


# nelly = Pet(name="Nelly", age="5 weeks",
#             bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.", posted_by=1)
# yuki = Pet(name="Yuki", age="8 months",
#            bio="I am a handsome gentle-cat. I like to dress up in bow ties.", posted_by=1)
# basker = Pet(name="Basker", age="1 year",
#              bio="I love barking. But, I love my friends more.", posted_by=1)
# mrfurrkins = Pet(name="Mr. Furrkins", age="5 years", bio="Probably napping.", posted_by=1)
#
# # Add all pets to the session
# db.session.add(nelly)
# db.session.add(yuki)
# db.session.add(basker)
# db.session.add(mrfurrkins)
#
# # Commit changes in the session
# try:
#     db.session.commit()
# except Exception as e:
#     print(e)
#     db.session.rollback()
# finally:
#     db.session.close()


@app.route("/")
def home():
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/details/<int:pet_id>", methods=['GET', 'POST'])
def pet_details(pet_id):
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    if form.validate_on_submit():
        if session.get('user'):
            user = session['user']
        else:
            flash('Please log in first!')
            return redirect(url_for('login', _scheme="http", _external=True))
        pet.name = form.pet_name.data
        pet.age = form.pet_age.data
        pet.bio = form.pet_bio.data
        pet.posted_by = user
        try:
            db.session.commit()
        except Excetion as e:
            db.session.rollback()
            return render_template("details.html", form=form, pet=pet, message="The pet already existed!")
    return render_template("details.html", form=form, pet=pet)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(full_name=form.full_name.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully Signed Up!")
    return render_template("signup.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        curr_user = User.query.filter(User.email == form.email.data,
                                      User.password == form.password.data).first()
        if not curr_user:
            return render_template("login.html", form=form, message="Wrong credentials. Please try again.")
        session['user'] = user.id
        return render_template("login.html", message="Successfully logged in!")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home', _scheme="http", _external=True))


@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Excetion as e:
        db.session.rollback()
    return redirect(url_for('home', _scheme="http", _external=True))


if __name__ == "__main__":
    # manager.run()
    app.run(debug=True, host="0.0.0.0", port=3000)
