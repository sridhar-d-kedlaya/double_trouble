import mysql.connector

def connectDB():
    if 'dataBase' not in globals():
        global dataBase
        dataBase = mysql.connector.connect(
            host ="localhost",
            user ="parzival",
            passwd ="zcs4Ft)ASJ'Y-.Nk`5twTs5E/",
            database = "iitb_ctf"
        )
        return dataBase.cursor()
    else:
        try:
            dataBase.ping(reconnect=True)
            return dataBase.cursor()
        except Exception as e:
            print("Error: ", e)
            return False



def closeDB():
    return dataBase.close()

def createUser(username, email, password, firstname, lastname):
    try:
        cursorObject = connectDB()
        qry = """INSERT INTO users (user_name, first_name, last_name, email, password)
VALUES (%s, %s, %s, %s, %s); """
        cursorObject.execute(qry, [username, firstname, lastname, email, password])
        dataBase.commit()
        return True
    except Exception as e:
        print("Error: ", e)
        return False

def loginUser(username, password):
    try:
        cursorObject = connectDB()
        qry = """SELECT * FROM users WHERE user_name=%s and password=%s;"""
        cursorObject.execute(qry, [username, password])
        status = cursorObject.fetchall()
        if status:
            return [True, username, status[0][0]]
        else:
            return False
    except Exception as e:
        print("Error: ", e)
        return False

def checkAdmin(username, id):
    try:
        cursorObject = connectDB()
        qry = """SELECT * FROM users WHERE id=%s AND user_name=%s AND admin=true;"""
        cursorObject.execute(qry, [id, username])
        status = cursorObject.fetchall()
        if status:
            return True
        else:
            return False
    except Exception as e:
        print("Error: ", e)
        return False

def forgotPassword(email):
    try:
        cursorObject = connectDB()
        qry = """ SELECT * FROM users WHERE email='{email}';"""
        qry = qry.format(email=email)
        res = [False, "Error"]
        for result in cursorObject.execute(qry, multi=True):
            if result.with_rows:
                status = result.fetchall()
                res = [True, status[0][5]]
            else:
                res = [False, "Error"]
                continue
        return res
    except Exception as e:
        print("Error: ", e)
        return [False, e]
