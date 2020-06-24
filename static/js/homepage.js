
console.log('homepage.js has been loaded')


$( document ).ready(function() {
    
    $('#date-form').on('submit', (evt) => {
        evt.preventDefault();
        
        const date = $('#calendar').val();
        const year = date.slice(0,4);
        const month = date.slice(5,7);
        const day = date.slice(8);

        $("#date-notice-box").text(`Viewing data from ${month}-${day}-${year}`)

        $.get('/map-details', (res) => {
            var center_lat = Number(res.center_lat);
            var center_long = Number(res.center_long);
            var zoom = Number(res.zoom);

            calendarMap(day, month, year, zoom, center_lat, center_long)            
        });
    });
});




