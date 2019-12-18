from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
class ServerError(Exception):pass

def getFriendList(db):
    logging.info("getting friend list")
    error = None
    friendslist=[]
    uid = session['uid']
    logging.info(uid)
    cursor = db.query("""select uid,Friendid from friendship where uid = %s or friendId = %s and starttime is not Null and endtime is NULL""",[uid,uid])
    frnds = cursor.fetchall()
    if frnds:
        logging.info("User has friends")
        for row in frnds:
            if row[0]!= uid:
                friendslist.append(row[0])
            if row[1]!=uid :
                friendslist.append(row[1])
        logging.info(friendslist)
        return friendslist
    else :
        logging.info("no friends")
        return friendslist


def get_friends_details(conn):
    error = None
    userid = session['uid']
    friendslist=[]

    cursor=conn.cursor()
    cursor.execute("select uid,Friendid from friendship where uid = %s or friendId = %s and starttime is not Null and "
                   "endtime is NULL",[userid,userid])
    logging.info("SEarch friends query executed")
    logging.info(cursor.fetchall())
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            if row[0]!= userid:
                friendslist.append(row[0])
            if row[1]!=userid :
                friendslist.append(row[1])
        return friendslist
    else :
        raise ServerError("No friends for this user")


def get_friends_requests(conn):
    userid = session['uid']
    friendslist=[]
    status="pending"
    cursor=conn.cursor()
    cursor.execute("select fname, lname, uid_requestor,Friendid from friend_request inner join user_info on user_info.uid=friend_request.uid_requestor where friendId = %s \
         and friend_request.request_status=%s",[userid, status])
    logging.info("SEarch friends query executed")
    frnds = cursor.fetchall()
    logging.info(cursor.fetchall())
    if cursor.fetchall() is not None:
        logging.info("fetched friends")
        for row in frnds:
            logging.info(row)
            if row[2]!= userid:
                friendslist.append((row[0], row[1], row[2]))
            if row[3]!=userid :
                friendslist.append((row[0], row[1], row[2]))
        logging.info(friendslist)
        return friendslist
    else :
        raise ServerError("No friends for this user")


def send_friend_request(conn,id):
    error = None
    user1 = int(session['uid'])
    logging.info(user1)
    user2 = int(id)
    logging.info(user2)
    status = "pending"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO friend_request (`uid_requestor`, `friendid`, `request_status`) VALUES (%s,%s,%s)",[user1, user2,status])
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
            cursor.execute("UPDATE friend_request set request_status = %s where uid_requestor = %s and friendid = %s",[status.lower(),user1,user2])
            conn.commit()
            return None
        except:
            error = "Db error"
            return error
    elif status.casefold() == "approve":
        status="approved"
        try:
            cursor.execute("UPDATE friend_request set request_status = %s where uid_requestor = %s and friendid = %s",[status.lower(),user1,user2])
            cursor.execute("INSERT INTO friendship (`uid`, `friendid`, `starttime`) VALUES (%s,%s,NOW())",[user1, user2])
            conn.commit()
            return None
        except:
            print("in rollback")
            conn.rollback()
            error = "Error"
            return error
    else:
        raise ServerError("status not expected")

    
