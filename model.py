"""Models for movie ratings app."""

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
