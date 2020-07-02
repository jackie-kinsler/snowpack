$( document ).ready(function() {
    
    $(".add-to-trail-db-button").on('click', (evt) => {
        evt.preventDefault();
        
        var suggestionId = $(event.target).attr("id");

        formInputs = {
            'suggestion_id' : suggestionId,
        };

        $.post('/moderator/add-to-trail-db', formInputs, (res) => {
            alert(res);
        }); 

        $.post('/moderator/delete-suggestion', formInputs);

        setTimeout(() => {  location.reload(true); }, 300);
    });

    $(".delete-button").on('click', (evt) => {
        evt.preventDefault();

        var suggestionId = $(event.target).attr("id");

            formInputs = {
                'suggestion_id' : suggestionId,
            };

        if (window.confirm("Are you sure you want to delete this suggestion?" +
                            " It cannot be undone!!")) {
            
            $.post('/moderator/delete-suggestion', formInputs);
            
            // pass true to reload page from server instead of from cache 
            setTimeout(() => {  location.reload(true); }, 200);
        }
    });
});


