import simulator

class StockSimulatorTestRequestContext:

    def get_logout_context(self):
        return simulator.app.test_request_context("/logout",
                method="POST", data={
                "email" : "test_email@gmail.com",
                "username" : "test_user_name",
                "password" : "password",
                "retypePassword" : "password"
            })

    # Example:
    # a = StockSimulatorTestRequestContext()
    # with a.get_create_account_context():
    #     print "request.form: " + str(request.form.get("username"))
    def get_create_account_context(self):
        return simulator.app.test_request_context("/createAccount",
                method="POST", data={
                "email" : "test_email@gmail.com",
                "username" : "test_user_name",
                "password" : "password",
                "retypePassword" : "password"
            })