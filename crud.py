"""CRUD operations"""

from model import db, User, Movie, Rating, connect_to_db
from datetime import datetime 


def create_trail(name, desc, long, lat, kml, length, ascent, descent, difficulty, location, url, img)
# def create_user(email, password):
#     """Create and return a new user."""

#     user = User(email = email, password = password)

#     db.session.add(user)
#     db.session.commit()

#     return user

# def create_movie(title = None, overview = None, release_date = None, poster_path = None):
#     """Create and return a new movie"""

#     movie = Movie(title = title, 
#                   overview = overview, 
#                   release_date = release_date, 
#                   poster_path = poster_path)

#     db.session.add(movie)
#     db.session.commit()

#     return movie



if __name__ == '__main__':
    from server import app
    connect_to_db(app)