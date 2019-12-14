from flask import Flask, jsonify, render_template, redirect, url_for, make_response, request,escape,session
import MySQLdb
import lib.Users as Users
import lib.Friends as Friends
import lib.Neighbors as Neighbors
import lib.Search as Search
import lib.Block as Block
import lib.message_boards as message_boards
#from flask.ext.session import Session
from lib import Hood

app = Flask(__name__)
#Session(app)
app.config.from_pyfile("config.conf", silent=False)


class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(
            host=app.config.get("DATABASE_HOST"),
            user=app.config.get("DATABASE_USER"),
            # passwd=app.config.get("DATABASE_HOST"),
            db=app.config.get("DATABASE_DB")
        )
        self.conn.autocommit(False)
        self.conn.set_character_set('utf8')

    def query(self, sql, args=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            # commit
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
        return cursor

    def createSession(self, uid):
        session['uid'] = uid


if __name__ == "__main__":
    app.secret_key = app.config.get("SECRET_KEY")
    print("app secret key:",app.secret_key)
    db = DB()  # creating db connection
    db.connect()
    notifications = None


#@app.route("/")
#def hello():
#    return "Hello World!"

@app.route("/")
def index():
    message = None
    if 'uid' in session:
        #logging.info(session)
        print("on home page")
        return redirect(url_for('show_feed')) #user feed html

    return render_template('index.html', session=session, message=message)


@app.route("/users/login", methods=['GET', 'POST'])
def login():
    message = None
    global notifications
    if notifications:
        message = notifications
        notifications = None
    if 'uid' in session:
        return redirect(url_for('show_feed'))
    print("Inside login")
    if request.method == 'POST':
        result = Users.getUser(db, request.form)
        print(result)
        if not result:
            notifications = {'message': 'Logged in', 'type': 'success'}
            # XSS Protection
            #response = make_response(render_template('user-feed.html', message=message))
            #response.headers['X-XSS-Protection'] = '1; mode=block'
           # return redirect('show_feed.html', message=message)
            return redirect(url_for('show_feed'))
        else:
            message = {'message': 'Failed to log in', 'type': 'error'}
            #response = make_response(render_template('login.html', message=message))
            #response.headers['X-XSS-Protection'] = '1; mode=block'
            return render_template('login.html', message=message)
    #response = make_response(render_template('login.html', message=message))
    #response.headers['X-XSS-Protection'] = '1; mode=block'
    else:
        return render_template('login.html', message=message)



@app.route('/logout')
def logout():
    global notifications
    print("in logout")
    if 'uid' not in session:
        return redirect(url_for('login'))
    result = Users.logout(db.conn)
    print("result:",result)
    if not result:
        session.pop('uid', None)
        notifications = {'message': 'Logged out', 'type': 'success'}
        return redirect(url_for('login'))
    else :
        message = {'message': 'Logout failed', 'type': 'error'}
        return message


@app.route("/users/signup", methods=['GET','POST'])
def signup():
    notifications = None
    message = None
    if request.method == 'POST':
        print(db.conn)

        result = Users.signup(db, db.conn, request.form, app.config.get("PWD_ROUNDS"))
        if not result:
            print("in signup success result")
            notifications = {'message': 'Registration successful', 'type': 'success'}
            return render_template('join_block.html', notifications=notifications)
        else:
            print("in signup error")
            message = {'message': 'Something went wrong: ' + result, 'type': 'error'}
            return render_template('sign-up.html', message=message)
    else:
        print("in signup get call")
        return render_template('sign-up.html', message=message)





@app.route("/users/update_password", methods=['POST'])
def update_password():
    notifications = None
    result = Users.update_password(db.conn, request.form)
    if not result:
        notifications = {'message': 'Password updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
        return notifications


@app.route("/users/update_block_details", methods=['POST'])
def update_block_details():
    notifications = None
    result = Users.update_block_details(db.conn, None)
    if not result:
        notifications = {'message': 'Block details updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
        return notifications


@app.route("/users/update_profile", methods=['POST'])
def update_profile():
    notifications = None
    result = Users.update_profile_details(db.conn, None)
    if not result:
        notifications = {'message': 'Profile details updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
        return notifications


@app.route("/users/view_profile", methods=['GET'])
def view_profile():
    notifications = None
    if 'uid' not in session:
        return redirect(url_for('login'))
    result = Users.view_profile(db.conn, None)
    if not result:
        message = {'message': 'User doesnot exist', 'type': 'success'}
        #return notifications
        redirect(url_for('login'))
    else:
        message = result
        return render_template('show_profile.html', message=message)


@app.route("/friends/send_friend_request", methods=['POST'])
def send_friend_request():
    notifications = None
    result = Friends.send_friend_request(db.conn, None)
    if not result:
        notifications = {'message': 'Friend Request sent', 'type': 'success'}
        return notifications
    else:
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message


@app.route("/friends/accept_friend_request", methods=['POST'])
def accept_friend_request():
    notifications = None
    result = Friends.accept_friend_request(db.conn, None)
    if not result:
        notifications = {'message': 'Friend request accepted', 'type': 'success'}
        return notifications
    else:
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message


@app.route("/neighbors/send_block_request", methods=['GET', 'POST'])
def send_block_request():
    notifications = None
    message=None
    print("in block request UI call")
    if 'uid' not in session:
        print("session in accept request",session)
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("in block request call")
        result = Neighbors.block_request(db.conn, request.form)
        if not result:
            print("in join block request success call")
            notifications = {'message': 'Neighborhood request sent', 'type': 'success'}
            return render_template("user-feed.html", notifications=notifications)
        else:
            print("in join block request failure call")
            message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
            return render_template("join_block.html", message=message)
    else :
        print("in join block get call")
        return render_template("join_block.html", message=message)


@app.route("/friends/get_friends_details", methods=['GET', 'POST'])
def get_friends_details():
    notifications = None
    result = Friends.get_friends_details(db.conn, None)
    if not result:
        notifications = {'message': 'Error in fetching', 'type': 'success'}
        return notifications
    else:
        notifications = result
        return notifications


@app.route("/neighbors/approve_block_request", methods=['GET', 'POST'])
def accept_block_request():
    notifications = None
    result = Neighbors.block_approve(db.conn, None)
    if not result:
        notifications = {'message': 'Neighborhood request approved', 'type': 'success'}
        return notifications
    else:
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message


@app.route("/neighbors/leave_block", methods=['GET', 'POST'])
def leave_block():
    notifications = None
    result = Neighbors.leave_block(db.conn, None)
    if not result:
        notifications = {'message': 'Block left.Please update your new block!', 'type': 'success'}
        return notifications
    else:
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message


@app.route("/neighbors/add_neighbors", methods=['GET', 'POST'])
def add_neighbors():
    notifications = None
    result = Neighbors.add_neighbors(db.conn, None)
    if not result:
        notifications = {'message': 'Neighbors added successfully!', 'type': 'success'}
        return notifications
    else:
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message


@app.route("/search/people", methods=['GET', 'POST'])
def search_people():
    notifications = None
    if request.method == 'POST':
        print("in search people")
        result = Search.search_people(db.conn, request.form)
        if not result:
            message = {'message': 'Search failed', 'type': 'failure'}
            return render_template("user-feed.html", message=message)
        else:
            #notifications = result
            print("result is:",result)
            return render_template("show-people.html", people=result)
    else :
        return render_template("show-people.html", notifications=notifications)


@app.route("/search/thread", methods=['GET', 'POST'])
def search_threads():
    notifications = None
    result=[{}]
    if request.method == 'POST':
        print("in search thread")
        result = Search.search_thread(db.conn, request.form)
        if not result:
            message = {'message': 'Search failed', 'type': 'failure'}
            return render_template("user-feed.html", message=message)
        else:
            #notifications = result
            print("result is:",result)
            return  render_template("show-threads.html", threads=result)
    else :
        return render_template("show-threads.html", notifications=notifications)


@app.route('/feed', methods=['GET', 'POST'])
def show_feed():
    print("in show feed")
    if 'uid' not in session:
        print(session)
        return redirect(url_for('login'))
    #db = DB()
    if request.method == 'GET':
        # friend
        friendThreads = message_boards.getUserFriendThreads(db, latest=True)
        #logging.info(friendThreads)
        friendThreadInfo = []
        if friendThreads is not None:
            for ft in friendThreads:
                #logging.info(ft)
                threadDeets = message_boards.getThreadDetails(db, ft, '0')
                if threadDeets:
                    friendThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                         'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
        print(friendThreadInfo)

        # Neighbors
        neighborThreads = message_boards.getUserNeighborThreads(db, latest=True)
        neighborThreadInfo = []
        if neighborThreads is not None:
            #logging.info(neighborThreads)
            for nt in neighborThreads:
                #logging.info(nt)
                 threadDeets = message_boards.getThreadDetails(db, nt, '1')
                 #logging.info(threadDeets)
                 if threadDeets:
                     neighborThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                           'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
        print(neighborThreadInfo)

        # block
        blockThreads = message_boards.getUserBlockThreads(db, latest=True)
        blockThreadInfo = []
        if blockThreads is not None:
            #logging.info(blockThreads)
            #blockThreadInfo = []
            for bt in blockThreads:
                #logging.info(bt)
                threadDeets = message_boards.getThreadDetails(db, bt, '2')
                if threadDeets:
                    blockThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                        'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
        print(blockThreadInfo)

        # hood
        hoodThreads = message_boards.getUserHoodThreads(db, latest=True)
        hoodThreadInfo = []
        if hoodThreads is not None:
            #logging.info("hood threads")
            #logging.info(hoodThreads)
            #hoodThreadInfo = []
            for ht in hoodThreads:
                threadDeets = message_boards.getThreadDetails(db, ht, '3')
                # logging.info("HOOD threadDeets")
                #logging.info(threadDeets)
                if threadDeets:
                    hoodThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                       'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
        print(hoodThreadInfo)
        return render_template('user-feed.html', friendFeedInfo=friendThreadInfo, neighborFeedInfo=neighborThreadInfo,
                               blockFeedInfo=blockThreadInfo, hoodFeedInfo=hoodThreadInfo)

    if request.method == 'POST':
            #logging.info("POST feed")
            if request.form['submit_btn'] == 'Submit':
                #logging.info("POSTED from create thread")
                 result = message_boards.postNewThread(db, request.form)
                #logging.info(result)
    return render_template('user-feed.html')


# TODO : XSS
@app.route('/block-feed', methods=['GET', 'POST'])
def blockfeed():
    #logging.info("Fetching block feed")
    # get thread description
    blockThreads = message_boards.getUserBlockThreads(db)
    blockThreads = list(set(blockThreads))
    #logging.info(blockThreads)
    blockThreadInfo = []
    for bt in blockThreads:
        #logging.info(bt)
        threadDeets = message_boards.getThreadDetails(db, bt, 'b')
        if threadDeets:
            blockThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                    'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

    return render_template('block_feed.html', blockFeedInfo=blockThreadInfo)


# TODO : Populate the thread details on top
@app.route('/show-thread', methods=['GET', 'POST'])
def showThread():
    #logging.info('get thread')
    if request.method == 'GET':
       # logging.info(request)
        comments = message_boards.showThreadComments(db)
        #logging.info(comments)
        commentInfo = []
        # get thread title
        title = message_boards.getThreadTitle(db)
        for c in comments:
            if comments:
                commentInfo.append({'comment': c[0], 'commentTime': c[1], 'FName': c[2], 'LName': c[3]})
        return render_template('show-threads.html', threadCommentInfo=commentInfo, threadTitle=title)


@app.route('/hood-feed', methods=['GET', 'POST'])
def hoodfeed():
    #logging.info("Fetching hood feed")
    hoodThreads = message_boards.getUserHoodThreads(db)
    #logging.info("hood threads")
    hoodThreads = list(set(hoodThreads))
    #logging.info(hoodThreads)
    hoodThreadInfo = []
    for ht in hoodThreads:
        #logging.info("getting hood thread deets")
        threadDeets = message_boards.getThreadDetails(db, ht, 'h')
        if threadDeets:
            hoodThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                   'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})

    return render_template('hood_feed.html', hoodFeedInfo=hoodThreadInfo)


@app.route('/friend-feed', methods=['GET', 'POST'])
def friendfeed():
   # logging.info("Fetching friend feed")
    friendThreads = message_boards.getUserFriendThreads(db)
   # logging.info(friendThreads)
    friendThreadInfo = []
    for ft in friendThreads:
       # logging.info(ft)
        threadDeets = message_boards.getThreadDetails(db, ft, 'f')
        if threadDeets:
            friendThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                     'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
    #logging.info(friendThreadInfo)
    return render_template('friend_feed.html', friendFeedInfo=friendThreadInfo)


@app.route('/neighbor-feed', methods=['GET', 'POST'])
def neighborfeed():
    #logging.info("Fetching neighbor feed")
    neighborThreads = message_boards.getUserNeighborThreads(db)
    #logging.info(neighborThreads)
    neighborThreadInfo = []
    for nt in neighborThreads:
        #logging.info(nt)
        threadDeets = message_boards.getThreadDetails(db, nt, 'n')
        #logging.info(threadDeets)
        if threadDeets:
            neighborThreadInfo.append({'tid': threadDeets[0], 'CreatedBy': threadDeets[1], 'Title': threadDeets[2],
                                       'Description_Msg': threadDeets[3], 'CreatedAt': threadDeets[4]})
    #logging.info(neighborThreadInfo)
    return render_template('neighbor_feed.html', neighborFeedInfo=neighborThreadInfo)

@app.route('/threads')
def show_message():
    if 'uid' not in session:
        return redirect(url_for('login'))
    allInfo = message_boards.getUserThreads(db)
    return render_template('show-threads.html', allInfo=allInfo)

@app.route('/profile')
def profile():
    if 'uid' not in session:
        return redirect(url_for('login'))
    profile = []
    if request.method == 'GET':
        profile_data = Users.view_profile(db.conn, request.form)
        block_id = profile_data[14]
        block_name = Block.getBlockNameFromBid(db, block_id)
        if profile_data:
            profile.append({"Fname": profile_data[1], "LName": profile_data[2], "email": profile_data[3],
                             "apt": profile_data[5],
                            "street": profile_data[6], "city": profile_data[7], "state": profile_data[8],
                            "zip": profile_data[9], "block_name": block_name, "email_preference": profile_data[14]})
    return render_template('show_profile.html', profileInfo=profile)

@app.route('/block_details',methods=['GET', 'POST'])
def get_block_details():
    if request.method == "POST":
        result =Block.get_block_details(db.conn, request.form)
        return render_template('join_block.html', blockinfo=result)
    else:
        message={'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return render_template('join_block.html', message=message)


@app.route('/neighborhood_details')
def get_neighborhood_details():
    # if request.method == "POST":
        result =Hood.getHooddetails(db.conn)
        print(result);
        return render_template('join_block.html', hoodinfo=result)
    # else:
    #     message={'message': 'Failed to send request.Please try again!', 'type': 'error'}
    #     return render_template('join_block.html', message=message)

@app.route('/searchMessages')
def getSearchMessagesPage() :
    message={}
    print("in serach message")
    return render_template('search-threads.html', message=message)

@app.route('/searchPeople')
def getSearchPeoplePage() :
    message={}
    return render_template('search-people.html', message=message)

@app.route('/blockaprrovalrequests')
def getBlockApprovalRequests() :
    message={}
    return render_template('approval-requests.html', message=message)

@app.route('/friendrequests')
def getFriendRequests() :
    message={}
    return render_template('friend-requests.html', message=message)

@app.route('/block_details_for_hood',methods=['GET', 'POST'])
def block_details_for_hood():
    if request.method == "GET":
        hoodid = request.args.get('selectedHoodid');
        result =Block.get_block_details_for_hood(db.conn, hoodid)
        return jsonify(blockList=result);
    else:
        message={'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return render_template('join_block.html', message=message)

@app.route('/changePasswordPage')
def getChangePasswordHTML() :
    message={}
    return render_template('change_password.html', message=message)

















if __name__ == "__main__":
    app.run()
