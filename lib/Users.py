from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import bcrypt
import logging
class ServerError(Exception):pass


def loginForm(db, form):
	error = None
	try:
		username = form['Username']
		cur = db.query("SELECT COUNT(1) FROM SignUp_Details WHERE username = %s", [username])
		print(cur)
		if not cur.fetchone()[0]:
			raise ServerError('Incorrect username / password')

		password = form['password']
		cur = db.query("SELECT pwd FROM SignUp_Details WHERE username = %s;", [username])
		for row in cur.fetchall():
			if bcrypt.hashpw(password.encode('utf-8'), row[0]) == row[0]:
				#session['username'] = form['username']
				print("password match")
				return None

		raise ServerError('Incorrect username / password')
	except ServerError as e:
		error = str(e)
		return error

# def registerUser(db, form, ROUNDS):
# 	error = None
# 	try:
# 		username = form['username']
# 		password = form['password']
# 		email    = form['email']

# 		if not username or not password or not email:
# 			raise ServerError('Fill in all fields')

# 		password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))

# 		cur = db.query("SELECT COUNT(*) FROM users WHERE user = %s",[username])
# 		c = cur.fetchone()
# 		if c[0] == 0:
# 			cur = db.query("INSERT INTO users (`user`, `email`, `pass`) VALUES (%s,%s,%s)", [username, email, password])
# 			return None
# 		else:
# 			return "User exists"
# 	except ServerError as e:
# 		error = str(e)
# 		return error

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
		print (username, password, email)
		print(lname) 
		print(addressLine1)
		print(addressLine2)  
		print(city)
		print(state) 
		print(xipcode)

		# if not username or not password or not email:
		# 	raise ServerError('Fill in all fields')

		newpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))
		#newpassword = sha256_crypt.encrypt(password.encode('utf-8'))

		#print("new pass", newpassword)

		cur = db.query("SELECT COUNT(*) FROM SignUp_Details WHERE username = %s",[username])
		c = cur.fetchone()
		if c[0] == 0:
			cur = db.query("INSERT INTO SignUp_Details (`username`, `pwd`, `signuptime`) VALUES (%s,%s,NOW())", [username, newpassword])
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