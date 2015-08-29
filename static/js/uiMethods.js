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
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
        
        var formData = {
            'username' : $('#createAccountForm input[name=username]').val(),
            'password' : $('#createAccountForm input[name=password]').val(),
            'retypePassword' : $('#createAccountForm input[name=retypePassword]').val(),
            'email'    : $('#createAccountForm input[name=email]').val(),
        };
        
        if (formData.password !== formData.retypePassword) {
            console.log("password does not match the retyped password");
        } else {
            createAccount(formData);
        }
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
