from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import bcrypt
import logging
class ServerError(Exception):pass

def loginForm(db, form):
	logging.info('Users login')
	error = None
	try:
		username = form['Username']
		cur = db.query("SELECT COUNT(1) FROM SignUp_Details WHERE username = %s", [username])
		if not cur.fetchone()[0]:
			raise ServerError('Incorrect username / password')

		cur2 = db.query("SELECT * from SignUp_Details WHERE username = %s", [username])
		#r = [dict((cur.description[i][0], value) \
		#for i, value in enumerate(row)) for row in ]
		query_row = cur2.fetchall()[0]
		uid = query_row[0]
		logging.info(uid)

		password = form['password']
		cur = db.query("SELECT pwd FROM SignUp_Details WHERE username = %s;", [username])
		for row in cur.fetchall():
			print(row)
			if bcrypt.hashpw(password.encode('utf-8'), row[0]) == row[0]:
				session['uid'] = uid
				print("password match")
				return None

		raise ServerError('Incorrect username / password')
	except ServerError as e:
		error = str(e)
		return error

def signupUser(conn, form, ROUNDS):
	error = None
	try:
		print("Inside signupuser")
		username = form['fname']
		password = form['password']
		email    = form['email']
		fname = "fname"
		lname = form["lname"]
		phone_number = "12345678"
		addressLine1 = form["addressLine1"]
		addressLine2 = form["addressLine2"]
		city = form["city"]
		state = form["state"]
		xipcode = form["xipcode"]
		gender = form["gender"]
		intro = "I am a good guy"
		email_pref = form["email_pref"]
		if email_pref == "yes":
			email_pref = 1
		else:
			email_pref = 0
		logging.info(conn)
		cursor = conn.cursor()
		logging.info(xipcode)
		logging.info(email_pref)

		newpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))

		cursor.execute("""SELECT COUNT(*) FROM SignUp_Details WHERE username = %s""",[username])
		c = cursor.fetchone()
		logging.info(c)
		if c[0] == 0:
			try:
				conn.autocommit(False)
				# Referred this to prevent SQLI https://realpython.com/prevent-python-sql-injection/
				cursor.execute("""INSERT INTO SignUp_Details(`username`, `pwd`, `signuptime`) VALUES (%s,%s,NOW())""", (username, newpassword,))
				logging.info("Inserted in signup_details")
				cursor.execute("SELECT uid from SignUp_Details where username = %s",[username])
				logging.info("selected uid")
				d = cursor.fetchone()
				uid=d[0]
				logging.info(uid)
				cur = cursor.execute("""INSERT INTO user_info (`uid`,`fname`,`lname`,`email`, `phone_number`, `apt_num`, `street`,`city`,`state`,`zip_code`,`intro`,`email_preference`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", \
				[int(uid),fname,lname,email,phone_number,addressLine1,addressLine2,city,state,int(xipcode),intro, int(email_pref)])
				logging.info("inserted")
				conn.commit()
				conn.autocommit(True)
			except:
				print("in rollback")
				logging.info("Error in insertion")
				conn.rollback()
				error ="Error"
				return error
			return None
		else:
			logging.info("user exists")
			return "User exists"
	except ServerError as e:
		logging.info("Error in fetching user data")
		error = str(e)
		return error

def getUsers(db):
	error = None
	try:
		userlist = []
		cur = db.query("SELECT user, email FROM users")
		for row in cur.fetchall():
			userlist.append({'name': row[0], 'email': row[1]})
		return userlist
	except:
		error = "Failed"
		return error

def deleteUser(db, user):
	error = None
	try:
		cur = db.query("DELETE FROM users WHERE user = %s",[user])
		return None
	except:
		return "Failed"