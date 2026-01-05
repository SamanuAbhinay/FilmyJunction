from app import app
from models import db, Movie

with app.app_context():
    m1 = Movie(
        title="Leo",
        poster="leo.jpg",
        rating=8.1,
        description="A violent past catches up with a former gangster."
    )

    m2 = Movie(
        title="Jawan",
        poster="jawan.jpg",
        rating=7.9,
        description="A high-octane action thriller with emotional depth."
    )

    m3 = Movie(
        title="Guntur Karam",
        poster="gunturkaram.jpg",
        rating=7.4,
        description="A gripping tale of love and revenge in a small town."
    )

    m4 = Movie(
        title="Salaar",
        poster="salaar.jpg",
        rating=8.9,
        description="An intense action drama about a vigilante's quest for justice."
    )

    db.session.add_all([m1, m2, m3, m4])
    db.session.commit()


print("Movies inserted successfully ✅")

from app import app
from models import db, Theatre, Screen, Show, Movie

with app.app_context():
    theatre1 = Theatre(name="PVR Cinemas", location="Hyderabad")
    theatre2 = Theatre(name="INOX", location="Hyderabad")
    theatre3 = Theatre(name="Cinepolis", location="Hyderabad")
    theatre4 = Theatre(name="AMB Cinemas", location="Hyderabad")
    theatre5 = Theatre(name="Satyam Cinemas", location="Hyderabad")
    theatre6 = Theatre(name="Prasads IMAX", location="Hyderabad")
    theatre7 = Theatre(name="Escape Cinemas", location="Hyderabad")
    theatre8 = Theatre(name="Carnival Cinemas", location="Hyderabad")
    theatre9 = Theatre(name="Big Cinemas", location="Hyderabad")
    theatre10 = Theatre(name="Luxe Cinemas", location="Hyderabad")
    theatre11 = Theatre(name="AAA Cinemas", location="Hyderabad")


    db.session.add_all([theatre1, theatre2, theatre3, theatre4, theatre5, theatre6, theatre7, theatre8, theatre9, theatre10, theatre11])
    db.session.commit()

    screen1 = Screen(name="Screen 1", theatre=theatre1)
    screen2 = Screen(name="Screen 2", theatre=theatre2)
    screen3 = Screen(name="Screen 3", theatre=theatre3)
    screen4 = Screen(name="Screen 4", theatre=theatre4)
    screen5 = Screen(name="Screen 5", theatre=theatre5)
    screen6 = Screen(name="Screen 6", theatre=theatre6)
    screen7 = Screen(name="Screen 7", theatre=theatre7)
    screen8 = Screen(name="Screen 8", theatre=theatre8)
    screen9 = Screen(name="Screen 9", theatre=theatre9)
    screen10 = Screen(name="Screen 10", theatre=theatre10)
    screen11 = Screen(name="Screen 11", theatre=theatre11)

    db.session.add_all([screen1, screen2, screen3, screen4, screen5, screen6, screen7, screen8, screen9, screen10, screen11])
    db.session.commit()

    leo = Movie.query.filter_by(title="Leo").first()
    jawan = Movie.query.filter_by(title="Jawan").first()
    guntur_karam = Movie.query.filter_by(title="Guntur Karam").first()
    salaar = Movie.query.filter_by(title="Salaar").first()

    show1 = Show(movie=leo, screen=screen1, show_time="10:30 AM")
    show2 = Show(movie=leo, screen=screen2, show_time="6:30 PM")
    show3 = Show(movie=jawan, screen=screen3, show_time="1:30 PM")
    show4 = Show(movie=jawan, screen=screen4, show_time="9:30 PM")
    show5 = Show(movie=guntur_karam, screen=screen5, show_time="11:00 AM")
    show6 = Show(movie=guntur_karam, screen=screen6, show_time="5:00 PM")
    show7 = Show(movie=salaar, screen=screen7, show_time="2:00 PM")
    show8 = Show(movie=salaar, screen=screen8, show_time="8:00 PM")

    db.session.add_all([show1, show2, show3, show4, show5, show6, show7, show8])
    db.session.commit()

print("Theatres & shows added ✅")
