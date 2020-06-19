
# standard libraryies 
import json
import os 
from datetime import datetime 

# third-party libraries 
from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename
import requests

# Internal imports
from model import connect_to_db
import crud


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined

# Google OAuth 2.0 Configuration 
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
# instantiate loginManager class 
login_manager = LoginManager()
# configure login manager wo work with Flask app 
login_manager.init_app(app)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)

# Upload configuration 
UPLOAD_FOLDER = 'static/GPS/user_uploads'
ALLOWED_EXTENSIONS = {'kml','json','geojson','application/json','js'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limit file upload size to 20MB
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

##########################
# This file contains three sections: 
# 1. Routes that render pages
# 2. API routes
# 3. Helper functions 
##########################

##########################
# ROUTES THAT RENDER PAGES 
##########################

@app.route('/')
def homepage():
    """Render root of website"""
    print(session)
    authenticated = current_user.is_authenticated
    if authenticated:
        email = current_user.email
        return render_template('homepage.html',
                            today = datetime.date(datetime.now()), authenticated = authenticated, email = email)
    else:  
        return render_template('homepage.html', 
                            today = datetime.date(datetime.now()), authenticated = authenticated)

@app.route('/trails')
def trail_page():
    """Render page with map and trail filtering capability."""

    return render_template('trailpage.html')


@app.route('/favorite-trails')
def favorite_trail():
    """Render page of user's favorite trails (only if logged in)."""

    user_id = session.get('user_id')
    if user_id:
        favorite_trails = crud.get_favorites_by_user_id(user_id)
        return render_template('favorite-trails.html', 
                               favorite_trails = favorite_trails)
    else: 
        return render_template('favorite-trails.html')


@app.route('/add-a-trail', methods=['GET', 'POST'])
def add_a_trail():
    """Render page where users can add a suggested trail (only if logged in)."""
    
    if request.method == 'GET':
        return render_template("add_a_trail.html")
    
    if request.method == 'POST':
        create_suggestion_from_user_inputs()
        
        flash('Your trail has been added to suggestions!' +
              ' Give us some time - you\'ll see it on the trailpage soon! :)')
        return redirect('/add-a-trail')


@app.route('/moderator')
def moderator_page():
    """Render moderator page. Here, suggestions can be added, edited, or deleted."""
    suggestions = crud.get_all_suggested()

    return render_template('moderator.html', suggestions = suggestions)


@app.route('/moderator/<suggestion_id>')
def edit_suggestion(suggestion_id):

    suggestion = crud.get_suggestion_by_id(suggestion_id)

    return render_template('edit_suggestion.html', suggestion = suggestion)


##########################
# API ROUTES 
##########################

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email"],
    )
    return redirect(request_uri)

