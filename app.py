from collections import namedtuple

from flask import *
import database
import azureFiles
import LoginScreen.LoginScreen as login

app = Flask(__name__)
db = database.Database()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
azureHandler = azureFiles.AzureHandler()

@app.route('/')
def indexPage():
    db.getUsers()
    return 'Hello World!'


@app.route('/login',methods = ['POST', 'GET'])
def loginPage():
    return render_template('Login/index.html')

@app.route('/handleLogin',methods=['POST'])
def handleLogin():
    result = request.form
    if request.method == 'POST':
        email = result['email']
        password = result['password']
        user = db.loginUser(email, password)
        if user != None:
            session['username'] = user.name
            # convert object into json so we can pass it to the success function
            return redirect(url_for('successLogin',user=json.dumps(user.__dict__)),code=307)
        else:
            return "Error"

@app.route('/autoLogin',methods=['POST'])
def autoLogin():
    email = request.args['email']
    password = request.args['password']
    user = db.loginUser(email,password)
    if user is not None:
        # convert object into json so we can pass it to the success function
        return redirect(url_for('successLogin', user=json.dumps(user.__dict__)))
    else:
        return "Error"


@app.route('/success', methods=['POST', 'GET'])
def successLogin():
    user = request.args['user']
    # convert json back to object format
    userObj = json.loads(user,object_hook= lambda d: namedtuple('X', d.keys())(*d.values()))
    return redirect(url_for('mainpage'))



@app.route('/register',methods=['POST', 'GET'])
def registerUser():
    return render_template('Register/register.html')

@app.route('/handleRegister',methods=['POST'])
def handleRegister():
    form = request.form
    if request.method == 'POST':
        registerResult = registerUser(form)
        if registerResult is not None:
            return redirect(url_for('autoLogin', email=registerResult.email,password=registerResult.password))
        else:
            return "Error"



@app.route('/mainpage')
def mainpage():
    files = azureHandler.getFileNames()
    return render_template('Mainpage/mainpage.html',username=session['username'],showfiles=files)

if __name__ == '__main__':
    app.run()



def registerUser(formResult):
    username = formResult['name']
    email = formResult['email']
    pass1 = formResult['password']
    pass2 = formResult['password2']

    if username is not None and email is not None and pass1 is not None and pass2 is not None:
        if pass1 == pass2:
            result = db.registerUser(username,email,pass1)
            return result
        else:
            return None
    else:
        return None