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
