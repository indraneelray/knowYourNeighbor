from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
class ServerError(Exception):pass

def getBlockUsersResidents(db, bid):
    logging.info("getting Block residents")
    error = None
    try:
        logging.info("bid")
        logging.info(bid)
        cursor = db.query("""select uid from user_info where block_id = %s""", [int(bid)])        
        logging.info("block residents")
        block_residents = cursor.fetchall()
        logging.info(block_residents)
        uid = session['uid']
        residentList = []
        if block_residents:
            logging.info("User has residents in same block")
            for row in block_residents:
                logging.info(row)
                if row[0]!= int(uid):
                    residentList.append(row[0])
            logging.info(residentList)
            return residentList
        else :
            logging.info("no residents in same block")
            return residentList
    except:
        logging.error("error fetching residents of same block")
        error = "error"
        return error
