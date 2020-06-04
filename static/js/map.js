console.log('map.js has been loaded')

 // This example creates a custom overlay called NOAAOverlay, containing
// NOAA / NOHRSC images of snow depth information.


// Initialize the map and the custom overlay.

function initMap() {

    // Set the custom overlay object's prototype to a new instance
    // of OverlayView. In effect, this will subclass the overlay class therefore
    // it's simpler to load the API synchronously, using
    // google.maps.event.addDomListener().
    // Note that we set the prototype to an instance, rather than the
    // parent class itself, because we do not wish to modify the parent class.

    var overlay;
    NOAAOverlay.prototype = new google.maps.OverlayView();

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: {lat: 45.373, lng: -121.686},
        mapTypeId: 'hybrid'
    });

    // here, we are looping over all entries in the img_coord dictionary
    for (var [img_key, coords] of Object.entries(img_coord)) {

        // bounds represents the lower left corner and upper right corner 
        // that the image will be stretch ed to 
        var bounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(coords[0][0], coords[0][1]),
        new google.maps.LatLng(coords[1][0], coords[1][1])
        );

        // the srcImage comes from the NOAA/NOHRSC website, where the img_key
        // directs to the appropriate image to populate 
        // WILL NEED TO ACCOUNT FOR DATE AS WELL 
        var srcImage = `https://www.nohrsc.noaa.gov/snow_model/GE/20200522/nsm_depth/nsm_depth_2020052205_${img_key}_us.png`;
        
        // The custom NOAAOverlay object contains the NOAA image,
        // the bounds of the image, and a reference to the map.
        overlay = new NOAAOverlay(bounds, srcImage, map);

    }


/** @constructor */
function NOAAOverlay(bounds, image, map) {

// Initialize all properties.
this.bounds_ = bounds;
this.image_ = image;
this.map_ = map;

// Define a property to hold the image's div. We'll
// actually create this div upon receipt of the onAdd()
// method so we'll leave it null for now.
this.div_ = null;

// Explicitly call setMap on this overlay.
this.setMap(map);
}

/**
 * onAdd is called when the map's panes are ready and the overlay has been
 * added to the map.
 */
NOAAOverlay.prototype.onAdd = function() {

var div = document.createElement('div');
div.style.borderStyle = 'none';
div.style.borderWidth = '0px';
div.style.position = 'absolute';

// Create the img element and attach it to the div.
var img = document.createElement('img');
img.src = this.image_;
img.style.width = '100%';
img.style.height = '100%';
img.style.position = 'absolute';
div.appendChild(img);

this.div_ = div;
this.div_.style.opacity = 0.5;

// Add the element to the "overlayLayer" pane.
var panes = this.getPanes();
panes.overlayLayer.appendChild(div);
};

NOAAOverlay.prototype.draw = function() {

// We use the south-west and north-east
// coordinates of the overlay to peg it to the correct position and size.
// To do this, we need to retrieve the projection from the overlay.
var overlayProjection = this.getProjection();

// Retrieve the south-west and north-east coordinates of this overlay
// in LatLngs and convert them to pixel coordinates.
// We'll use these coordinates to resize the div.
var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());

// Resize the image's div to fit the indicated dimensions.
var div = this.div_;
div.style.left = sw.x + 'px';
div.style.top = ne.y + 'px';
div.style.width = (ne.x - sw.x) + 'px';
div.style.height = (sw.y - ne.y) + 'px';
};

// The onRemove() method will be called automatically from the API if
// we ever set the overlay's map property to 'null'.
NOAAOverlay.prototype.onRemove = function() {
this.div_.parentNode.removeChild(this.div_);
this.div_ = null;
};

}