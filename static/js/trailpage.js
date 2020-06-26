console.log('trailpage.js has been loaded')


$( document ).ready(function() {
    
    $("#distance-form").on('submit', (evt) => {

        evt.preventDefault();

        const trailName = $('#trail-name').val();
        const minDist = $('#min-dist').val();
        const maxDist = $('#max-dist').val();

        if (!trailName && !minDist && !maxDist) {
            alert("Please enter at least one filtering parameter");
            return;
        }

        formInputs = {
            'trail_name' : trailName,
            'min_dist' : minDist,
            'max_dist' : maxDist,
        }        
        
        $.get('/api/filtered-trails', formInputs, (res) => {

            if (res.length) {
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
                // for each trail that matches the filtering criterion, 
                // create a data row in the table 
                // if the trail has gps data, a button to show the GPS data on the map will appear
                // otherwise, a button to show the trailhead on the map will appear
                for (var trail of res) {
                    if (trail['trail_gps']) {
                        $("#trail-table").append(`
                            <tr>
                                <td><a href=${trail['trail_url']}>${trail['trail_name']}</a></td>
                                <td>${trail['trail_distance']}</td>
                                <td><a href=https://www.google.com/maps/dir/Current+Location/${trail['trail_lat']},${trail['trail_long']}>${trail['trail_location']}</a></td>
                                <td><button id=${trail['trail_id']} class="favorite-button">Add to favorites</button></td>
                                <td><button id=${trail['trail_gps']} class="display-button" title="${trail['trail_lat']}:${trail['trail_long']}">View GPS</button></td>
                            </tr>`
                        );
                    } else {
                        $("#trail-table").append(`
                            <tr>
                                <td><a href=${trail['trail_url']}>${trail['trail_name']}</a></td>
                                <td>${trail['trail_distance']}</td>
                                <td><a href=https://www.google.com/maps/dir/Current+Location/${trail['trail_lat']},${trail['trail_long']}>${trail['trail_location']}</a></td>
                                <td><button id=${trail['trail_id']} class="favorite-button">Add to favorites</button></td>
                                <td><button class="display-button" title="${trail['trail_lat']}:${trail['trail_long']}">View trailhead</button></td>
                            </tr>`
                        );
                    }
                }

                $('.favorite-button').on('click', () => {

                    var trailId = $(event.target).attr("id");
                    
                    formInputs = {
                        'trail_id' : trailId,
                    }
                    
                    $.get('/add-to-favorites', formInputs, (res) => {
                        alert(res);
                    });
                });

                $('.display-button').on('click', () => {

                    var url = $(event.target).attr("id");

                    // this gets the latLong of the trailhead, then splits it
                    // into an array of the format latLong = [latitude, longitude]
                    var latLong = $(event.target).attr("title").split(":");
                    
                    var initial_zoom = 10;

                    $.get('/api/latest-date', (res) => {
                        // response is a string of format yyyy-mm-dd
                        var year = String(res.slice(0, 4));
                        var month = String(res.slice(5, 7));
                        var day = String(res.slice(8));

                        trailMap(day, month, year, url, 
                                 Number(latLong[0]), Number(latLong[1]), 
                                 initial_zoom, Number(latLong[0]), Number(latLong[1]));
                        
                        $("#date-notice-box").text(`(data from ` + 
                                    `${month}-${day}-${year})`); 
                    });
                });
            } else {
                alert("No trails found with that filtering criteria.");
            }
        });
    }); 
});






