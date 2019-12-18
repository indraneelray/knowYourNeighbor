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
        logging.info("Query executed to add locality approval")
        for row in cursor.fetchall():
            details.append({'userid': row[3], 'firstname': row[4], 'lastname': row[5]})
            logging.info("in block")
            logging.info(details)
        return details
    else:
        raise ServerError("No block requests for this user")


def block_approve(conn,id):
    error = None
    cursor = conn.cursor()
    user2 = int(session['uid'])
    user1 = id
    blockid=0
    try:
        approval=1
        print("updating block request")
        #cursor.execute("update Locality_Access_Request set Approval_Status=1 where uid=%s and requestor_id= %s",[user2,user1])
        cursor.execute("update locality_approval set Approval_Status='pending' where uid=%s and requestor_id= %s",[user2,user1])
        cursor.execute("select count(Approval_Status) from Locality_Access_Request where requestor_id= %s and approval=1",[user1])
        c=cursor.fetchone()
        print("count is:",c[0])
        if c[0] == 3:
            logging.info("in count")
            cursor.execute("select block_id from user_info where uid = %s",[user2])
            blockid = cursor.fetchone()[0]
            cursor.execute("INSERT INTO User_Locality (`bid`, `uid`, `starttime`) VALUES (%s,%s,NOW())",
                           [blockid, user1])
            cursor.execute("update user_info set block_id = %s where uid = %s", [blockid, user1])
        conn.commit()
        return None
    except ServerError as e:
        print("in rollback")
        conn.rollback()
        error = "Approval failed"
        return error