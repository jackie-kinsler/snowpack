"""Dropdb, createdb, and populate all tables"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title = movie.get('title')
    overview = movie.get('overview')
    poster_path = movie.get('poster_path')
    release_date = datetime.strptime(movie.get('release_date'), '%Y-%m-%d')

    movie = crud.create_movie(title, overview, release_date, poster_path)

    movies_in_db.append(movie)
 
for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'
    user = crud.create_user(email, password)
    
    for _ in range(10):
        crud.create_rating(user, choice(movies_in_db), randint(1,5))
