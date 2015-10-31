(function($) {
    $.Login = function(options) {
        var login = {
             options : $.extend({
             }, options),

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
            validateCreateAccountData : function(formData) {
                var emptyValue = Utility.hasEmptyValue(formData);
                if (emptyValue) {
                    TopBar.showError("Some fields are empty. Please fill in all of the fields.");
                    return false;
                }

                if (formData.password !== formData.retypePassword) {
                    TopBar.showError("The passwords typed in do not match. Please try again.");
                    return false;
                }

                if (formData.username.indexOf(" ") > -1) {
                    TopBar.showError("The username should not contain any spaces. Please try again.");
                    return false;
                }

                if ( ! validateEmail(formData.email)) {
                    return false;
                }

                return true;
            },

            validateEmail : function(email) {
                if (email.indexOf(" ") > -1) {
                    TopBar.showError("The email should not contain any spaces. Please try again");
                    return false;
                }

                var atIndex = email.indexOf("@");
                if (atIndex < 1) {
                    TopBar.showError("The email address should have characters before @ symbol. Please try again.");
                    return false;
                }

                if (atIndex === email.length - 1) {
                    TopBar.showError("The email address should have character after the @ symbol. Please try again.");
                    return false;
                }

                if ((email.indexOf("@", atIndex + 1) > -1)) {
                    TopBar.showError("Email addresses should only contain a single @ symbol. Please try again");
                    return false;
                }
                return true;
            },

            showLoginForm : function() {
                $('#createAccount').hide();
                $('#login').show();
                return false;
            },

            showCreateAccount : function() {
                $('#login').hide();
                $('#createAccount').show();
                return false;
            }
        }

        return {
            validateCreateAccountData : login.validateCreateAccountData,
            validateEmail : login.validateEmail,
            showLoginForm : login.showLoginForm,
            showCreateAccount : login.showCreateAccount
        };
    }
})(jQuery);
var Login = $.Login();

$( document ).ready(function() {
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

        ApiClient.login(formData);
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

        if (Login.validateCreateAccountData(formData)) {
            ApiClient.createAccount(formData);
        }
    });
}) ;
