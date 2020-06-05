"""CRUD operations"""

from model import db, User, Trail, Favorite, connect_to_db
from datetime import datetime 

# *******************
# TRAIL CRUD FUNCTIONS:
# *******************

def create_trail(name, desc, long, lat, kml, length, ascent, descent, 
                 difficulty, location, url, img):
    """Create and return a new trail."""

    trail = Trail(name = name, desc = desc, long = long, lat = lat, kml = kml, 
                  length = length, ascent = ascent, descent = descent, 
                  difficulty = difficulty, location = location, 
                  url = url, img = img)

    db.session.add(trail)
    db.session.commit()
    
    return trail
  

def all_trails():
    """Return all trails in db."""

    return db.session.query(Trail).all()

def trails_by_distance(min_dist, max_dist):
    return db.session.query(Trail).filter(Trail.length<max_dist, 
                                          Trail.length>min_dist).all()


# *******************
# USER CRUD FUNCTIONS:
# *******************

  
def create_user(email, password):
    """Create and return a new user."""

    user = User(email = email, password = password)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(user_id):
    return db.session.query(User).get(user_id)

def get_user_by_email(user_email):
    return db.session.query(User).filter(User.email == user_email).first()

def get_password_by_email(user_email):
    if get_user_by_email(user_email):
        return (db.session.query(User.password).filter(User.email == user_email).first())[0]
    else:
        return None

def get_user_id_by_email(user_email):
    return (db.session.query(User.user_id).filter(User.email == user_email).first())[0]

# *******************
# FAVORITE CRUD FUNCTIONS:
# *******************

def create_favorite(user, trail):
    """Create and return a favorited trail."""

    favorite = Favorite(user = user, trail = trail)

    db.session.add(favorite)
    db.session.commit()

    return favorite

if __name__ == '__main__':
    from server import app
    connect_to_db(app)