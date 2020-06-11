"""Models for trail information."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///mapping', echo=True):
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
    gps = db.Column(db.String)
    length = db.Column(db.Float, nullable = False)
    ascent = db.Column(db.Integer)
    descent = db.Column(db.Integer)
    difficulty = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)
    img = db.Column(db.String)

    # favorites = a list of Favorite objects

    def __repr__(self):
        return f'<Trail trail_id={self.trail_id} name={self.name}>'

class Suggestion(db.Model):
    """A suggested trail from a user."""

    __tablename__ = 'suggestions'
    
    suggestion_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    desc = db.Column(db.Text)
    long = db.Column(db.Float, nullable = False)
    lat = db.Column(db.Float, nullable = False)
    gps = db.Column(db.String)
    length = db.Column(db.Float, nullable = False)
    ascent = db.Column(db.Integer)
    descent = db.Column(db.Integer)
    difficulty = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return f'<Suggestion suggestion_id={self.suggestion_id} name={self.name}>'


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True,
                        )
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    moderator = db.Column(db.Boolean, nullable = False)
    
    # favorites = a list of Favorite objects
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Favorite(db.Model):
    """A favorited trail."""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'), nullable = False)

    trail = db.relationship('Trail', backref = 'favorites')
    user = db.relationship('User', backref = 'favorites')

    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id} user_id={self.user_id} trail_id={self.trail_id}>'

def example_data():
    """Create some sample data for testing."""

    Favorite.query.delete()
    Trail.query.delete()
    User.query.delete()
    Suggestion.query.delete()

    middle = Trail(name = "Middle Sister via Pole Creek Trail", 
                   desc = "a 17.3 mile lightly trafficked out and back trail located near Sisters, Oregon that features a river and is only recommended for very experienced adventurers. The trail offers a number of activity options.",
                   long = 44.1876,
                   lat = -121.70044, 
                   gps = '/static/GPS/all_gps/middle_sister_summit_pole_creek.js', 
                   length = 17.3, 
                   ascent = 5282,
                   descent = 5282,
                   difficulty = "black", 
                   location = "Sisters, Oregon", 
                   url = "https://www.alltrails.com/trail/us/oregon/middle-sister-via-pole-creek-trail-4072", 
                   img = "https://cdn-assets.alltrails.com/uploads/photo/image/16547628/extra_large_d8480e26df4f62016e928acba537d525.jpg",
                  )

    user = User(email = 'user0@test.com', 
                password = 'test')
    favorite = Favorite(trail = middle, user = user)

    db.session.add_all([middle, user, favorite])
    db.session.commit


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)


# create_suggested_trail(name = 'New Suggestion', desc = 'winding trail', long = 43, lat = -121, gps = 'none', length = 12.5, ascent = 500, descent = 500, difficulty = 'blue', location = 'lyon, OR', url = 'none', img = 'none')