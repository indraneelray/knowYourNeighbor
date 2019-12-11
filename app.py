from flask import Flask , jsonify
import MySQLdb
import lib.Users as Users
import lib.Friends as Friends
import lib.Neighbors as Neighbors
import lib.Search as Search

app = Flask(__name__)
app.config.from_pyfile("config.conf", silent=False)


class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(
            host=app.config.get("DATABASE_HOST"),
            user=app.config.get("DATABASE_USER"),
            #passwd=app.config.get("DATABASE_HOST"),
            db=app.config.get("DATABASE_DB")
        )
        self.conn.autocommit(False)
        self.conn.set_character_set('utf8')

    def query(self, sql, args=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            #commit
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
        return cursor

if __name__ == "__main__":
        db = DB() # creating db connection
        db.connect()

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/login",methods=['GET','POST'])
def login():
    notifications=None
    result = Users.getUser(db,None)
    print("result is:",result)
    if not result:
       notifications = {'message': 'Logged in', 'type': 'success'}
       return notifications
    else:
        message = {'message': 'Failed to log in', 'type': 'error'}
        return message



@app.route("/users/signup",methods=['GET','POST'])
def signup():
    notifications = None
    #db.connect()
    result = Users.signup(db.conn, None, app.config.get("PWD_ROUNDS"))
    if not result:
        notifications = {'message': 'Registration successful', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: '+result, 'type': 'error'}
        return notifications

@app.route("/users/update_password",methods=['POST'])
def update_password():
    notifications = None
    result = Users.update_password(db.conn, None)
    if not result:
        notifications = {'message': 'Password updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: '+result, 'type': 'error'}
        return notifications

@app.route("/users/update_block_details",methods=['POST'])
def update_block_details():
    notifications = None
    result = Users.update_block_details(db.conn, None)
    if not result:
        notifications = {'message': 'Block details updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: '+result, 'type': 'error'}
        return notifications

@app.route("/users/update_profile",methods=['POST'])
def update_profile():
    notifications = None
    result = Users.update_profile_details(db.conn, None)
    if not result:
        notifications = {'message': 'Profile details updated', 'type': 'success'}
        return notifications
    else:
        notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
        return notifications

@app.route("/users/view_profile",methods=['GET'])
def view_profile():
    notifications = None
    result = Users.view_profile(db.conn, None)
    if not result:
        notifications = {'message': 'User doesnot exist', 'type': 'success'}
        return notifications
    else:
        notifications = result
        return notifications
        #return jsonify(result)

@app.route("/friends/send_friend_request",methods=['POST'])
def send_friend_request():
    notifications = None
    result = Friends.send_friend_request(db.conn,None)
    if not result :
        notifications = {'message': 'Friend Request sent', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/friends/accept_friend_request",methods=['POST'])
def accept_friend_request():
    notifications = None
    result = Friends.accept_friend_request(db.conn,None)
    if not result :
        notifications = {'message': 'Friend request accepted', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/neighbors/send_block_request",methods=['GET','POST'])
def send_block_request():
    notifications = None
    result = Neighbors.block_request(db.conn,None)
    if not result :
        notifications = {'message': 'Neighborhood request sent', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/friends/get_friends_details",methods=['GET','POST'])
def get_friends_details():
    notifications = None
    result = Friends.get_friends_details(db.conn,None)
    if not result :
        notifications = {'message': 'Error in fetching', 'type': 'success'}
        return notifications
    else :
        notifications=result
        return notifications

@app.route("/neighbors/approve_block_request",methods=['GET','POST'])
def accept_block_request():
    notifications = None
    result = Neighbors.block_approve(db.conn,None)
    if not result :
        notifications = {'message': 'Neighborhood request approved', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/neighbors/leave_block",methods=['GET','POST'])
def leave_block():
    notifications = None
    result = Neighbors.leave_block(db.conn,None)
    if not result :
        notifications = {'message': 'Block left.Please update your new block!', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/neighbors/add_neighbors",methods=['GET','POST'])
def add_neighbors():
    notifications = None
    result = Neighbors.add_neighbors(db.conn,None)
    if not result :
        notifications = {'message': 'Neighbors added successfully!', 'type': 'success'}
        return notifications
    else :
        message = {'message': 'Failed to send request.Please try again!', 'type': 'error'}
        return message

@app.route("/search/people",methods=['GET','POST'])
def search_people():
    notifications = None
    result = Search.search_people(db.conn,None)
    if not result :
        message = {'message': 'Search failed', 'type': 'success'}
        return message
    else :
        notifications = result
        return notifications

if __name__ == "__main__":
    app.run()