# Handle the google login callback endpoint 
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = crud.get_user_by_email(users_email)
    print("user", user)
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )

    # Doesn't exist? Add it to the database.
    if not user:
        user = crud.create_user(users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("homepage"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
    

# @app.route('/api/log-in')
# def log_in():
#     """Check user input email/password against User table in db"""
    
#     email = request.args.get('email')
#     password = request.args.get('password')

#     user = crud.get_user_by_email(email)
    
#     # if credentials are in db, the user_id and moderator boolean
#     # are added to session 
#     if user: 
#         if user.password == password: 
#             session['user_id'] = user.user_id
#             session['moderator'] = user.moderator
#             return ('success')
#     else:
#         return('failure')
        
    
# @app.route('/api/log-out')
# def log_out():
#     """Log out user and clear the session."""

#     session.clear()
#     return "logged out"


@app.route('/api/is-logged-in')
def check_if_user():
    print(session)
    if session.get('user_id'):
        return('true')
    else:
        return ('false')


@app.route('/api/create-user', methods = ['POST'])
def create_account():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('That email is already assigned to a registered account.')

    else: 
        crud.create_user(email = email, password = password)
        flash('User successfully registered.')
    
    return redirect('/')


@app.route('/api/filtered-trails')
def filtered_trail(): 
    """Return a list of trails filtered on distance"""
    
    trail_name = request.args.get('trail_name')
    min_dist = request.args.get('min_dist')
    max_dist = request.args.get('max_dist')

    if min_dist == '':
        min_dist = 0
    if max_dist == '': 
        max_dist = 99999
    
    if trail_name == '': 
        trails = crud.trails_by_distance(min_dist, max_dist)
    else:
        trails = crud.trails_by_name_distance(min_dist, max_dist, trail_name)

    trail_list = []

    for trail in trails: 
         trail_list.append({'trail_id' : trail.trail_id,
                            'trail_name' : trail.name,
                            'trail_url' : trail.url, 
                            'trail_distance' : trail.length,
                            'trail_location' : trail.location,
                            'trail_gps' : trail.gps,
                            'trail_lat' : trail.lat,
                            'trail_long' : trail.long,
                           })
    return jsonify(trail_list)

@app.route('/add-to-favorites')
def add_to_favorites():
    """Add a trail to favorites based after pressing favorite button on /trails page."""

    # The trail_id comes from the client (attached to the favorite button)
    trail_id = request.args.get('trail_id')

    # the user id comes from the session (if they logged in)
    user_id = session.get('user_id')

    if not user_id: 
        return ("Please log in to favorite trails.")

    user = crud.get_user_by_id(user_id)

    trail = crud.get_trail_by_id(trail_id)
    
    if crud.check_favorite_exists(user, trail):
        return ("You must really like that trail :) You already favorited it!")
    
    # create a new favorite in the database 
    crud.create_favorite(user, trail)

    return (trail.name + " added to favorites!")


@app.route('/moderator/add-to-trail-db', methods = ['POST'])
def add_suggestion_to_trail_db():
    """Adds a selected Suggestion to the db."""

    suggestion_id = request.form.get('suggestion_id')

    suggestion = crud.get_suggestion_by_id(suggestion_id)
    
    crud.create_trail(suggestion.name, 
                      suggestion.desc, 
                      float(suggestion.lat), 
                      float(suggestion.long),
                      suggestion.gps, 
                      suggestion.length, 
                      suggestion.ascent, 
                      suggestion.descent,
                      suggestion.difficulty, 
                      suggestion.location, 
                      suggestion.url,
                      None
                    )
    
    return("Suggestion added to trail db")

@app.route('/moderator/delete-suggestion', methods = ['POST'])
def delete_suggestion():
    """Delete a bad suggestion."""
    
    suggestion_id = request.form.get('suggestion_id')

    crud.delete_suggestion_by_id(suggestion_id)

    return redirect('/moderator')



@app.route('/moderator/add-edited-suggestion', methods = ['POST'])
def add_edited_suggestion():
    """Add an edited suggestion to the trail db. Delete the suggestion from Suggestion db."""
    
    name = request.form.get('name')
    desc = request.form.get('description')
    lat = float(request.form.get('lat'))
    long = float(request.form.get('long'))
    length = float(request.form.get('length'))
    ascent = request.form.get('ascent')
    descent = request.form.get('descent')
    difficulty = request.form.get('difficulty')
    location = request.form.get('location')
    url = request.form.get('url')
    gps = request.form.get('gps')

    crud.create_trail(name, desc, lat, long, gps, length, ascent, descent, 
                 difficulty, location, url, None)

    suggestion_id = request.form.get('suggestion-id')
    crud.delete_suggestion_by_id(suggestion_id)

    flash("Trail has been added and suggestion has been deleted.")
    return redirect('/moderator')

@app.route('/map-details', methods = ['GET','POST'])
def store_map_details():
    """Store map details for use later."""

    if request.method == 'POST':
        zoom = request.form.get('zoom')
        center_lat = request.form.get('center_lat')
        center_long = request.form.get('center_long')

        session['zoom'] = zoom
        session['center_lat'] = center_lat
        session['center_long'] = center_long

        return ('success')
    
    if request.method == 'GET':
        map_params = {'zoom' : session.get('zoom'), 
                      'center_lat' : session.get('center_lat'), 
                      'center_long' : session.get('center_long')
                     }
        return jsonify(map_params)


##########################
# HELPER FUNCTIONS 
##########################

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_suggestion_from_user_inputs():
    """Parses the form from /add-a-trail"""
    name = request.form.get('name')
    desc = request.form.get('description')
    long = float(request.form.get('long'))
    lat = float(request.form.get('lat'))
    length = float(request.form.get('length'))
    length_unit = request.form.get('length-unit')
    if length_unit == 'kilometers':
        length *= 0.621371
    ascent = request.form.get('ascent')
    ascent_unit = request.form.get('ascent-unit')
    if ascent_unit == 'meters':
        ascent *= 3.28084
    descent = request.form.get('descent')
    descent_unit = request.form.get('descent-unit')
    if descent_unit == 'meters':
        descent *= 3.28084
    difficulty = request.form.get('difficulty')
    location = request.form.get('location')
    url = request.form.get('url')
    print("*****")
    print(url)
    gps = ""
    user_id = session.get('user_id')
    user = crud.get_user_by_id(user_id)
    file = request.files.get('file')


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # gps is the name of the file path to the gps information
        # used for building the Suggestion database
        gps = (os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    crud.create_suggested_trail(name, desc, lat, long, gps, length, 
                                ascent, descent, difficulty, location, url, user)
    return 



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, ssl_context = "adhoc")
