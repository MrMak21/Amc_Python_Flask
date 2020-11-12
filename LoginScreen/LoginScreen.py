from flask import Flask

class LoginScreen(object):
    app = Flask


    def __init__(self,app,db):
        self.app = app
        self.db = db

    def login(self,email,password):
        print(email + " " + password)