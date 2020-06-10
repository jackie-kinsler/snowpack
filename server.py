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

    return render_template('homepage.html')

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

@app.route('/add-a-trail')
def add_trail():
    """Page to add a trail to the db"""

    user_id = session.get('user_id')
    print(session)
    if user_id:
        return render_template("add_a_trail.html")
    else: 
        flash('Log In to add a trail')
        return redirect('/')


# @app.route('/add-to-db', methods = ['POST'])
# def add_trail_to_db():
#     """Page to add a trail to the db"""
    
#     # name = request.form.get('trail_name')
#     # print("*********")
#     # print(request)
#     # print(request.form)
#     # print(request.form.get('trail_gps'))
#     # print(request.form[0])

#     # desc = request.form.get('trail_desc')
#     # long = request.form.get('trail_long')
#     # lat = request.form.get('trail_lat')
#     # length = request.form.get('trail_length')
#     # length_unit = request.form.get('length_unit')
#     # # convert anyting in km to miles 
#     # if length_unit == 'kilometers':
#     #     length *= 0.621371
#     # ascent = request.form.get('trail_ascent')
#     # ascent_unit = request.form.get('ascent_unit')
#     # # convert anything in m to ft 
#     # if ascent_unit == 'meters':
#     #     ascent *= 3.28084
#     # descent = request.form.get('trail_descent')
#     # descent_unit = request.form.get('descent_unit')
#     # if descent_unit == 'meters': 
#     #     descent *= 3.28084
#     # difficulty = request.form.get('trail_difficulty')
#     # location = request.form.get('trail_location')
#     # url = request.form.get('trail_url')
#     # gps = request.form.get('trail_gps')
#     # gps_url = request.form.get('trail_gps_url')
#     # gps = 'blank'
#     # print("********")
#     # print(gps)

#     # RIGHT NOW USING GPS_URL INSTEAD OF THE FILE 
#     # crud.create_suggested_trail(name, desc, lat, long, gps, length, ascent, descent, 
#     #              difficulty, location, gps)
    

#     return ("Added to suggestions!")


@app.route('/add-a-trail', methods=['GET', 'POST'])
def upload_file():
    print(request)
    print(request.files['file'])

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/add-a-trail')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        # print(allowed_file(file.filename))

        if file.filename == '':
            flash('No selected file')
            return redirect('/add-a-trail')
        print(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/add-a-trail')
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
