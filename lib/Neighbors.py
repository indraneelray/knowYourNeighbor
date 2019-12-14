from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
class ServerError(Exception):pass

def getNeighborList(db):
    logging.info("getting Neighbor list")
    error = None
    neighborlist=[]
    uid = session['uid']
    logging.info(uid)
    cursor = db.query("""select uid, Neighborid from Neighbors where uid = %s or neighborId = %s and starttime is not Null and endtime is NULL""",[uid,uid])
    logging.info(cursor.fetchall())
    if cursor.fetchall():
        logging.info("User has Neighbors")
        for row in cursor.fetchall():
            if row[0]!= uid:
                neighborlist.append(row[0])
            if row[1]!=uid :
                neighborlist.append(row[1])
        logging.info(neighborlist)
        return neighborlist
    else :
        logging.info("no Neighbors")
        return neighborlist


def add_neighbors(conn,id):
    error = None
    cursor=conn.cursor()
    requested_byuser = int(session['uid'])
    requested_touser = int(id)
    #check for user
    # check if entry exists
    try:
        cursor.execute("INSERT INTO neighbors (`uid`, `neighborid`, `starttime`) VALUES (%s,%s,NOW())",
                           [requested_byuser, requested_touser])
        conn.commit()
    except ServerError as e:
        conn.rollback()
        error = "Update failed"
        return error


def get_requests_for_block(conn):
    logging.info("fetching block approval requests")
    userid = int(session['uid'])
    error = None
    details = []
    cursor = conn.cursor()
    cursor.execute(
        "select * from locality_approval inner join user_info on user_info.uid=locality_approval.requestor_id and locality_approval.uid=%s and locality_approval.approval_status='pending'",
        [userid])
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            details.append({'userid': row[3], 'firstname': row[4], 'lastname': row[5]})
            logging.info("in block")
            logging.info(details)
        return details
    else:
        raise ServerError("No friends for this user")