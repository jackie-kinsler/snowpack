$( document ).ready(function() {
    console.log("add_a_trail.js loaded");

    $("#new-trail-form").on('submit', (evt) => {
        evt.preventDefault();
        formInputs = {
            'trail_name' : $("input[name=name]").val(),
            'trail_desc' : $("input[name=description]").val(),
            'trail_long' : $("input[name=long]").val(),
            'trail_lat' : $("input[name=lat]").val(),
            'trail_length' : $("input[name=length]").val(),
            'length_unit' : $("#length-unit").val(),
            'trail_ascent' : $("input[name=ascent]").val(),
            'ascent_unit' : $("#ascent-unit").val(),
            'trail_descent' : $("input[name=descent]").val(),
            'descent_unit' : $("#descent-unit").val(),
            'trail_difficulty' : $("#difficulty").val(),
            'trail_location' : $("input[name=location]").val(),
            'trail_url' : $("input[name=url]").val(),

        }
    
        console.log(formInputs);
    });
});