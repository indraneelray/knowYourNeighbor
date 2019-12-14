from flask import Flask , jsonify,session


class ServerError(Exception):pass


def send_friend_request(conn,id):
    error = None
    user1 = int(session['uid'])
    user2 = int(id)
    status = "pending"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO friendrequest (`requested_by`, `requestedto`, `status`) VALUES (%s,%s,%s)",[user1, user2,status])
        conn.commit()
        return None
    except ServerError as e:
        error = "Update failed"
        return error

def accept_friend_request(conn,id,action):
    error = None
    user1 =id
    user2 =int(session['uid'])
    status = action
    #if not user1 or user2 or status:
       # raise ServerError("Mandatory fields not present in request")
    cursor = conn.cursor()
    if status.casefold() == "decline":
        status="declined"
        try :
            cursor.execute("UPDATE friendrequest set status = %s where requested_by = %s and requestedto = %s",[status.lower(),user1,user2])
            conn.commit()
            return None
        except:
            error = "Db error"
            return error
    elif status.casefold() == "approve":
        status="approved"
        try:
            cursor.execute("UPDATE friendrequest set status = %s where requested_by = %s and requestedto = %s",[status.lower(),user1,user2])
            cursor.execute("INSERT INTO friendship (`user1`, `user2`, `starttime`) VALUES (%s,%s,NOW())",[user1, user2])
            conn.commit()
            return None
        except:
            print("in rollback")
            conn.rollback()
            error = "Error"
            return error
    else:
        raise ServerError("status not expected")



def get_friends_details(conn):
    error = None
    userid = session['uid']
    friendslist=[]
    if not userid:
        raise ServerError("Mandatory fields not present in request")

    cursor=conn.cursor()
    cursor.execute("select user1,user2 from friendship where user1 = %s or user2 = %s and starttime is not Null and "
                   "endtime is NULL",[userid,userid])
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            if row[0]!= userid:
                friendslist.append(row[0])
            if row[1]!=userid :
                friendslist.append(row[1])
        return friendslist
    else :
        raise ServerError("No friends for this user")


def get_friend_requests(conn):
    userid=int(session['uid'])
    error=None
    details=[]
    status="pending"
    cursor = conn.cursor()
    cursor.execute("select * from friendrequest inner join user_details on user_details.userid=friendrequest.requested_by and friendrequest.requestedto=%s and friendrequest.status=%s", [userid,status])
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            details.append({'userid':row[0],'firstname':row[4],'lastname':row[5]})
            print("details:",details)
        return details
    else:
        raise ServerError("No friends for this user")


def getFriendList(db):
    #logging.info("getting friend list")
    error = None
    friendslist=[]
    uid = int(session['uid'])
    print("uid in getfriendlist:",uid)
    cursor = db.query("""select user1,user2 from friendship where user1 = %s or user2 = %s and starttime is not Null and endtime is NULL""",[uid,uid])
    for row in cursor.fetchall():
        print("row is:",row)
        if row[0]!=uid:
            friendslist.append(row[0])
        if row[1]!=uid :
            friendslist.append(row[1])
        print("friends returned is:",friendslist)
    return friendslist
