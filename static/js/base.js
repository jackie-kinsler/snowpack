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
        console.log(formInputs);
        

        $.get('/filtered-trails', formInputs, (res) => {
            console.log(res);
            $("#filtered-trails").empty();
            $("#filtered-trails").text("Trails filtered by distance:");
            
            for (var trail of res) {
                $("#filtered-trails").append(`<li><a href=${trail['trail_url']}>${trail['trail_name']}</a></li>`);
            }
        })
    });
});



