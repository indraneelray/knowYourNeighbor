from flask import Flask , jsonify,session

class ServerError(Exception):pass



def search_people(conn,form):
    error = None
    #check userid not null and invalid
    people_list =[]
    final_list=[]
    #searchstring="S" #fetch from form
    #userid = 19 # fetch from session
    print("in search fetch method")
    searchstring = form["searchKey"]
    userid=session['uid']
    print("searchkey:", searchstring)

    neighborhoodid = find_neighborhood_id(conn,userid)
    print("neighborhood id:",neighborhoodid)
    try:
        if neighborhoodid is not None:
            #filter on name
            neighborhood_list = find_neighborhors_by_id(conn,neighborhoodid)
            print("neighborhood list:",neighborhood_list)
            for neighbor in neighborhood_list:
                addFriend=False
                addNeighbor=False
                    #check friend
                addFriend = is_friend(conn,userid,neighbor.get('userid'))
                    #check neighbor
                addNeighbor = is_neighbor(conn,userid,neighbor.get('userid'))
                people_list.append({'user_details':neighbor,'addFriend':addFriend,'addNeighbor':addNeighbor})

            # filter people with letter a
            for peoples in people_list:
                user=peoples.get('user_details').get('firstname')
                if user.startswith(searchstring.casefold()):
                    final_list.append(peoples)

            if len(final_list) == 0:
                error = "No result found!"
                return error
            else :
                print("final list is:",final_list)
                return final_list
        else:
            raise ServerError("No result found")
    except ServerError as e:
        error = "failure"
        return error




def search_thread(conn,form):
    error = None
    # check userid not null and invalid
    cursor = conn.cursor()
    final_list = []
    thread_list=[]
    print("in search fetch method")
    #searchstring = "a"  # fetch from form
    #userid = 19  # fetch from session

    searchstring = form["searchKey"]
    print("searchkey:",searchstring)
    userid = session['uid']

    neighborhoodid = find_neighborhood_id(conn, userid)
    print("neighborhood id:", neighborhoodid)
    try:
        if neighborhoodid is not None:
            neighborhood_list = find_neighborhors_by_id(conn, neighborhoodid)
            for neighbor in neighborhood_list:
                user = neighbor.get('userid')
                #find all threads posted
                cursor.execute("select * from Threads where author=%s",[user])
                for row in cursor.fetchall():
                    thread_list.append({'threadid': row[0], 'userid': row[1], 'thread_title': row[2], 'thread_description': row[3],'posted_at': row[4]})
            print("thread_list",thread_list)

            if len(thread_list) == 0:
                error = "No result found!"
                return error

            else :
                # check for filters in thread
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
        error = "failure"
        return error






def is_friend(conn,user1,user2):
    add = True
    cursor=conn.cursor()
    try:
        cursor.execute("select count(*) from friendship where (user1=%s and user2=%s ) or (user1=%s and user2=%s) and endtime is NULL",[user1,user2,user2,user1])
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
        cursor.execute("select count(*) from neighbors where (user1=%s and user2=%s ) or (user1=%s and user2=%s) and endtime is NULL",[user1,user2,user2,user1])
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
        cursor.execute("select neighborhood_id from user_details,block_details where user_details.userid=%s and user_details.blockid=block_details.blockid",[userid])
        neighborhood = cursor.fetchone()[0]
        #conn.commit()
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
        cursor.execute("select * from user_details,block_details where block_details.neighborhood_id=%s and block_details.blockid=user_details.blockid",[neighborhoodid])
        for row in cursor.fetchall():
            print("userid is:",row[0])
            neighbors_list.append({'userid': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3],'phone_number': row[4],'gender':row[5],'user_bio':row[6]})
        return neighbors_list
    except:
        error = "Error in fetching neighborhood id"
        return error
