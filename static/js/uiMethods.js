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
    
    // process the create account form when pressing the submit button
    $('#createAccountForm').submit(function(event) {
        
        var formData = {
            'username' : $('input[name=username]').val(),
            'password' : $('input[name=password]').val(),
            'email'    : $('input[name=email]').val(),
        };
        
        createAccount(formData);

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
    
    function createAccount(formData) {
        $.ajax("/createAccount", {
            method: "POST",
            data: formData,
            success: function(data) {
                console.log("successfully created account!");
            },
            error: function() {
                console.log("error, did not create account");
            }
        });
    }

}) ;
