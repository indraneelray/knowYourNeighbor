from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
import lib.Block as Block
class ServerError(Exception):pass

def getHoodResidents(db, hid):
    logging.info("getting hood residents")
    error = None
    try:
        blocks = getAllBlocksInHood(db,hid)
        logging.info("blocks in hood")
        logging.info(blocks)
        hoodResidents = []
        for block in blocks:
                blockResidents = Block.getBlockUsersResidents(db, block)
                for resident in blockResidents:
                    hoodResidents.append(resident)
        logging.info(hoodResidents)
        return hoodResidents
    except:
        logging.error("error fetching residents of same block")
        error = "error"
        return error

def getHoodIdFromBlockId(db, bid):
    try:
        logging.info("getting hood ID")
        cursor = db.query("""select distinct(nid) from user_info join block_details where bid = %s""", [int(bid)]) 
        hid = cursor.fetchall()[0]
        logging.info(hid)
        return hid
    except:
        logging.error("error getting hoodID")
        return None

def getAllBlocksInHood(db, hid):
    try:
        logging.info("Getting all blocks in hood")
        logging.info(hid)
        cursor = db.query("""select bid from block_details where nid = %s""", [int(hid)])
        logging.info("got all blocks in neighborhood")
        bids = cursor.fetchall()
        logging.info(bids)
        blocks = []
        if bids:
            logging.info("found bid for this neighborhood")
            for row in bids:
                logging.info(row[0])
                blocks.append(row[0])
            return blocks
        else:
            logging.info("error")
            return None
    except:
        logging.error("error getting BID's from hid")
        return None

def gethoodlist(db):
    hoodlist = []
    try:
        cursor = db.query("""select * from neighborood_details""")
        for row in cursor.fetchall():
            hoodlist.append({
                'hoodid' : row[0], 'hoodname' : row[1]
            })
        return hoodlist
    except:
        error = "Error"
        return error
    
