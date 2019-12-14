from flask import Flask , jsonify, session
import logging

class ServerError(Exception):pass

def search_people(conn,form):
    error = None
    #check userid not null and invalid
    people_list =[]
    final_list=[]
    #searchstring="S" #fetch from form
    searchstring = form["searchKey"]
    logging.info(searchstring)
    userid = session['uid']
    logging.info(userid)
    neighborhoodid = find_neighborhood_id(conn,userid)
    logging.info("neighborhood id:")
    logging.info(neighborhoodid)
    try:
        if neighborhoodid is not None:
            #filter on name
            neighborhood_list = find_neighborhors_by_id(conn,neighborhoodid)
            for neighbor in neighborhood_list:
                logging.info(neighbor)
                addFriend=False
                addNeighbor=False
                    #check friend
                addFriend = is_friend(conn,userid,neighbor.get('userid'))
                    #check neighbor
                addNeighbor = is_neighbor(conn,userid,neighbor.get('userid'))
                people_list.append({'user_details':neighbor,'addFriend':addFriend,'addNeighbor':addNeighbor})
            logging.info(people_list)

            # filter people with letter a
            for peoples in people_list:
                logging.info("fetching key first name")
                logging.info(peoples.get('user_details').get('firstname'))
                user=peoples.get('user_details').get('firstname')
                if user.startswith(searchstring.casefold()):
                    final_list.append(peoples)
            logging.info("final list")
            logging.info(final_list)

            if len(final_list) == 0:
                error = "No result found!"
                return error
            else :
                return final_list
        else:
            raise ServerError("No result found")
    except ServerError as e:
        error = "failure"
        return error

def search_thread(conn,form):
    error = None
    # check userid not null and invalid
    final_list = []
    thread_list=[]
    #searchstring = "a"  # fetch from form
    userid = session['uid']
    searchstring = form["searchKey"]
    logging.info(searchstring)
    cursor=conn.cursor()
    #userid = 19  # fetch from session'
    neighborhoodid = find_neighborhood_id(conn, userid)
    print("neighborhood id:", neighborhoodid)
    try:
        if neighborhoodid is not None:
            neighborhood_list = find_neighborhors_by_id(conn, neighborhoodid)
            logging.info(neighborhood_list)
            print("nrighborhoodlist:",neighborhood_list)
            for neighbor in neighborhood_list:
                print("neighbort oobject is:",neighbor)
                user = neighbor.get('userid')
                #find all threads posted
                cursor.execute("select * from messageThreads where created_by=%s",[user])
                for row in cursor.fetchall():
                    thread_list.append({'threadid': row[0], 'userid': row[1], 'thread_title': row[2], 'thread_description': row[3],'posted_at': row[4]})
            print("thread_list",thread_list)

            if len(thread_list) == 0:
                error = "No result found!"
                return error
            else :
                for thread in thread_list:
                    if searchstring.casefold() in thread.get('thread_title'):
                        final_list.append(thread)
                print("final list is:",final_list)

            if len(final_list) == 0:
                error = "No result found!"
                return error
            else :
                return final_list
        else:
            raise ServerError("user not associated with block")
    except ServerError as e:
        error = e
        return error

def is_friend(conn,user1,user2):
    add = True
    cursor=conn.cursor()
    try:
        cursor.execute("select count(*) from friendship where (uid=%s and friendid=%s ) or (uid=%s and friendid=%s) and endtime is NULL",[user1,user2,user2,user1])
        conn.commit()
        c = cursor.fetchone()
        print("c is:", c)
        print("c[0] is :", c[0])
        if c[0] >=1:
            add=False
        return add
    except ServerError as e:
        error = "failure"
        return error

def is_neighbor(conn,user1,user2):
    add = True
    cursor=conn.cursor()
    try:
        cursor.execute("select count(*) from neighbors where (uid=%s and neighborid=%s ) or (uid=%s and neighborid=%s) and endtime is NULL",[user1,user2,user2,user1])
        conn.commit()
        c = cursor.fetchone()
        print("c is:",c)
        print("c[0] is :",c[0])
        if c[0] >=1:
            add=False
        return add
    except ServerError as e:
        error = "failure"
        return error



def find_neighborhood_id(conn,userid):
    error=None
    neighborhood = 0
    cursor = conn.cursor()
    if not userid:
        raise ServerError("Request incomplete")
    try :
        #validate neighborhood id returned of no neighborhood
        cursor.execute("select nid from user_info,block_details where user_info.uid=%s and user_info.block_id=block_details.bid",[userid])
        neighborhood = cursor.fetchone()[0]
        #conn.commit()
        logging.info("neighborhood")
        logging.info(neighborhood)
        return neighborhood

    except:
        error = "Error in fetching neighborhood id"
        return error



def find_neighborhors_by_id(conn,neighborhoodid):
    error=None
    print("in neighbors")
    neighbors_list=[]
    cursor=conn.cursor()
    if not neighborhoodid:
        raise ServerError("Request incomplete")
    try :
        #validate neighborhood id returned of no neighborhood
        cursor.execute("select * from user_info,block_details where block_details.nid=%s and block_details.bid=user_info.block_id",[neighborhoodid])
        for row in cursor.fetchall():
            logging.info("userid is:")
            logging.info(row[0])
            neighbors_list.append({'userid': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3],'phone_number': row[4],'gender':row[5],'user_bio':row[6]})
        #conn.commit()
        return neighbors_list
    except:
        error = "Error in fetching neighborhood id"
        return error
