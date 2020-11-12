from collections import namedtuple

from flask import *
import database
import LoginScreen.LoginScreen as login

app = Flask(__name__)
db = database.Database()

@app.route('/')
def indexPage():
    db.getUsers()
    return 'Hello World!'


@app.route('/login',methods = ['POST', 'GET'])
def loginPage():
    return render_template('Login/login.html')

@app.route('/handleLogin',methods=['POST'])
def handleLogin():
    result = request.form
    if request.method == 'POST':
        username = result['name']
        password = result['password']
        user = db.loginUser(username, password)
        if user != None:
            return redirect(url_for('successLogin',user=json.dumps(user.__dict__)))
        else:
            return "Error"

@app.route('/success', methods=['POST', 'GET'])
def successLogin():
    user = request.args['user']
    userObj = json.loads(user,object_hook= lambda d: namedtuple('X', d.keys())(*d.values()))
    return "success " + userObj.name + " " + userObj.email


def customStudentDecoder(dict):
    return namedtuple('X', dict.keys())(*dict.values())

if __name__ == '__main__':
    app.run()
