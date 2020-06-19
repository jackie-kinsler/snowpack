"""Dropdb, createdb, and populate all tables"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb mapping')
os.system('createdb mapping')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/trails.json') as f:
    trail_data = json.loads(f.read())


# Create trails, store them in list

trails_in_db = []
for trail in trail_data['trails']:
    name = trail.get('name')
    desc = trail.get('summary')
    long = trail.get('longitude')
    lat = trail.get('latitude')
    gps = None 
    length = trail.get('length')
    ascent = trail.get('ascent')
    descent = trail.get('descent')
    difficulty = trail.get('difficulty')
    location = trail.get('location')
    url = trail.get('url')
    img = trail.get('imgMedium')
    
    
    trail = crud.create_trail(name, 
                              desc, 
                              lat,
                              long, 
                              gps, 
                              length, 
                              ascent, 
                              descent, 
                              difficulty, 
                              location, 
                              url, 
                              img)

    trails_in_db.append(trail)
 
for n in range(10):
    email = f'user{n}@test.com'
    # password = 'test'
    # user = crud.create_user(email = email, password = password)
    user = crud.create_user(email = email)
    

    for _ in range(10):
        crud.create_favorite(user, choice(trails_in_db))


# ***************

# Add any data as needed!

# ***************

crud.add_gps_by_trail_id(7,'/static/GPS/wonderland.js')

crud.create_trail("Middle Sister via Pole Creek Trail", 
                  "a 17.3 mile lightly trafficked out and back trail located near Sisters, Oregon that features a river and is only recommended for very experienced adventurers. The trail offers a number of activity options.",
                  44.1876,
                  -121.70044, 
                  '/static/GPS/all_gps/middle_sister_summit_pole_creek.js', 
                  17.3, 
                  5282,
                  5282,
                  "black", 
                  "Sisters, Oregon", 
                  "https://www.alltrails.com/trail/us/oregon/middle-sister-via-pole-creek-trail-4072", 
                  "https://cdn-assets.alltrails.com/uploads/photo/image/16547628/extra_large_d8480e26df4f62016e928acba537d525.jpg",
                  )

# crud.create_user(email = 'moderator@test.com', password = 'test', moderator = True)