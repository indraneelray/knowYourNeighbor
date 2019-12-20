from flask import Flask, jsonify, session, render_template, redirect, url_for, make_response, request,escape
import bcrypt,hashlib,binascii,os


class ServerError(Exception): pass


def signup(db, conn, form, ROUNDS):
    error = None
    try:
        print("in signup")
        #username = form['username']
        password = form['password']
        email = form['email']
        firstname = form["fname"]
        lastname = form["lname"]
        phone_number = "12345678"
        apartment_no = form["addressLine1"]
        street = form["addressLine2"]
        city = form["city"]
        state = form["state"]
        zipcode = form["xipcode"]
        gender = form["gender"]
        user_bio = form["user_bio"]
        email_preference = form["email_pref"]
        if email_preference == "yes":
            email_preference = 1
        else:
            email_preference = 0

        if not password or not email:
            raise ServerError('Fill in all fields')

        new_password = hash_password(password)
        #new_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))
        print("passord is:",password)


        cursor = conn.cursor()
        print("cursor is:", cursor)
        cursor.execute("SELECT COUNT(*) FROM user_signup WHERE email = %s", [email])
        c = cursor.fetchone()
        print("c is:",c)
        if c[0] == 0:
            print("in executing queries")
            try:
                cursor.execute(
                    """INSERT INTO user_signup (`email`, `password`, `signup_at`, `updated_at`) VALUES (%s,%s,NOW(),NOW())""",
                    [email, new_password])
                print("new_password is:",new_password)
                cursor.execute("Select userid from user_signup where email = %s ", [email])
                print("email fecth executed")
                d = cursor.fetchone()
                uid = d[0]
                #session['uid'] = uid
                print("uid is:",uid)
                cur = cursor.execute(
                    """INSERT INTO user_details (`userid`,`firstname`,`lastname`,`email`, `phone_number`, `gender`, `user_bio`,`email_preference`,`apartment_no`,`street`,`city`,`state`,`zipcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    [int(uid), firstname, lastname, email, phone_number, gender, user_bio, email_preference,
                     apartment_no, street, city, state, int(zipcode)])
                conn.commit()
                if 'uid' not in  session:
                    session['uid'] = str(uid)
                    print((session['uid']))
                # if session:
                #     print("session object in try:", session)
                # else:
                #     print('session is null')
                #     db.createSession(str(uid))
                return None
            except:
                print("in rollback")
                conn.rollback()
                error = "Error"
                return error
        else:
            return "User exists"
    except ServerError as e:
        error = str(e)
        return error


def getUser(db, form):
    error = None
    try:
        email = form['Username']
        password = form['password']

        if not password or not email:
            raise ServerError('Fill in all fields')

        cur = db.query("""SELECT COUNT(1) FROM user_signup where email = %s""", [email])
        print("fetch email in login:",cur)
        if not cur.fetchone()[0] == 1:
            print("in check")
            raise ServerError('Incorrect username / password')

        cur2 = db.query("""SELECT * from user_details WHERE email = %s""", [email])
        print("fetch email in login:", cur2)
        query_row = cur2.fetchall()[0]
        userid = query_row[0]
        print("userid:",userid)
        cur = db.query("""SELECT password FROM user_signup WHERE email = %s;""", [email])
        # print(cur.fetchall())
        for row in cur.fetchall():
            print("password:",row[0])
            #new_password = hash_password(password)
            #new_password = password
            if verify_password(row[0],password):
                session['uid'] = str(userid)
                print("password match:")
                return None
            else:
                raise ServerError('Incorrect username / password')
    except ServerError as e:
        error = str(e)
        return error


def update_password(conn, form):
    error = None
    print("update password")
    try:
        old_password= form["old_password"]
        new_password= form["new_password"]
        userid = session['uid']
        print(old_password)
        print(new_password)
        if not old_password or not new_password:
            raise ServerError('Fill in all fields')
        cursor = conn.cursor()
        cursor.execute("""SELECT password FROM user_signup WHERE userid = %s""", [userid])
        c = cursor.fetchone()
        print(c[0])
        if c[0] == old_password:
            cursor.execute(
                """UPDATE user_signup set password = %s and updated_at = NOW() where userid = %s""",
                [new_password, userid])
            conn.commit()
            return None
        else:
            raise ServerError("Existing password entered doesn't match our records")
    except ServerError as e:
        error = str(e)
        return error


def update_block_details(conn, form):
    error = None
    try:
        blockid = ""
        if not blockid:
            raise ServerError('Fill in all fields')
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM user_signup WHERE userid = %s""", [userid])
        c = cursor.fetchone()
        if c[0] == 1:
            cursor.execute("""SELECT blockid from user_details where userid= %s""", [userid])
            d = cursor.fetchone()
            if d[0] != "NULL":
                cursor.execute("""UPDATE user_details set blockid = %s where userid = %s""", [blockid, userid])
                conn.commit()
                return None
            else:
                raise ServerError("Block is not null")
        else:
            raise ServerError("User does not exist")
    except ServerError as e:
        error = str(e)
        return error


def view_profile(conn, form):
    error = None
    cursor = conn.cursor()
    profile_details = []
    #email = "sunidhi.4@nyu.com"
    userid = session['uid']

    try:
        cursor.execute("""select * from user_details where userid = %s""", [userid])
        c = cursor.fetchone()
        if c is not None:
            print("c is:", c)
            return c
        else:
            raise ServerError("User does not exist")
    except ServerError as e:
        error = str(e)
        return error


def update_profile_details(conn, form):
    error = None
    try:
        userid=session['uid']
        firstname = ""
        lastname = ""
        phonenumber = ""
        user_bio = ""
        apartment_no = ""
        street = ""
        city = ""
        state = ""
        zipcode = ""

        cursor = conn.cursor()
        try:
            if firstname:
                cursor.execute("UPDATE user_details set firstname = %s where userid = %s", [firstname, userid])
            if lastname:
                cursor.execute("UPDATE user_details set lastname = %s where userid = %s", [lastname, userid])
            if phonenumber:
                cursor.execute("UPDATE user_details set phone_number = %s where userid = %s", [phonenumber, userid])
            if user_bio:
                cursor.execute("UPDATE user_details set user_bio = %s where userid = %s", [user_bio, userid])
            if apartment_no:
                cursor.execute("UPDATE user_details set apartment_no = %s where userid = %s", [apartment_no, userid])
            if city:
                cursor.execute("UPDATE user_details set city = %s where userid = %s", [city, userid])
            if street:
                cursor.execute("UPDATE user_details set street = %s where userid = %s", [street, userid])
            if state:
                cursor.execute("UPDATE user_details set state = %s where userid = %s", [state, userid])
            if zipcode:
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


def logout(conn):
    error = None
    try:
        userid = session['uid']
        print("userid:",userid)
        cursor=conn.cursor()
        cursor.execute("""UPDATE user_details set logout_at = NOW() where userid = %s""", [userid])
        conn.commit()
        return None
    except:
        print("not updated logout at")
        error = "Failed"
        return error


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password