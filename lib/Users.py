from flask import Flask , jsonify
import bcrypt

class ServerError(Exception):pass

def signup(conn,form,ROUNDS):
    error = None
    try:
        #password = form['password']
        #email = form['email']
        password = "abcd"
        email ="sunidhi.6@nyu.com"
        firstname = "sunidhi"
        lastname ="brajesh"
        phone_number = "+919916039335"
        gender= "Female"
        user_bio= ""
        email_preference= "1"
        apartment_no= "B4"
        street= "68th street"
        city = "Brooklyn"
        state="New York"
        zipcode="11220"

        if not password or not email:
            raise ServerError('Fill in all fields')

        new_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_signup WHERE email = %s", [email])
        c = cursor.fetchone()
        if c[0] == 0:
            try:
                cursor.execute("INSERT INTO user_signup (`email`, `password`, `signup_at`, `updated_at`) VALUES (%s,%s,NOW(),NOW())",[email, new_password])
                cursor.execute("Select userid from user_signup where email = %s ",[email])
                d = cursor.fetchone()
                uid=d[0]
                cur = cursor.execute("INSERT INTO user_details (`userid`,`firstname`,`lastname`,`email`, `phone_number`, `gender`, `user_bio`,`email_preference`,`apartment_no`,`street`,`city`,`state`,`zipcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [int(uid),firstname,lastname,email,phone_number,gender,user_bio,email_preference,apartment_no,street,city,state,int(zipcode)])
                conn.commit()
            except:
                print("in rollback")
                conn.rollback()
                error ="Error"
                return error
            return None
        else:
            return "User exists"
    except ServerError as e:
        error = str(e)
        return error

def getUser(db,form):
    error = None
    try:
        email = "sunidhi@nyu.com"
        password = "abcd"
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        string_password = hashed_password.decode('utf8')

        if not password or not email:
            raise ServerError('Fill in all fields')

        cur = db.query("SELECT COUNT(1) FROM user_signup where email = %s",[email])

        #if not cur.fetchone()[0]:
            #raise ServerError('Incorrect username / password')
        if not cur.fetchone()[0] == 1:
            print("in check")
            raise ServerError('Incorrect username / password')

        cur = db.query("SELECT password FROM user_signup WHERE email = %s;", [email])
        #print(cur.fetchall())
        for row in cur.fetchall():
            print(type(row))
            if bcrypt.hashpw(string_password.encode('utf-8'), row[0].encode('utf-8')) == row[0]:
                #session['username'] = form['username']
                print("password match:")
                return error

        #raise ServerError('Incorrect username / password')
    except ServerError as e:
        error = str(e)
        return error

def update_password(conn, form):
    error = None
    try :
        password = ""
        userid = ""
        if not password:
            raise ServerError('Fill in all fields')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_signup WHERE userid = %s", [userid])
        c = cursor.fetchone()
        if c[0] == 1:
            cursor.execute(
            "UPDATE user_signup set password = %s and updated_at = NOW() where userid = %s",
            [password,userid])
            conn.commit()
            return None
        else:
            raise ServerError("User doesnt exist'")
    except ServerError as e:
        error = str(e)
        return error



def  update_block_details(conn,form):
    error = None
    try:
        blockid=""
        if not password:
            raise ServerError('Fill in all fields')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_signup WHERE userid = %s", [userid])
        c = cursor.fetchone()
        if c[0] == 1:
            cursor.execute("SELECT blockid from user_details where userid= %s",[userid])
            d = cursor.fetchone()
            if d[0] != "NULL":
                cursor.execute("UPDATE user_details set blockid = %s where userid = %s",[blockid,userid])
                conn.commit()
                return None
            else:
                raise ServerError("Block is not null")
        else:
            raise ServerError("User does not exist")
    except ServerError as e:
        error = str(e)
        return error

def view_profile(conn,form):
    error =None
    cursor = conn.cursor()
    profile_details = []
    email="sunidhi.4@nyu.com"
    try:
        cursor.execute("select * from user_details where email = %s",[email])
        c = cursor.fetchone()
        if c is not None:
            print("c is:",c)
            return jsonify(c)
        else :
            raise ServerError("User does not exist")
    except ServerError as e:
        error = str(e)
        return error


def update_profile_details(conn,form):
    error =None
    try:
        firstname = ""
        lastname =""
        phonenumber=""
        user_bio=""
        apartment_no=""
        street=""
        city=""
        state=""
        zipcode=""

        cursor = conn.cursor()
        try:
            if firstname:
                cursor.execute("UPDATE user_details set firstname = %s where userid = %s",[firstname,userid])
            if lastname :
                cursor.execute("UPDATE user_details set lastname = %s where userid = %s", [lastname, userid])
            if phonenumber:
                cursor.execute("UPDATE user_details set phone_number = %s where userid = %s", [phonenumber, userid])
            if user_bio :
                cursor.execute("UPDATE user_details set user_bio = %s where userid = %s", [user_bio, userid])
            if apartment_no :
                cursor.execute("UPDATE user_details set apartment_no = %s where userid = %s", [apartment_no, userid])
            if city :
                cursor.execute("UPDATE user_details set city = %s where userid = %s", [city, userid])
            if street :
                cursor.execute("UPDATE user_details set street = %s where userid = %s", [street, userid])
            if state :
                cursor.execute("UPDATE user_details set state = %s where userid = %s", [state, userid])
            if zipcode :
                cursor.execute("UPDATE user_details set zipcode = %s where userid = %s", [zipcode, userid])
            conn.commit()
            return None
        except:
            print("in rollback")
            conn.rollback()
            error = "Error in database update"
            return error
    except ServerError as e:
        error = str(e)
        return error





















