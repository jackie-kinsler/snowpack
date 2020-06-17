
console.log('navigation.js has been loaded')


$( document ).ready(function() {



    $("#log-out").on('click', (evt) => {
        evt.preventDefault();

        
        $.get("/api/log-out");

        setTimeout(() => {  location.reload(true); }, 100);

    });

    $("#log-in-form").on('submit', (evt) => {
        evt.preventDefault();

        const formValues = $("#log-in-form").seralize();
        console.log(formValues);


        // $.get("/api/log-in", formValues)
    });
});






