from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)

from models import db, User, Movie, Show, SeatBooking
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "bookmyshow_secret_key_123"

# ================= DATABASE CONFIG =================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ================= LOGIN MANAGER =================
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= CREATE TABLES =================
with app.app_context():
    db.create_all()

# ================= HOME =================
@app.route("/")
def home():
    movies = Movie.query.all()

    user_bookings = []
    if current_user.is_authenticated:
        user_bookings = SeatBooking.query.filter_by(
            user_id=current_user.id
        ).all()

    return render_template(
        "home.html",
        movies=movies,
        bookings=user_bookings
    )

# ================= MOVIE DETAILS =================
@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template("movie_details.html", movie=movie)

# ================= SHOW TIMES =================
@app.route("/movie/<int:movie_id>/shows")
@login_required
def movie_shows(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    shows = Show.query.filter_by(movie_id=movie_id).all()
    return render_template("shows.html", movie=movie, shows=shows)

# ================= SEAT SELECTION =================
@app.route("/show/<int:show_id>/seats", methods=["GET", "POST"])
@login_required
def select_seats(show_id):
    show = Show.query.get_or_404(show_id)

    booked_seats = [
        s.seat_number
        for s in SeatBooking.query.filter_by(show_id=show_id).all()
    ]

    if request.method == "POST":
        selected_seats = request.form.getlist("seats")

        for seat in selected_seats:
            booking = SeatBooking(
                show_id=show_id,
                seat_number=seat,
                user_id=current_user.id
            )
            db.session.add(booking)

        db.session.commit()
        return redirect(url_for("booking_success"))

    seats = []
    for row in "ABCDEFGHIJ":
        for num in range(1, 9):
            seats.append(f"{row}{num}")

    return render_template(
        "seats.html",
        show=show,
        seats=seats,
        booked_seats=booked_seats
    )

# ================= BOOKING SUCCESS =================
@app.route("/booking-success")
@login_required
def booking_success():
    return render_template("success.html")

# ================= USER BOOKINGS =================
@app.route("/my-bookings")
@login_required
def my_bookings():
    bookings = SeatBooking.query.filter_by(
        user_id=current_user.id
    ).all()
    return render_template("my_bookings.html", bookings=bookings)

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("home"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ================= ADMIN DASHBOARD =================
@app.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    movies = Movie.query.all()
    bookings = SeatBooking.query.all()

    return render_template("admin/dashboard.html",
        movies=movies,
        bookings=bookings
    )

# ================= ADMIN ADD MOVIE =================
@app.route("/admin/add-movie", methods=["GET", "POST"])
@login_required
def add_movie():
    if not current_user.is_admin:
        abort(403)

    if request.method == "POST":
        movie = Movie(
            title=request.form["title"],
            rating=request.form["rating"],
            description=request.form["description"],
            poster=request.form["poster"]
        )
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_movie.html")

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)
    