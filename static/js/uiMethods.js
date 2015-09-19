$( document ).ready(function() {
    $('#loginPageLink').click(function() {
        changePage('loginPage');
    });
    
    $('#stockTablePageLink').click(function() {
        changePage('stockTablePage');
    });
    
    $('#loginLink').click(showLoginForm);
    $('#createAccountLink').click(showCreateAccount);
    $('#createAccountLink').click(showCreateAccount);
    $('#logoutButton').click(logout);
    

    function changePage(page) {
        $('#tabs > div').hide();
        $('#' + page).show();
    }
    
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
    
    // process the login form when pressing the submit button
    $('#loginForm').submit(function(event) {
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
        
        var formData = {
            'username' : $('#loginForm input[name=username]').val().trim(),
            'password' : $('#loginForm input[name=password]').val(),
        };
        
        var passwordFields = $(':input[type="password"]');
        passwordFields.val('');
        
        login(formData);
    });
    
    // process the create account form when pressing the submit button
    $('#createAccountForm').submit(function(event) {
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
        
        var formData = {
            'username' : $('#createAccountForm input[name=username]').val().trim(),
            'password' : $('#createAccountForm input[name=password]').val(),
            'retypePassword' : $('#createAccountForm input[name=retypePassword]').val(),
            'email'    : $('#createAccountForm input[name=email]').val().trim(),
        };
        
        if (validateCreateAccountData(formData)) {
            createAccount(formData);
        }
    });
    
    function showError(errorMsg) {
        $('#errorBox').text(errorMsg);
        $('#errorBox').show();
    }
    
    /**
     * Gets the error message from a jqXHR (jQuery XMLHttpRequest) object.
     */
    function showErrorFromJqXHR(jqXHR) {
        var obj = JSON.parse(jqXHR.responseText);
        showError(obj.message);
    }
    
    /*
     * Note that this does not mean we do not need to validate on the backend.
     * The backend check should do the same validation checks as here.
     * This validation just makes it so normal users gets fast feedback on what they did wrong.
     * 
     * We have to validate the following things:
     *      - all fields have information (not blank)
     *      - make sure that the password and retyped password are the same.
     *      - make sure the username does not contain illegal characters (like spaces)
     *      - the email address has one and only one @ symbol and letters before and after the @ symbol and does not contain spaces
     */
    function validateCreateAccountData(formData) {
        var emptyValue = hasEmptyValue(formData);
        if (emptyValue) {
            showError("Some fields are empty. Please fill in all of the fields.");
            return false;
        }
        
        if (formData.password !== formData.retypePassword) {
            showError("The passwords typed in do not match. Please try again.");
            return false;
        }
        
        if (formData.username.indexOf(" ") > -1) {
            showError("The username should not contain any spaces. Please try again.");
            return false;
        }
        
        if ( ! validateEmail(formData.email)) {
            return false;
        }
        
        return true;
    }
    
    function validateEmail(email) {
        if (email.indexOf(" ") > -1) {
            showError("The email should not contain any spaces. Please try again");
            return false;
        }
        
        var atIndex = email.indexOf("@");
        if (atIndex < 1) {
            showError("The email address should have characters before @ symbol. Please try again.");
            return false;
        }
        
        if (atIndex === email.length - 1) {
            showError("The email address should have character after the @ symbol. Please try again.");
            return false;
        }
        
        if ((email.indexOf("@", atIndex + 1) > -1)) {
            showError("Email addresses should only contain a single @ symbol. Please try again");
            return false;
        }
        return true;
    }
    
    /*
     * If one of the properties is undefined or an empty string, return the property.
     * Otherwise returns false.
     */
    function hasEmptyValue(object) {
        for (var property in object) {
            /*
             * hasOwnProperty is necessary because an object's prototype contains additional properties for the object which are technically part of the object.
             * These additional properties are inherited from the base object class, but are still properties of object.
             * hasOwnProperty simply checks to see if this is a property specific to this class, and not one inherited from the base class.
             */
            if (object.hasOwnProperty(property)) {
                if (object[property] === undefined || object[property] === '') {
                    return property;
                }
            }
        }
        return false;
    }
    
    function login(formData) {
        $.ajax("/login", {
            method: "POST",
            data: formData,
            success: function(data) {
                console.log(data);
                $('#usernameBox').text(formData.username);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showErrorFromJqXHR(jqXHR);
                console.log("error, did not login");
            }
        });
    }
    
    function logout() {
        $.ajax("/logout", {
            method: "POST",
            success: function(data) {
                console.log(data);
                $('#usernameBox').text("Not logged in");
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showErrorFromJqXHR(jqXHR);
                console.log("error, did not login");
            }
        });
    }
    
    function createAccount(formData) {
        $.ajax("/createAccount", {
            method: "POST",
            data: formData,
            success: function(data) {
                console.log("successfully created account!");
            },
            error: function(jqXHR, textStatus, errorThrown ) {
                showErrorFromJqXHR(jqXHR);
            }
        });
    }

}) ;
