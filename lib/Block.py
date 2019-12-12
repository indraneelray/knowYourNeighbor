from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
class ServerError(Exception):pass

def getBlockUsersResidents(db, bid):
    '''
    Get all residents in a block
    '''
    #logging.info("getting Block residents")
    error = None
    try:
        #logging.info("bid")
        #logging.info(bid)
        cursor = db.query("""select userid from user_details where blockid = %s""", [int(bid)])
        #logging.info("block residents")
        block_residents = cursor.fetchall()
        #logging.info(block_residents)
        uid = session['uid']
        residentList = []
        if block_residents:
            #logging.info("User has residents in same block")
            for row in block_residents:
                #logging.info(row)
                if row[0]!= int(uid):
                    residentList.append(row[0])
            #logging.info(residentList)
            return residentList
        else :
            #logging.info("no residents in same block")
            return residentList
    except:
        #logging.error("error fetching residents of same block")
        error = "error"
        return error


def get_block_details(conn):
    error = None
    block_details=[]
    cursor = conn.cursor()
    try :
        cursor.execute("""select * from block_details limit 10""")
        for row in cursor.fetchall():
            block_details.append({'blockid': row[0], 'blockname': row[1], 'neighborhood_id': row[6], 'pincode': row[7]})
        return block_details
    except:
        error = "error"
        return error


def getBlockNameFromBid(db, bid):
    cur = db.query("select blockname from block_details where blockid = %s", [bid])
    bname = cur.fetchone()[0]
    return bname











