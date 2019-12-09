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

def signupUser(db, form, ROUNDS):
	error = None
	try:
		logging.info('This is an info message')
		print("Inside signupuser")
		username = form['fname']
		password = form['password']
		email    = form['email']
		lname = form["lname"]
		addressLine1 = form["addressLine1"]
		addressLine2 = form["addressLine2"]
		city = form["city"]
		state = form["state"]
		xipcode = form["xipcode"]

		# if not username or not password or not email:
		# 	raise ServerError('Fill in all fields')

		newpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))

		cur = db.query("SELECT COUNT(*) FROM SignUp_Details WHERE username = %s",[username])
		c = cur.fetchone()
		if c[0] == 0:
			cur = db.query("INSERT INTO SignUp_Details (`username`, `pwd`, `signuptime`) VALUES (%s,%s,NOW())", [username, newpassword])
			#cur = db.query("INSERT INTO User_Info ('Fname', 'Lname', 'email', 'phone_number', 'apt_num', 'street', 'city', 'state', 'zip_code', )VALUES ")
			return None
		else:
			return "User exists"
	except ServerError as e:
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