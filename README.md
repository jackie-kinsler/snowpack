<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/logo.png" width="250" height="auto" />

# SnowPack Map

SnowPack Map features a searchable map with curernt snow depth overlaid. The app was created with hikers and skiiers in mind, therefore combines mapping, snow-depth information, and trail information. 


<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/home.png" width="400" height="auto" />

## Deployment

https://snowpackmap.com/


## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)
* [License](#license)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* Jinja2
* SQL
* SQLAlchemy ORM
* HTML
* CSS
* Bootstrap
* jQuery
* Google Maps JavaScript API (and Places Library)
* OAuth2.0

## <a name="features"></a>Features

## <a name="instillation"></a>Installation 

To run SnowPack Map on your own machine: 

Install Python 
Install PostgreSQL (MAC OXS)

Clone or fork this repo: 
```bash
https://github.com/jackie-kinsler/snowpack
```

Create and activate a virtual environment inside the SnowPack directory: 
```bash
virtualenv env
source env/bin/activate
```

Install dependencies: 
```bash
pip install -r requirements.txt
```

Sign up to use the <a href= "https://developers.google.com/maps/documentation/javascript/tutorial">Google Maps API </a> and <a href= "https://developers.google.com/maps/documentation/javascript/get-api-key"> request an API key </a>.

NOTE: Once you have an API key, you will also need to <a href= "https://developers.google.com/maps/documentation/javascript/places">turn on the Google Maps Places library </a>. This is needed for the searchbar to work. 

Save your api keys into a file called `secrets.sh` using this format:  

```bash
export GOOGLE_MAP_API="YOUR_KEY_HERE"
```
Set up and download your Google OAuth 2.0 client IDs, and save them in the same secrets.sh file. 

It should now look like this: 
```bash
export GOOGLE_MAP_API="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_ID_HERE"
export GOOGLE_CLIENT_SECRET="YOUR_SECRET_HERE"
```


## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)