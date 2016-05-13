from flask_wtf import Form
from wtforms import StringField
from flask_security.forms import RegisterForm
import logging
from flask import request
import urllib
import urllib2
import json
from wtforms.validators import DataRequired


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [DataRequired()])
    recaptcha = StringField()

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.recaptcha_secret_key = '6Lf7ZBoTAAAAAHIKbm4AnecJxycyM5PIjmWt3eO_'

    def validate(self):
        from simulator import config, stock_user_datastore

        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            self.logger.warning("Standard Flask-Security register validators failed")
            return False

        # Check if username already exists
        user = stock_user_datastore.find_user(username=self.username.data)
        if user is not None:
            # Text displayed to the user
            self.username.errors.append('Username already taken')
            return False

        if " " in self.username.data:
            self.logger.warning("User tried to create an account with a space in it.")
            self.username.errors.append('Username cannot contain spaces')
            return False

        # if statement for unit tests to bypass recaptcha
        if not config.get("DEBUG"):
            captcha = request.form.get('g-recaptcha-response')
            if not captcha:
                self.logger.warning("Recaptcha was not in the create account request")
                self.recaptcha.errors.append('Please prove you are human with the captcha')
                return False

            self.logger.info("captcha: " + str(captcha))

            data = urllib.urlencode({'secret': self.recaptcha_secret_key,
                                    'response': captcha})
            u = urllib2.urlopen('https://www.google.com/recaptcha/api/siteverify', data)
            google_response = u.read()
            self.logger.info("Google responded to captcha with " + str(google_response))

            google_json = json.loads(google_response)
            self.logger.info('google_json.get("success"): ' + str(google_json.get("success")))

            if not google_json.get("success"):
                self.logger.warning("User tried creating an account but failed because reCaptcha failed")
                self.recaptcha.errors.append('Please prove you are human with the captcha again')
                return False

        return True
