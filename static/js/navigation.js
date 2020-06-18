
console.log('navigation.js has been loaded')

function logOutElement() {
    $('#user-credentials').append('<button id="log-out">LOG OUT</button>');
    $("#log-out").on('click', (evt) => {
        evt.preventDefault();
        
        $.get("/api/log-out");

        setTimeout(() => {  location.reload(true); }, 100);
    });
}

$( document ).ready(function() {

    $.get('/api/is-logged-in', (res) => {
        if (res === 'false') {
            $('#user-credentials').append(`
                <h3>Log In:</h3>
                <form id="log-in-form">
                    Email <input type="text" name="email">
                    Password <input type="password" name="password">
                    <input type="submit">
                </form>
                <h3>Not on FlakeMap? Create an account!</h3>
                <form action="/api/create-user" method="POST">
                    Email <input type="text" name="email">
                    Password <input type="password" name="password">
                    <input type="submit">
                </form>`);

            $("#log-in-form").on('submit', (evt) => {
                evt.preventDefault();
        
                const formValues = $("#log-in-form").serialize();
        
                $.get("/api/log-in", formValues, (res) => {
                    if (res === 'success') {
                        $('#user-credentials').empty();
                        logOutElement();

                    } else {
                        alert("Log-in Failed");
                        document.getElementById('log-in-form').reset();
                    }
                });
                
                setTimeout(() => {  location.reload(true); }, 100);
            });
        } else {
            logOutElement();
        }
    });
});