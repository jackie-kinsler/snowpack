console.log('map.js has been loaded');

var day = '11'
var month = '12'
var year = '2015'

function initMap() {
    // assign a variable called map and assign it to a new google object
    // google maps objects are coming from the googleapis script linked
    // first parameter is the element the map should be dumped in 
    // 2nd parameter is the options 
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        // map is centered on Mt. Hood summit
        center: {lat: 45.373, lng: -121.686},

        // hybrid map type has satellite with roads/labels
        mapTypeId: 'hybrid'
    });
    
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
