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
    logging.info(cursor.fetchall())
    if cursor.fetchall():
        logging.info("User has friends")
        for row in cursor.fetchall():
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
    logging.info(cursor.fetchall)
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            if row[0]!= userid:
                friendslist.append(row[0])
            if row[1]!=userid :
                friendslist.append(row[1])
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
