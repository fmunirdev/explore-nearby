from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alizar:majboor125@localhost/helloflask'
db.init_app(app)

app.secret_key = 'development-key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session['email'] = new_user.email
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', form=form)
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':
        if form.validate_on_submit():
            address = form.address.data
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)
        else:
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)
    elif request.method == 'GET':
        return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = user.email
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        else:
            return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
