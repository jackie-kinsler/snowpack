"""CRUD operations"""

from model import db, User, Trail, Favorite, Suggestion, connect_to_db
from datetime import datetime 

# *******************
# TRAIL CRUD FUNCTIONS:
# *******************

def create_trail(name, desc, lat, long, gps, length, ascent, descent, 
                 difficulty, location, url, img):
    """Create and return a new trail."""

    trail = Trail(name = name, desc = desc, long = long, lat = lat, gps = gps, 
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

def get_trail_by_id(trail_id):
    return db.session.query(Trail).get(trail_id)

def add_gps_by_trail_id(trail_id, gps_path):
    trail = db.session.query(Trail).filter(Trail.trail_id == trail_id).first()
    trail.gps = gps_path
    db.session.commit()

def get_gps_by_trail_id(trail_id):
    return (get_trail_by_id(trail_id)).gps


# *******************
# SUGGESTION CRUD FUNCTIONS:
# *******************

def create_suggested_trail(name, desc, lat, long, gps, length, ascent, descent, 
                 difficulty, location, url, user):
    """Create and return a new suggested trail."""

    suggestion = Suggestion(name = name, desc = desc, long = long, lat = lat, gps = gps, 
                  length = length, ascent = ascent, descent = descent, 
                  difficulty = difficulty, location = location, 
                  url = url, user = user)

    db.session.add(suggestion)
    db.session.commit()
    
    return suggestion

def get_all_suggested():
    return db.session.query(Suggestion).all()

def get_suggestion_by_id(suggestion_id):
    return db.session.query(Suggestion).get(suggestion_id)    

def delete_suggestion_by_id(suggestion_id):
    suggestion = get_suggestion_by_id(suggestion_id)
    db.session.delete(suggestion)
    db.session.commit()

    return "Delete successful."

# *******************
# USER CRUD FUNCTIONS:
# *******************

  
def create_user(email, password, moderator = False):
    """Create and return a new user."""

    user = User(email = email, password = password, moderator = moderator)

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
def check_favorite_exists(user, trail):
    return db.session.query(Favorite).filter(Favorite.user == user, Favorite.trail == trail).first()

def get_favorites_by_user_id(user_id):
    return db.session.query(Favorite).filter(Favorite.user_id == user_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)