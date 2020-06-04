console.log('map.js has been loaded');

var NOAAOverlay;

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
            `https://www.nohrsc.noaa.gov/snow_model/GE/20200522/nsm_depth/nsm_depth_2020052205_${img_key}_us.png`, 
              imageBounds, 
              overlayOpts
          );

          NOAAOverlay.setMap(map)
    }
}
