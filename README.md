<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/logo.png" width="250" height="auto" />

# SnowPack Map

SnowPack Map was developed for skiers and hikers. When planning for an adventure, its often desired to overlay trail data, snow depth information, and terrain maps... SnowPack Map finally makes that possible! 
<br>
SnowPack Map enables users to look at curent or historical snow depth data. Users can overlay GPS data on the map to get a detailed view of the snow depth they can plan to encounter on their next outdoor endeavor. 


<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/home.png" width="700" height="auto" />

## Deployment

https://snowpackmap.com/


## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Installation](#installation)
* [Next Steps](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack
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

SnowPack Map's main feature is a searchable map onto which current and historical snow data can be overlaid. 

<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/main-feature.gif" width="700" height="auto" />

On the /trails page, users can query for trails, and view trail information on the map. 

<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/search.gif" width="700" height="auto" />

Users can also add trails to their favorites. 

<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/favorite.gif" width="700" height="auto" />


Users can suggest new trails. 

<img src="https://raw.githubusercontent.com/jackie-kinsler/snowpack/master/static/images/readme/add-trail.png" width="700" height="auto" />

Moderators can approve, edit, or delete suggestions. Then, the suggested trail will be findable on the trails page. 

## <a name="instillation"></a>Installation 

To run SnowPack Map on your own machine: 

* Install Python 
* Install PostgreSQL (MAC OXS)

Clone or fork this repo: 
```bash
https://github.com/jackie-kinsler/snowpack
```

Create and activate a virtual environment inside the SnowPack directory: 
```bash
virtualenv env
source env/bin/activate
```

With the virtual environment active, install dependencies: 
```bash
pip install -r requirements.txt
```

Sign up to use the <a href= "https://developers.google.com/maps/documentation/javascript/tutorial">Google Maps API </a> and <a href= "https://developers.google.com/maps/documentation/javascript/get-api-key"> request an API key</a>.

NOTE: Once you have an API key, you will also need to <a href= "https://developers.google.com/maps/documentation/javascript/places">turn on the Google Maps Places library</a>. This is needed for the searchbar to work. 

Save the API keys into a file called `secrets.sh` using this format:  

```bash
export GOOGLE_MAP_API="YOUR_KEY_HERE"
```
Set up and retreive your Google OAuth 2.0 client IDs, and save them in the same secrets.sh file. 
Ensure that the approved URIs include your localhost and port. 

`secrets.sh` should now look like this: 
```bash
export GOOGLE_MAP_API="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_ID_HERE"
export GOOGLE_CLIENT_SECRET="YOUR_SECRET_HERE"
```

Copy the API keys from the `secrets.sh` file into the environment. 

```bash
source secrests.sh
```

Now, set up a database (call it `mapping`). 

```bash
createdb mapping
python model.py
python seed_database.py 
```
Run the app!

```bash
python servery.py
```

## <a name="future"></a>Next Steps
The project roadmap for SnowPack Map has several features planned: 
* Improve search algorithm when filtering for trails
* Incldue an option to only search trails inside of the map bounds 
* Email users when their suggestions have been approved
* Push search parameters into the URL so queries can easily be shared


## <a name="license"></a>License 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.