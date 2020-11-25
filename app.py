from collections import namedtuple
import os
from flask import *
import database
import azureFiles
import Domain.FileInfo as fileInfo
import LoginScreen.LoginScreen as login

app = Flask(__name__)
db = database.Database()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
azureHandler = azureFiles.AzureHandler()


@app.route('/')
def indexPage():
    return redirect(url_for('loginPage'))


@app.route('/login', methods=['POST', 'GET'])
def loginPage():
    try:
        error = request.args['error']
        return render_template('Login/index.html',error=error)
    except Exception:
        return render_template('Login/index.html')


@app.route('/handleLogin', methods=['POST'])
def handleLogin():
    result = request.form
    if request.method == 'POST':
        email = result['email']
        password = result['password']
        user = db.loginUser(email, password)
        if user != None:
            session['username'] = user.name
            session['useremail'] = user.email
            # convert object into json so we can pass it to the success function
            return redirect(url_for('successLogin', user=json.dumps(user.__dict__)), code=307)
        else:
            return redirect(url_for('loginPage',error="True"))


@app.route('/autoLogin', methods=['POST'])
def autoLogin():
    email = request.args['email']
    password = request.args['password']
    user = db.loginUser(email, password)
    if user is not None:
        # convert object into json so we can pass it to the success function
        return redirect(url_for('successLogin', user=json.dumps(user.__dict__)))
    else:
        return "Error"


@app.route('/success', methods=['POST', 'GET'])
def successLogin():
    user = request.args['user']
    # convert json back to object format
    userObj = json.loads(user, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return redirect(url_for('mainpage'))


@app.route('/register', methods=['POST', 'GET'])
def registerUser():
    return render_template('Register/register.html')


@app.route('/handleRegister', methods=['POST'])
def handleRegister():
    form = request.form
    if request.method == 'POST':
        registerResult = registerUser(form)
        if registerResult is not None:
            return redirect(url_for('autoLogin', email=registerResult.email, password=registerResult.password))
        else:
            return "Error"


@app.route('/uploadFile', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        selectedFiles = request.files.getlist('files')
        if selectedFiles[0].filename != "":
            uploadFiles = list()
            for file in selectedFiles:
                print(file.filename)
                uploadFileToAzure(file)
                f = fileInfo.FileInfo(file.filename, None, None, azureHandler.convert_size(file.seek(0, 2)),
                                      file.content_type)
                uploadFiles.append(f)
            return render_template('Upload/success.html', username=session['username'], files=uploadFiles)
        return render_template('Upload/upload.html', username=session['username'])
    else:
        return render_template('Upload/upload.html', username=session['username'])


@app.route('/selectFiles', methods=['POST'])
def selectFiles():
    selectedFiles = request.files.getlist('files')
    for file in selectedFiles:
        print(file.filename)
        uploadFileToAzure(file)

    return render_template('Upload/selectedFiles.html', username=session['username'])


@app.route('/mainpage')
def mainpage():
    userEmail = session['useremail']
    files = azureHandler.getFileNames(userEmail)
    return render_template('Mainpage/mainpage.html', username=session['username'], showfiles=files)

@app.route('/downloadFile/<filename>',methods={'GET'})
def downloadFile(filename):
    serverPath = session['useremail'] + "/" + filename
    azureHandler.download_file(serverPath)
    # avoid page redirect
    return (''),204

@app.route('/deleteFile/<filename>',methods=['GET'])
def deleteFile(filename):
    serverPath = session['useremail'] + "/" + filename
    azureHandler.deleteFile(serverPath)
    return redirect(url_for('mainpage'))



@app.route('/logout')
def doLogout():
    session.clear()
    return redirect(url_for('loginPage'))


if __name__ == '__main__':
    app.run()


def registerUser(formResult):
    username = formResult['name']
    email = formResult['email']
    pass1 = formResult['password']
    pass2 = formResult['password2']

    if username is not None and email is not None and pass1 is not None and pass2 is not None:
        if pass1 == pass2:
            result = db.registerUser(username, email, pass1)
            return result
        else:
            return None
    else:
        return None


def uploadFileToAzure(file):
    return azureHandler.uploadfile(file, session['useremail'])
