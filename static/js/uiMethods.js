$( document ).ready(function() {
    $('#loginLink').click(showLoginForm);
    $('#createAccountLink').click(showCreateAccount);

    function showLoginForm() {
        $('#createAccount').hide();
        $('#login').show();
    }
    
    function showCreateAccount() {
        $('#login').hide();
        $('#createAccount').show();
    }
}) ;
