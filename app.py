from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for, make_response
import MySQLdb
import lib.Users as Users
import lib.message_boards as message_boards
import lib.Threads as Threads
import lib.Block as Block
import lib.Search as Search
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
	if 'uid' in session:
		return redirect(url_for('index'))
	if request.method == 'POST':
		logging.info("sign up")
		result = Users.signupUser(db.conn, request.form, config['pw_rounds'])
		if not result:
			notifications = {'message': 'Registration successful', 'type': 'success'}
			#XSS Protection
			response = make_response(render_template('join_block.html', message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			response = make_response(render_template('sign-up.html', message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
	if config['registration_enabled']:
		return render_template('sign-up.html', message=message)
	else:
		notifications = {'message': 'User registration is disabled by the admin', 'type': 'warning'}
		if 'uid' in session:
			return redirect(url_for('index'))
		else:
			return redirect(url_for('join_block'))


# TODO: XSS
@app.route('/join_block', methods=['GET','POST'])
def join_block():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	if request.method == 'POST':
		logging.info("/join_block")
		result = Users.requestBlock(db, request.form)
		if not result:
			message = {'message': 'Registration successful', 'type': 'success'}
			response = make_response(render_template("login.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			response = make_response(render_template("join_block.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
	if request.method == 'GET':
		logging.info('populate available blocks')
		#blocks = 
	return render_template('join_block.html')

@app.route('/profile', methods = ['GET'])
def profile():
	if 'uid' not in session:
		return redirect(url_for('login'))
	profile = []
	if request.method == 'GET':
		logging.info("Get profile")
		profile_data = Users.view_profile(db.conn, request.form)
		block_id = profile_data[10]
		block_name = Block.getBlockNameFromBid(db, block_id)
		logging.info(profile_data)
		if profile_data:
			profile.append({"Fname": profile_data[1], "LName": profile_data[2], "email": profile_data[3], "Username": profile_data[5], "apt": profile_data[5],\
				"street": profile_data[6], "city": profile_data[7], "state": profile_data[8], "zip": profile_data[9],"block_name" : block_name, "email_preference": profile_data[14]})
			logging.info(profile)				
	return render_template('show_profile.html', profileInfo = profile)

@app.route("/editProfile", methods=['POST', 'GET'])
def update_profile():
	notifications = None
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	if request.method == 'POST':
		logging.info("POST on update profile")
		result = Users.update_profile_details(db.conn, request.form)
		if not result:
			message = {'message': 'Profile update successful', 'type': 'success'}
			response = make_response(render_template("edit_profile.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			response = make_response(render_template("edit_profile.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
	return render_template('edit_profile.html')

# TODO: XSS
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
		friendThreads = message_boards.getUserFriendThreads(db, latest=True)
		logging.info(friendThreads)
		friendThreadInfo = []
		if friendThreads:
			for ft in friendThreads:
				logging.info(ft)
				threadDeets = message_boards.getThreadDetails(db, ft, 'f')
				if threadDeets:
					friendThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
			logging.info(friendThreadInfo)

		# Neighbors
		neighborThreads = message_boards.getUserNeighborThreads(db, latest=True)
		logging.info(neighborThreads)
		neighborThreadInfo = []
		if neighborThreads:
			for nt in neighborThreads:
				logging.info(nt)
				threadDeets = message_boards.getThreadDetails(db, nt, 'n')
				logging.info(threadDeets)
				if threadDeets:
					neighborThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
			logging.info(neighborThreadInfo)

		#block
		blockThreads = message_boards.getUserBlockThreads(db, latest=True)
		logging.info(blockThreads)
		blockThreadInfo = []
		if blockThreads:
			for bt in blockThreads:
				logging.info(bt)
				threadDeets = message_boards.getThreadDetails(db, bt, 'b')
				if threadDeets:
					blockThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

		#hood
		hoodThreads = message_boards.getUserHoodThreads(db, latest=True)
		logging.info("hood threads")
		logging.info(hoodThreads)
		hoodThreadInfo = []
		if hoodThreads:
			for ht in hoodThreads:
				threadDeets = message_boards.getThreadDetails(db, ht, 'h')
				logging.info("HOOD threadDeets")
				logging.info(threadDeets)
				if threadDeets:
					hoodThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
			
		return render_template('user-feed.html', friendFeedInfo = friendThreadInfo, neighborFeedInfo = neighborThreadInfo, blockFeedInfo = blockThreadInfo, hoodFeedInfo = hoodThreadInfo)
	
	if request.method == 'POST':
		logging.info("POST feed")
		if request.form['CreateThreadBtn'] == 'Save changes':
			logging.info("Creating new thread")
			result = message_boards.postNewThread(db, request.form)
			logging.info(result)
	return render_template('user-feed.html')


# TODO : XSS
@app.route('/block-feed', methods=['GET','POST'])
def blockfeed():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	logging.info("Fetching block feed")
	# get thread description
	blockThreadInfo = []
	blockThreads = message_boards.getUserBlockThreads(db)
	if blockThreads:
		blockThreads = list(set(blockThreads))
		logging.info(blockThreads)
		
		for bt in blockThreads:
			logging.info(bt)
			threadDeets = message_boards.getThreadDetails(db, bt, 'b')
			if threadDeets:
				blockThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

	return render_template('block_feed.html', blockFeedInfo = blockThreadInfo)


# TODO : Populate the thread details on top
@app.route('/show-thread', methods=['GET','POST'])
def showThread():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	logging.info('get thread')
	commentInfo = []
	if request.method == 'GET':
		tid = request.args.get('tid')
		logging.info('getting full thread')
		logging.info(tid)
		commentInfo = []
		comments = message_boards.showThreadComments(db, tid)
		logging.info(comments)
		# get thread title
		title = message_boards.getThreadTitle(db, tid)
		for c in comments:
			if comments:
				commentInfo.append({'tid':c[0], 'comment': c[1], 'tid': c[2], 'FName': c[3], 'LName': c[4]})
		logging.info("rendering template")
		#return jsonify({'threadCommentInfo' : commentInfo, 'threadTitle' : title})
		return render_template('show-threads.html', threadCommentInfo = commentInfo, threadTitle = title, tid = tid)
	if request.method == 'POST':
		logging.info(request)
		logging.info('post comment on thread ')
		tid = request.args.get('tid')
		posted = message_boards.postComment(db, request.form, tid)
		if posted is None:
			message = {'message': 'Posted comment successfully', 'type': 'success'}
			# get thread title
			title = message_boards.getThreadTitle(db, tid)
			comments = message_boards.showThreadComments(db, tid)
			for c in comments:
				if comments:
					commentInfo.append({'tid':c[0], 'comment': c[1], 'commentTime': c[2], 'FName': c[3], 'LName': c[4]})
			response = make_response(render_template('show-threads.html', threadCommentInfo = commentInfo, threadTitle = title, message = message, tid = tid))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Error in posting comment', 'type': 'error'}
			response = make_response(render_template("show-threads.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response


@app.route('/show-thread/post-comment', methods=['POST'])
def postThreadComment():
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	if request.method == 'POST':
		logging.info('post comment on thread ')
		posted = message_boards.postComment(db, request.form)
		if posted is None:
			message = {'message': 'Posted comment successfully', 'type': 'success'}
			response = make_response(render_template("show-threads.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response
		else:
			message = {'message': 'Error in posting comment', 'type': 'error'}
			response = make_response(render_template("show-threads.html", message =message))
			response.headers['X-XSS-Protection'] = '1; mode=block'
			return response


@app.route('/hood-feed', methods=['GET','POST'])
def hoodfeed():
	logging.info("Fetching hood feed")
	hoodThreads = message_boards.getUserHoodThreads(db)
	logging.info("hood threads")
	hoodThreadInfo = []
	if hoodThreads:
		hoodThreads = list(set(hoodThreads))
		logging.info(hoodThreads)
		for ht in hoodThreads:
			logging.info("getting hood thread deets")
			threadDeets = message_boards.getThreadDetails(db, ht, 'h')
			if threadDeets:
				hoodThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

	return render_template('hood_feed.html', hoodFeedInfo = hoodThreadInfo)

@app.route('/friend-feed', methods=['GET','POST'])
def friendfeed():
	logging.info("Fetching friend feed")
	friendThreads = message_boards.getUserFriendThreads(db)
	logging.info(friendThreads)
	friendThreadInfo = []
	if friendThreads:
		for ft in friendThreads:
			logging.info(ft)
			threadDeets = message_boards.getThreadDetails(db, ft, 'f')
			if threadDeets:
				friendThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
		logging.info(friendThreadInfo)
	return render_template('friend_feed.html', friendFeedInfo = friendThreadInfo)

@app.route('/neighbor-feed', methods=['GET','POST'])
def neighborfeed():
	logging.info("Fetching neighbor feed")
	neighborThreads = message_boards.getUserNeighborThreads(db)
	logging.info(neighborThreads)
	neighborThreadInfo = []
	if neighborThreads:
		for nt in neighborThreads:
			logging.info(nt)
			threadDeets = message_boards.getThreadDetails(db, nt, 'n')
			logging.info(threadDeets)
			if threadDeets:
				neighborThreadInfo.append({'tid': threadDeets[0],'CreatedBy': threadDeets[1], 'Title': threadDeets[2], 'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
		logging.info(neighborThreadInfo)
	return render_template('neighbor_feed.html', neighborFeedInfo = neighborThreadInfo)

@app.route("/search/thread", methods=['GET', 'POST'])
def search_threads():
	logging.info("display search threads")
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	if request.method == 'GET':
		return render_template('map_threads.html')
	if request.method == "POST":
		logging.info("POST search threads")
		result = Search.search_thread(db.conn, request.form)
		logging.info(result)
		if not result:
			message = {'message': 'Search failed', 'type': 'failure'}
			return render_template('show_friends.html', message = message)
		else:
			notifications = result
			return render_template('map_threads.html')
	return render_template('map_threads.html')


@app.route("/search/people", methods=['GET', 'POST'])
def search_people():
	notifications = None
	if 'uid' not in session:
		logging.info(session)
		return redirect(url_for('login'))
	if request.method == "POST":
		logging.info("POST search poeple")
		result = Search.search_people(db.conn, request.form)
		logging.info(result)
		if not result:
			message = {'message': 'Search failed', 'type': 'failure'}
			return render_template('search_people.html', message = message)
		else:
			return render_template('show_friends.html')
	else:
		return render_template('search_people.html')

#Run app
if __name__ == '__main__':
		app.run()