$( document ).ready(function() {
    console.log("add_a_trail.js loaded");

    $("#new-trail-form").on('submit', (evt) => {
        evt.preventDefault();
        formInputs = {
            // 'trail_name' : $("input[name=name]").val(),
            'trail_desc' : $("input[name=description]").val(),
            // 'trail_long' : $("input[name=long]").val(),
            // 'trail_lat' : $("input[name=lat]").val(),
            // 'trail_length' : $("input[name=length]").val(),
            // 'length_unit' : $("#length-unit").val(),
            // 'trail_ascent' : $("input[name=ascent]").val(),
            'ascent_unit' : $("#ascent-unit").val(),
            // 'trail_descent' : $("input[name=descent]").val(),
            // 'descent_unit' : $("#descent-unit").val(),
            // 'trail_difficulty' : $("#difficulty").val(),
            // 'trail_location' : $("input[name=location]").val(),
            // 'trail_url' : $("input[name=url]").val(),
            'trail_gps' : $("input[name=gps-file]")[0].files[0],
            // 'trail_gps_url' : $("input[name=gps-link]"),
        }
    
        console.log(formInputs);

    
        // had to use $.ajax() here instead of $.post() so I could set processData
        // to flase - needs to be flase when sending documents 
        $.ajax({ 
            url: '/add-to-db', 
            type: 'post', 
            data: formInputs, 
            processData: false, 
            success: function(res){ 
                if(res != 0){ 
                    alert(res); 
                } 
                else{ 
                    alert('file not uploaded'); 
                } 
            }, 
        });  
        
    });
});