// potentially create an initMap functiona and a calendarMap function 

console.log('base.js has been loaded')


$( document ).ready(function() {
    
    $('#date-form').on('submit', (evt) => {
        evt.preventDefault();
        
        const date = $('#calendar').val();
        const year = date.slice(0,4);
        const month = date.slice(5,7);
        const day = date.slice(8);

    
        console.log('date:' + date.slice(8));

        calendarMap(day, month, year);
    });


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
                $("#trail-table").append("<tr><th>Trail Name</th><th>Length</th><th>Location</th><th>Favorite Trail</th></tr>");
                
                for (var trail of res) {
                        $("#trail-table").append(`
                            <tr>
                                <td><a href=${trail['trail_url']}>${trail['trail_name']}</a></td>
                                <td>${trail['trail_distance']}</td>
                                <td>${trail['trail_location']}</td>
                                <td><button id=${trail['trail_id']} class="favorite-button">Add Trail to Favorites</button></td>
                            </tr>`
                        );
                }
                $('.favorite-button').on('click', () => {
                    console.log('favorite-button clicked');
            
                });

            } else { 
                console.log('response empty');                
                alert('No trails found with that filtering criteria.'); 
            }
        });
    }); 
});



