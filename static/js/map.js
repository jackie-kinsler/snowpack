function initMap() {
  // get the lastest date for which snow data has been uploaded
  // then, populate a map with that data 

  $.get('/api/latest-date', (res) => {
      // response is a string of format yyyy-mm-dd
      var year = String(res.slice(0, 4));
      var month = String(res.slice(5, 7));
      var day = String(res.slice(8));
      
      calendarMap(day, month, year);

    });
}


function calendarMap(day, month, year, initial_zoom = 5, 
                     center_lat = 39.50, center_long = -121.686) {
  
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: initial_zoom,
      // map is centered on Mt. Hood summit
      center: {lat: center_lat, lng: center_long},
      mapTypeId: 'terrain'
  });
  
  // Adds the NOAA snow overlay to the map 
  addSnowOverlay(day, month, year, map);
  
  listenForMovement(map);
  
  addSearchbox(map);
}


function trailMap(day, month, year, url, thLat, thLong, initial_zoom = 5, 
                  center_lat = 45.373, center_long = -121.686) {
    
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: initial_zoom,
      // map is centered on Mt. Hood summit
      center: {lat: center_lat, lng: center_long},
      mapTypeId: 'terrain'
  });
  
  // Adds the NOAA snow overlay to the map 
  addSnowOverlay(day, month, year, map);

  // this goes to the url of the gps data, and loads it onto the map
  map.data.loadGeoJson(url);

  // styles the gps data so it is blue 
  map.data.setStyle({strokeColor : 'blue'});
  
  // adds a marker on the trailhead 
  var marker = new google.maps.Marker({
      position: {lat: thLat, lng: thLong},
      map: map,
      title: 'Trailhead!',
  });

  addSearchbox(map);
}


function addSearchbox(map) {
  // locates the id="search-box" element on DOM and turns it into a searchbox
  // adding a searchbox requires the places library when calling googlemaps api  

  var input = document.getElementById("search-box");
  var searchBox = new google.maps.places.SearchBox(input);

  // set the search box bounds to the map bounds so results will be biased 
  // to the map's current viewpoint 
  map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
  });

  var markers = [];

  // places_changed is an event fired when a user selects an item from 
  // the predictions attached to the searchbox 
  searchBox.addListener('places_changed', function() {
    // places is a list of PlaceResult objects
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // forEach() calls a function once for each element in an arary 
    // in this case, it removes any markers that were on the map by 
    // setting the marker's map to null
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      // geometry contains information like lat/long of the place
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      // Create a marker for each place.
      // place.geometry.location is lat/long for marker 
      markers.push(new google.maps.Marker({
        map: map,
        title: place.name,
        position: place.geometry.location
      }));

      // place.geometry.viewport defined the preferred viewport on the map 
      // when viewing that place 
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        // union will increase bounds to include existing bounds plus viewport 
        bounds.union(place.geometry.viewport);
      } else {
        // will extend map bounds to include existing bounds and given point 
        bounds.extend(place.geometry.location);
      }
    });
    // sets bounds so that viewport contains all markers (or is centered on a 
    // single marker in the case that only one place returned)
    map.fitBounds(bounds);
  });
}


function addSnowOverlay(day, month, year, map) {
  var NOAAOverlay;
  
  var overlayOpts = {
      opacity : 0.5
  };

  for (var [img_key, coords] of Object.entries(img_coord)) {
      
      var imageBounds = {
          north: coords[1][0],
          south: coords[0][0],
          east: coords[1][1],
          west: coords[0][1]
          };
  
          NOAAOverlay = new google.maps.GroundOverlay(
          `https://www.nohrsc.noaa.gov/snow_model/GE/${year}${month}${day}` +
          `/nsm_depth/nsm_depth_${year}${month}${day}05_${img_key}_us.png`, 
              imageBounds, 
              overlayOpts
          );

          NOAAOverlay.setMap(map);
  };
}


function listenForMovement(map) {
  // when a user stops moving the map, the map details will be collected 
  // details used to re-render the map in the same condition at a later time 
  map.addListener('idle', function() {
    var center_lat = map.getCenter().lat(); 
    var center_long = map.getCenter().lng();
    var zoom = map.getZoom(); 

    formInputs = {
      'zoom' : zoom, 
      'center_lat' : center_lat, 
      'center_long' : center_long, 
    }

    $.post('/map-details', formInputs);
  })
}