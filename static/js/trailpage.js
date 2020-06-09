
console.log('trailpage.js has been loaded')


$( document ).ready(function() {

    $("#distance-form").on('submit', (evt) => {
        
        evt.preventDefault();

        formInputs = {
            'min_dist' : $('#min-dist').val(),
            'max_dist' : $('#max-dist').val()
        };        
        
        $.get('/filtered-trails', formInputs, (res) => {
            console.log(res);
                        
            if (res.length !== 0) {

                $("#filtered-trails").empty();
                $("#filtered-trails").text("Trails filtered by distance:");
                $("#trail-table").empty();
                $("#trail-table").append(`
                    <tr>
                        <th>Trail Name</th>
                        <th>Length</th>
                        <th>Location</th>
                        <th>Favorite Trail</th>
                        <th>Show On Map (only available for certain trails)</th>
                    </tr>`
                );
                
                for (var trail of res) {
                    if (trail['trail_gps']) {
                        $("#trail-table").append(`
                            <tr>
                                <td><a href=${trail['trail_url']}>${trail['trail_name']}</a></td>
                                <td>${trail['trail_distance']}</td>
                                <td><a href=https://www.google.com/maps/dir/Current+Location/${trail['trail_lat']},${trail['trail_long']}>${trail['trail_location']}</a></td>
                                <td><button id=${trail['trail_id']} class="favorite-button">Add Trail to Favorites</button></td>
                                <td><button id=${trail['trail_gps']} class="display-button" title="${trail['trail_lat']}:${trail['trail_long']}">Display Trail on Map</button></td>
                            </tr>`
                        );
                    } else {
                        $("#trail-table").append(`
                            <tr>
                                <td><a href=${trail['trail_url']}>${trail['trail_name']}</a></td>
                                <td>${trail['trail_distance']}</td>
                                <td><a href=https://www.google.com/maps/dir/Current+Location/${trail['trail_lat']},${trail['trail_long']}>${trail['trail_location']}</a></td>
                                <td><button id=${trail['trail_id']} class="favorite-button">Add Trail to Favorites</button></td>
                            </tr>`
                        );
                    }
                }
                $('.favorite-button').on('click', () => {
                    console.log('favorite-button clicked');

                    var trailId = $(event.target).attr("id");
                    
                    formInputs = {
                        'trail_id' : trailId,
                    }
                    
                    $.get('/add-to-favorites', formInputs, (res) => {
                        alert(res);
                    });
                });

                $('.display-button').on('click', () => {
                    console.log('you clicked?');

                    var url = $(event.target).attr("id");

                    // this gets the latLong of the trailhead, then splits it
                    // into an array of the format latLong = [latitude, longitude]
                    var latLong = $(event.target).attr("title").split(":");

                    var today = new Date();
                    var day = String(today.getDate()).padStart(2, '0');
                    var month = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                    var year = today.getFullYear();
                    
                    var initial_zoom = 10;

                    calendarMap(day, month, year, url, Number(latLong[0]), Number(latLong[1]), initial_zoom, Number(latLong[0]), Number(latLong[1]));

                });

            } else { 
                console.log('response empty');                
                alert('No trails found with that filtering criteria.'); 
            }
        });
    }); 
});






