from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import lib.Block as Block
class ServerError(Exception):pass

def getHoodResidents(db, hid):
    error = None
    try:
        blocks = getAllBlocksInHood(db,hid)
        hoodResidents = []
        for block in blocks:
                blockResidents = Block.getBlockUsersResidents(db, block)
                for resident in blockResidents:
                    hoodResidents.append(resident)
        return hoodResidents
    except:
        error = "error"
        return error

def getHoodIdFromBlockId(db, bid):
    try:
        cursor = db.query("""select distinct(neighborhood_id) from user_details join block_details where blockid = %s""", [int(bid)])
        hid = cursor.fetchall()[0]
        return hid
    except:
        #logging.error("error getting hoodID")
        return None

def getAllBlocksInHood(db, hid):
    try:
        cursor = db.query("""select blockid from block_details where neighborhood_id = %s""", [int(hid)])
        #logging.info("got all blocks in neighborhood")
        bids = cursor.fetchall()
        blocks = []
        if bids:
            #logging.info("found bid for this neighborhood")
            for row in bids:
                #logging.info(row[0])
                blocks.append(row[0])
            return blocks
        else:
            #logging.info("error")
            return None
    except:
        #logging.error("error getting BID's from hid")
        return None

def getHooddetails(conn):
        error = None
        hood_details = []
        cursor = conn.cursor()
        try:
            cursor.execute("""select * from Neighborhood_details limit 10""")
            for row in cursor.fetchall():
                hood_details.append(
                    {'neighborhoodid': row[0], 'neighborhoodname': row[1]})
            return hood_details
        except:
            error = "error"
            return error