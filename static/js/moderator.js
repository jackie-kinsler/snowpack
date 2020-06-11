
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

    $(".delete-button").on('click', (evt) => {
        evt.preventDefault();

        if (window.confirm("Are you sure you want to delete this suggestion?" +
                            " It cannot be undone!!")) {
            var suggestionId = $(event.target).attr("id");

            formInputs = {
                'suggestion_id' : suggestionId,
            };
    
            $.get('/moderator/delete-suggestion', formInputs);
            
            location.reload();
        }
    });
});


