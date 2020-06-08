console.log('map.js has been loaded');

// use helper functions?

function calendarMap(day, month, year, url, initial_zoom = 7, center_lat = 45.373, center_long = -121.686) {
    
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: initial_zoom,
        // map is centered on Mt. Hood summit
        center: {lat: center_lat, lng: center_long},

        // hybrid map type has satellite with roads/labels
        mapTypeId: 'terrain'
    });
    
    map.data.loadGeoJson(url)

    map.data.setStyle({strokeColor : 'blue'})
    
    var NOAAOverlay;
    
    var overlayOpts = {
        opacity : 0.5
    }

    for (var [img_key, coords] of Object.entries(img_coord)) {
        
        var imageBounds = {
            north: coords[1][0],
            south: coords[0][0],
            east: coords[1][1],
            west: coords[0][1]
            };
    
            NOAAOverlay = new google.maps.GroundOverlay(
            `https://www.nohrsc.noaa.gov/snow_model/GE/${year}${month}${day}/nsm_depth/nsm_depth_${year}${month}${day}05_${img_key}_us.png`, 
                imageBounds, 
                overlayOpts
            );

            NOAAOverlay.setMap(map)
    }

    google.maps.event.addListener(map, 'bounds_changed', () => {
        window.setTimeout( () => {
            console.log('change!')
        }, 3000);
    });
}



function initMap() {
    // default date for map load is today's date (sometimes, snow data will
    // not load if it hasn't been uploaded yet for the day)
    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var year = today.getFullYear();
    

    calendarMap(day, month, year);
}

