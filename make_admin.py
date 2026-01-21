from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(username="Admin").first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("Admin assigned ✅")
    else:
        print("User not found ❌")
