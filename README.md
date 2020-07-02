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

Sign up to use the <a href= "https://developers.google.com/maps/documentation/javascript/tutorial">Google Maps API /> and <a href= "https://developers.google.com/maps/documentation/javascript/get-api-key"> request an API key />.

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