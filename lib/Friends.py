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