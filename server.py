"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime 

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefine = StrictUndefined

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
                            'trail_kml' : trail.kml,
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



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
