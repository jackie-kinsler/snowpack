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

if __name__ == '__main__':
    from server import app
    connect_to_db(app)