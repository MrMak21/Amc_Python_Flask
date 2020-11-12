import mysql.connector
import uuid
import Domain.User as user

createUsersQuery = "CREATE TABLE IF NOT EXISTS Users (UserId VARCHAR(255), Name VARCHAR(255), Email VARCHAR(255), Password VARCHAR(255)           )"
insertUsersQuery = "INSERT INTO Users (UserId,name,email,password) VALUES(%s, %s, %s, %s)"
readUsersQuery = "SELECT * FROM Users"

class Database(object):

    cursor = None

    def __init__(self):
        print("Initializing database")
        try:
            self.db = mysql.connector.connect(
                host="makrisdatabase.mysql.database.azure.com"
                , user="pmakris@makrisdatabase"
                , password="Panosaek1997"
                , database="amcflaskdb")

            self.cursor = self.db.cursor()

        except Exception as ex:
            print(ex)
            self.db = None
            # raise Exception(ex)

    def query(self,query):
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            resultSet = cursor.fetchall()
            cursor.close()
            return resultSet
        except Exception as err:
            raise Exception(err)




    def getUsers(self):
        db = self.db
        if db != None:
            if db.is_connected():
                print(db)
                cursor = db.cursor()
                cursor.execute(createUsersQuery)

                val = (str(uuid.uuid4()), "Stavros Megremis", "meg@gmail.com", "Meg")
                # cursor.execute(insertUsersQuery,val)
                # db.commit()

                cursor.execute(readUsersQuery)
                result = cursor.fetchall()
                if len(result) > 0:
                    for user in result:
                        print(user[1] + " " + user[2])

        else:
            print("Cannot connect")


    def loginUser(self,email,password):
        db = self.db
        if db != None:
            self.cursor.execute("Select * from Users u Where u.email = '" + email + "' and u.password = '" + password + "'")
            result = self.cursor.fetchone()
            if result != None:
                if len(result) > 0:
                    userObj = user.User(result[0],result[1],result[2],result[3])
                    return userObj
            else:
                return None