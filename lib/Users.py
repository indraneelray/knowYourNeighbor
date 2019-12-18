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
		username = form['username']
		password = form['password']
		email    = form['email']
		fname = form["fname"]
		lname = form["lname"]
		phone_number = "12345678"
		addressLine1 = form["addressLine1"]
		addressLine2 = form["addressLine2"]
		city = form["city"]
		state = form["state"]
		xipcode = form["xipcode"]
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
				session['uid'] = uid
			except:
				logging.error("Rollback. Error in insertion")
				conn.rollback()
				error ="Error"
				return error
			return None
		else:
			logging.error("user exists")
			return "User exists"
	except ServerError as e:
		logging.info("Error in fetching user data")
		error = str(e)
		return error

def logout(db):
	error = None
	try:
		uid = session['uid']
		db.query("UPDATE user_info set logout_time = NOW() where uid = %s", [uid])
		return None
	except:
		logging.error("Not updated logout time in DB")
		error = "Failed"
		return error

def requestBlock(conn, form):
	error = None
	userid = session['uid']
	blockid = form["baname"]
	logging.info(blockid)
	logging.info(userid)
	status = "pending"
	activeneighbors=[]
	cursor = conn.cursor()
	try :
		## fetching active neighbors in the block
		cursor.execute("""select * from user_locality where bid = %s and endtime is NULL""",[int(blockid)])
		#c = cursor.fetchall()
		logging.info("neighborhood")
		for row in cursor.fetchall():
			print("row:",row)
			activeneighbors.append({'blockid': row[0], 'userid': row[1], 'joined_at': row[2], 'left_at': row[3]})
		logging.info(activeneighbors)
		if len(activeneighbors)<=2:
			print("in less neighbors")
			#default insert if no neighbors in that block
			status = "approved"
			requestapproved=1
			print("active neighbors")
			try:
				cursor.execute("""INSERT INTO locality_access_request (`uid`, `bid`, `request_status`, `isActive`) VALUES (%s,%s,%s,%s)""",[userid, blockid,status,int(requestapproved)])
				cursor.execute("""update user_info set block_id = %s where uid = %s""",[blockid,userid])
				cursor.execute("INSERT INTO user_locality (`bid`, `uid`, `starttime`) VALUES (%s,%s,NOW())",[blockid, userid])
				conn.commit()
				return None
			except :
				print("in neighbor rollback")
				conn.rollback()
				error = "Error"
				return error
		else:
			print("in more neighbors")
			status = "pending"
			approval =0
			try:
				cursor.execute(
					"INSERT INTO locality_access_request (`uid`, `bid`, `request_status`, `isActive`) VALUES (%s,%s,%s,%s)",
					[userid, blockid, status, approval])
				for  n in activeneighbors:
					cursor.execute(
						"INSERT INTO locality_approval (`uid`, `requestor_id`, `bid`, `approval_status`) VALUES (%s,%s,%s,%s)",
						[n.get("userid"), userid, blockid, status])
				conn.commit()
				return None
			except:
				conn.rollback()
				error = "Error"
				return error
	except ServerError as e:
		error = "Update failed"
		return error


def update_profile_details(conn,form):
		error =None
		try:
			firstname = form["fname"]
			lastname = form["lname"]
			apartment_no=form["addressLine1"]
			street=form["addressLine2"]
			city=form["city"]
			state=form["state"]
			zipcode=form["xipcode"]
			userid = session['uid']
			cursor = conn.cursor()
			try:
				conn.autocommit(False)
				if firstname:
					cursor.execute("UPDATE user_info set fname = %s where uid = %s",[firstname,userid])
				if lastname :
					cursor.execute("UPDATE user_info set lname = %s where uid = %s", [lastname, userid])
				if apartment_no :
					cursor.execute("UPDATE user_info set apt_num = %s where uid = %s", [apartment_no, userid])
				if city :
					cursor.execute("UPDATE user_info set city = %s where uid = %s", [city, userid])
				if street :
					cursor.execute("UPDATE user_info set street = %s where uid = %s", [street, userid])
				if state :
					cursor.execute("UPDATE user_info set state = %s where uid = %s", [state, userid])
				if zipcode :
					cursor.execute("UPDATE user_info set zip_code = %s where uid = %s", [zipcode, userid])
				conn.commit()
				conn.autocommit(True)
				return None
			except:
				print("in rollback")
				conn.rollback()
				error = "Error in database update"
				return error
		except ServerError as e:
			error = str(e)
			return error

def view_profile(conn,form):
	error =None
	cursor = conn.cursor()
	profile_details = []
	uid = session['uid']
	try:
		cursor.execute("select * from user_info where uid = %s",[uid])
		c = cursor.fetchone()
		if c is not None:
			logging.info("user info")
			logging.info(c)
			return c
		else :
			raise ServerError("User does not exist")
	except ServerError as e:
		error = str(e)
		return error

def get_logout_time(db):
	uid = session['uid']
	curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
	logout_time = curTime.fetchone()[0]
	return logout_time