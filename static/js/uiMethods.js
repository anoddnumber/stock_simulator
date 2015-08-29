$( document ).ready(function() {
    $('#loginLink').click(showLoginForm);
    $('#createAccountLink').click(showCreateAccount);

    function showLoginForm() {
        $('#createAccount').hide();
        $('#login').show();
        return false;
    }
    
    function showCreateAccount() {
        $('#login').hide();
        $('#createAccount').show();
        return false;
    }
    
    
    // process the form
    $('createAccount').submit(function(event) {

        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = {
            'username' : $('input[name=username]').val(),
            'password' : $('input[name=password]').val(),
            'email'    : $('input[name=email]').val(),
        };

        // process the form
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url         : 'process.php', // the url where we want to POST
            data        : formData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
            // encode      : true
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                console.log(data); 

                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
    
    function createAccount(username, password, email) {
        $.ajax("/createAccount", {
            method: "POST",
            data: {username : username,
                password : password,
                email : email
            },
            success: function(data) {
                console.log("successfully created account!");
            },
            error: function() {
                console.log("error, did not create account");
            }
        });
    }

}) ;
