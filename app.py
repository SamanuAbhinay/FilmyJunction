from flask import Flask, render_template
from models import SeatBooking, Show, db, Movie
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from flask import request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'bookmyshow_secret_key_123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ✅ Flask 3.x compatible table creation
with app.app_context():
    db.create_all()
#============================Routocols=====================================
#=======Main Route============
@app.route('/')
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)

# ==============Movie Details Route================
#===============Movies============================
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_details.html', movie=movie)

#=================Movie Showtimes Route================
@app.route('/movie/<int:movie_id>/shows')
@login_required
def movie_shows(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    shows = Show.query.filter_by(movie_id=movie_id).all()
    return render_template('shows.html', movie=movie, shows=shows)

#=================Seat Selection Route================
@app.route('/show/<int:show_id>/seats', methods=['GET', 'POST'])
@login_required
def select_seats(show_id):
    show = Show.query.get_or_404(show_id)

    booked_seats = [
        s.seat_number for s in
        SeatBooking.query.filter_by(show_id=show_id).all()
    ]

    if request.method == 'POST':
        selected_seats = request.form.getlist('seats')

        for seat in selected_seats:
            booking = SeatBooking(
                show_id=show_id,
                seat_number=seat,
                user_id=current_user.id
            )
            db.session.add(booking)

        db.session.commit()
        return redirect(url_for('booking_success'))

    seats = []
    for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        for num in range(1, 9):
            seats.append(f"{row}{num}")

    return render_template(
        'seats.html',
        show=show,
        seats=seats,
        booked_seats=booked_seats
    )
#=================Booking Success Route================
@app.route('/booking-success')
@login_required
def booking_success():
    return render_template('success.html')

# ==============User Authentication Routes================
# ================Signup Route================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

# ================Login Route================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid credentials')

    return render_template('login.html')

# ================Logout Route================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
