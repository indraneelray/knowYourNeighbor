from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for, make_response
import MySQLdb
import lib.Users as Users
import lib.message_boards as message_boards
from flask_wtf.csrf import CSRFProtect
import logging

app = Flask(__name__)
# CSRF Protect
csrf = CSRFProtect(app)

class ServerError(Exception):pass

class DB:
	conn = None
	
	def connect(self):
		config = {}
		#execfile("config.conf",config)
		exec(open("config.conf").read(), config)

		self.conn = MySQLdb.connect(
			host=config['db_host'],
			user=config['db_user'],
			passwd=config['db_pass'],
			db=config['db_data']
		)
		self.conn.autocommit(True)
		self.conn.set_character_set('utf8') 

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		return cursor

if __name__ == '__main__':
	config = {}
	#execfile("config.conf",config)
	exec(open("config.conf").read(), config)
	app.secret_key = config['app_key']
	db = DB()
	db.connect()
	notifications = None
	logging.basicConfig(filename=config['logfile'], level=logging.INFO)
	with open(config['logfile'], 'w'):
		pass
	

#Routes
@app.route('/')
def index():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	# if 'username' not in session:
	# 	message = {'message': 'Please log in', 'type': 'warning'}
	# 	return redirect(url_for('login'))
	if 'uid' in session:
		logging.info(session)
		return redirect(url_for('show_feed'))
	return render_template('index.html',session=session,message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
	logging.info('Started login')
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if 'uid' in session:
		logging.info(session)
		return redirect(url_for('show_feed'))
	print ("Inside login")
	if request.method == 'POST':
		result = Users.loginForm(db, request.form)
		print(result)
		if not result:
			notifications = {'message': 'Logged in', 'type': 'success'}
			#XSS Protection
			response = make_response(render_template('user-feed.html',message=message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Failed to log in', 'type': 'error'}
			response = make_response(render_template('login.html',message=message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
	response = make_response(render_template('login.html',message=message))
	response.headers['X-XSS-Protection'] = '1; mode=block'
	return response


@app.route('/logout')
def logout():
	logging.info('logout pressed')
	global notifications
	if 'uid' not in session:
		return redirect(url_for('index'))
	result = Users.logout(db)
	if not result:
		session.pop('uid', None)
		notifications = {'message': 'Logged out', 'type': 'success'}
		#XSS Protection
		response = make_response(render_template('index.html'))
		response.headers['X-XSS-Protection'] = '1; mode=block'
		return response
	else:
		notifications = {'message': 'Log out Failed', 'type': 'error'}

@app.route('/sign-up', methods=['GET','POST'])
def signup():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if request.method == 'POST':
		logging.info("sign up")
		result = Users.signupUser(db.conn, request.form, config['pw_rounds'])
		if not result:
			notifications = {'message': 'Registration successful', 'type': 'success'}
			#XSS Protection
			response = make_response(render_template('index.html'))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			return render_template('sign-up.html', message=message)
	if 'uid' in session and session['uid'] == 1:
		return render_template('sign-up.html', message=message)
	if config['registration_enabled']:
		return render_template('sign-up.html', message=message)
	else:
		notifications = {'message': 'User registration is disabled by the admin', 'type': 'warning'}
		if 'uid' in session:
			return redirect(url_for('index'))
		else:
			return redirect(url_for('join_block'))


@app.route('/join_block', methods=['GET','POST'])
def join_block():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('index'))
	if request.method == 'POST':
		logging.info("/join_block")
		result = Users.requestBlock(db, request.form)
		if not result:
			message = {'message': 'Registration successful', 'type': 'success'}
			return render_template("join_block.html", message=message)
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			return render_template("join_block.html", message=message)
	if request.method == 'GET':
		logging.info('/populate available blocks')
		#blocks = 
	return render_template('join_block.html')

@app.route('/profile')
def profile():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	return render_template('show_profile.html')

@app.route('/editProfile')
def editProfile():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	return render_template('edit_profile.html')

# @app.route('/threads')
# def show_message():
# 	if 'uid' not in session:
# 		logging.info(session)
# 		return redirect(url_for('login'))
# 	db = DB()
# 	allInfo = message_boards.getUserThreads(db)
# 	logging.info(allInfo)
# 	return render_template('user-feed.html', allInfo = allInfo)

@app.route('/feed', methods=['GET','POST'])
def show_feed():
	logging.info("Show feed")
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	db = DB()
	if request.method == 'GET':
		logging.info(request)
		# friend 
		friendThreads = message_boards.getUserFriendThreads(db)
		logging.info(friendThreads)
		friendThreadInfo = []
		for ft in friendThreads:
			logging.info(ft)
			threadDeets = message_boards.getThreadDetails(db, ft, 'f')
			friendThreadInfo.append({'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
		logging.info(friendThreadInfo)

		# Neighbors
		neighborThreads = message_boards.getUserNeighborThreads(db)
		logging.info(neighborThreads)
		neighborThreadInfo = []
		for nt in neighborThreads:
			logging.info(ft)
			threadDeets = message_boards.getThreadDetails(db, nt, 'n')
			logging.info(threadDeets)
			neighborThreadInfo.append({'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
		logging.info(neighborThreadInfo)

		#block
		blockThreads = message_boards.getUserBlockThreads(db)
		logging.info(blockThreads)
		blockThreadInfo = []
		for bt in blockThreads:
			logging.info(bt)
			threadDeets = message_boards.getThreadDetails(db, bt, 'b')
			logging.info("BLOCK Deets")
			logging.info(threadDeets)
			blockThreadInfo.append({'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

		return render_template('user-feed.html', friendFeedInfo = friendThreadInfo, neighborFeedInfo = neighborThreadInfo, blockFeedInfo = blockThreadInfo)
	if request.method == 'POST':
		logging.info("POST feed")
		if request.form['submit_btn'] == 'Submit':
			logging.info("POSTED from create thread")
			result = message_boards.postNewThread(db, request.form)
			logging.info(result)
	return render_template('user-feed.html')

#Run app
if __name__ == '__main__':
		app.run()