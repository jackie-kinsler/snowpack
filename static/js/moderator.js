
console.log('moderator.js has been loaded')


$( document ).ready(function() {
    
    $(".add-to-trail-db-button").on('click', (evt) => {
        evt.preventDefault();

        var suggestionId = $(event.target).attr("id");

        formInputs = {
            'suggestion_id' : suggestionId,
        };

        $.get('/moderator/add-suggestion-to-db', formInputs, (res) => {
            alert(res);
        }); 
    });

    
});


