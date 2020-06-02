"""Models for trail information."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class Trail(db.Model):
    """A trail."""

    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    desc = db.Column(db.Text)
    long = db.Column(db.Float, nullable = False)
    lat = db.Column(db.Float, nullable = False)
    kml = db.Column(db.String)
    length = db.Column(db.Float, nullable = False)
    ascent = db.Column(db.Integer)
    descent = db.Column(db.Integer)
    difficult = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)
    img = db.Column(db.String)

    def __repr__(self):
        return f'<Trail trail_id={self.trail_id} name={self.name}>'

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True,
                        )
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Favorite(db.Model):
    """A favorited trail."""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, autoincrement = True, primary_key = True)

    trail = db.relationship('Trail', backref = 'trails')
    user = db.relationship('User', backref = 'users')

    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id}>'

# class Rating(db.Model):
#     """A movie rating."""

#     __tablename__ = 'ratings'

#     rating_id = db.Column(db.Integer, 
#                           autoincrement = True, 
#                           primary_key = True,
#                           )
#     score = db.Column(db.Integer)
#     movie_id = db.Column(db.Integer, 
#                          db.ForeignKey('movies.movie_id'),
#                          )
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'),
#                         )

#     movie = db.relationship('Movie', backref = 'ratings')
#     user = db.relationship('User', backref = 'ratings')
    
#     def __repr__(self):
#         return f'<Rating rating_id={self.rating_id} score={self.score}>'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
