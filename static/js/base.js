
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

    $("#log-out").on('click', (evt) => {
        evt.preventDefault();

        
        $.get("/log-out");

        setTimeout(() => {  location.reload(true); }, 100);

    });
});






