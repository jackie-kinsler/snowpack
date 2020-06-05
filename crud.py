"""CRUD operations"""

from model import db, User, Trail, Favorite, connect_to_db
from datetime import datetime 


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
    
def create_user(email, password):
    """Create and return a new user."""

    user = User(email = email, password = password)

    db.session.add(user)
    db.session.commit()

    return user

def create_favorite(user, trail):
    """Create and return a favorited trail."""

    favorite = Favorite(user = user, trail = trail)

    db.session.add(favorite)
    db.session.commit()

    return favorite

def all_trails():
    """Return all trails in db."""

    return db.session.query(Trail).all()

def trails_dist_ascent(max_dist, max_asc, min_dist = 0, min_asc=0):
    return db.session.query(Trail).filter(Trail.length<max_dist, 
                                          Trail.length>min_dist,
                                          Trail.ascent<max_asc, 
                                          Trail.ascent>min_asc).all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)