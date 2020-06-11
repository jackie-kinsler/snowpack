"""Server for movie ratings app."""

import os 
from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/GPS/user_uploads'
ALLOWED_EXTENSIONS = {'kml','json','geojson','application/json','js'}

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limit file upload size to 20MB
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """Render root page of website"""

    return render_template('homepage.html', today = datetime.date(datetime.now()))

@app.route('/log-in')
def log_in():
    email = request.args.get('email')
    password = request.args.get('password')

    if crud.get_password_by_email(email) == password: 
        flash('Logged In!')
        session['user_id'] = crud.get_user_id_by_email(email)

        return redirect('/')
    else:
        flash('Log-in Failed')
        return redirect('/')
    
@app.route('/users', methods = ['POST'])
def create_account():
    """Create a new user"""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('That email is already assigned to a registered account.')

    else: 
        crud.create_user(email, password)
        flash('User successfully registered')
    
    return redirect('/')


@app.route('/trails')
def trail_page():
    """Show a trail page that has a list of trails and a map"""


    return render_template('trailpage.html')

@app.route('/filtered-trails')
def filtered_trail(): 
    """Return a list of trails filtered on distance"""
    
    min_dist = request.args.get('min_dist')
    max_dist = request.args.get('max_dist')
    
    trails = crud.trails_by_distance(min_dist, max_dist)

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

@app.route('/favorite-trails')
def favorite_trail():
    """Page to display a user's favorite trails"""

    user_id = session.get('user_id')
    if user_id:
        favorite_trails = crud.get_favorites_by_user_id(user_id)
        return render_template('favorite-trails.html', favorite_trails = favorite_trails)
    else: 
        flash('Log In to see favorite trails')
        return redirect('/')


@app.route('/add-a-trail', methods=['GET', 'POST'])
def add_a_trail():
    """Users can suggest a trail to be added to the site."""
    
    if request.method == 'GET':
        user_id = session.get('user_id')
        print(session)
        if user_id:
            return render_template("add_a_trail.html")
        else: 
            flash('Log In to add a trail')
            return redirect('/')
    
    if request.method == 'POST':
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
        gps = ""


        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect('/add-a-trail')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect('/add-a-trail')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # gps is the name of the file path to the gps information
            # used for building the Suggestion database
            gps = (os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        crud.create_suggested_trail(name, desc, lat, long, gps, length, 
                                    ascent, descent, difficulty, location, url)
        flash('Your trail has been added to suggestions! Give us some time - you\'ll see it on the trailpage soon! :)')
        return redirect('/add-a-trail')

@app.route('/moderator')
def moderator_page():
    """Moderators can manage the Suggestion database."""
    suggestions = crud.get_all_suggested()

    return render_template('moderator.html', suggestions = suggestions)

@app.route('/moderator/add-suggestion-to-db')
def add_suggestion_to_trail_db():
    """Adds a selected Suggestion to the db."""

    suggestion_id = request.args.get('suggestion_id')
    print(suggestion_id)

    suggestion = crud.get_suggestion_by_id(suggestion_id)
    print("****")
    print(suggestion)
    print(suggestion.name)
    print(suggestion.desc)
    print(type(suggestion.long))
    
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
    
    print(suggestion.name)
    return("hey")

@app.route('/moderator/delete-suggestion')
def delete_suggestion():
    """Delete a bad suggestion."""
    
    suggestion_id = request.args.get('suggestion_id')
    print(suggestion_id)

    crud.delete_suggestion_by_id(suggestion_id)

    return render_template('/moderator')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
