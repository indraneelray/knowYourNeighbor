from flask import Flask , jsonify,session


class ServerError(Exception):pass



def block_request(conn,form):
    print("in block request")
    error = None
    #blockid = 1
    #userid= 5
    userid = session['uid']
    blockid = form["baname"]
    print("blockid is:",blockid)
    print("userid is:", userid)
    status = "pending"
    activeneighbors=[]
    #if blockid or userid is None:
    #    raise ServerError("Request incomplete")
    cursor = conn.cursor()
    try :
        ## fetching active neighbors in the block
        cursor.execute("select * from userneighborhood where blockid = %s and left_at is NULL",[int(blockid)])
        #c = cursor.fetchall()
        print("neighborhood")
        for row in cursor.fetchall():
            print("row:",row)
            activeneighbors.append({'blockid': row[0], 'userid': row[1], 'joined_at': row[2], 'left_at': row[3]})
        print("len of :",len(activeneighbors))
        if len(activeneighbors)<=2:
            print("in less neighbors")
            #default insert if no neighbors in that block
            status = "approved"
            requestapproved=1
            print("active neighbors")
            try:
                cursor.execute("INSERT INTO neighborhood_request (`userid`, `blockid`, `request_status`, `request_approved`) VALUES (%s,%s,%s,%s)",[userid, blockid,status,int(requestapproved)])
                cursor.execute("update user_details set blockid = %s where userid = %s",[blockid,userid])
                cursor.execute("INSERT INTO userneighborhood (`blockid`, `userid`, `joined_at`) VALUES (%s,%s,NOW())",[blockid, userid])
                conn.commit()
                return None
            except :
                print("in neighbor rollback")
                conn.rollback()
                error = "Error"
                return error
        else:
            print("in more neighbors")
            status = "pending"
            approval =0
            try:
                cursor.execute(
                    "INSERT INTO neighborhood_request (`userid`, `blockid`, `request_status`, `request_approved`) VALUES (%s,%s,%s,%s)",
                    [userid, blockid, status, approval])
                for  n in activeneighbors:
                    cursor.execute(
                        "INSERT INTO Neighborhood_access (`requested_touser`, `requested_byuser`, `approval`) VALUES (%s,%s,%s)",
                        [n.get("userid"), userid, approval])
                conn.commit()
                return None
            except:
                conn.rollback()
                error = "Error"
                return error
    except ServerError as e:
        error = "Update failed"
        return error


def block_approve(conn,id):
    error = None
    cursor = conn.cursor()
    user2 = int(session['uid'])
    user1 = id
    blockid=0
    try:
        approval=1
        print("updating block request")
        cursor.execute("update neighborhood_access set approval=1 where requested_touser=%s and requested_byuser= %s",[user2,user1])
        cursor.execute("select count(approval) from neighborhood_access where requested_byuser= %s and approval=1",[user1])
        c=cursor.fetchone()
        print("count is:",c[0])
        if c[0] == 3:
            print("in count")
            cursor.execute("select blockid from user_details where userid = %s",[user2])
            blockid = cursor.fetchone()[0]
            cursor.execute("INSERT INTO userneighborhood (`blockid`, `userid`, `joined_at`) VALUES (%s,%s,NOW())",
                           [blockid, user1])
            cursor.execute("update user_details set blockid = %s where userid = %s", [blockid, user1])
        conn.commit()
        return None
    except ServerError as e:
        print("in rollback")
        conn.rollback()
        error = "Approval failed"
        return error


def leave_block(conn,form):
    error = None
    cursor = conn.cursor()
    userid=session['uid']
    blockid=None
    #add userid null check
    #add user exists or not
    try :
        cursor.execute("update user_details set blockid = %s where userid = %s", [blockid, userid])
        cursor.execute("update userneighborhood set left_at= NOW() where userid= %s",[userid] )
        conn.commit()
        return None
    except ServerError as e:
        conn.rollback()
        error = "Update failed"
        return error


def add_neighbors(conn,id):
    error = None
    cursor=conn.cursor()
    requested_byuser = int(session['uid'])
    requested_touser = int(id)
    #check for user
    # check if entry exists
    try:
        cursor.execute("INSERT INTO neighbors (`user1`, `user2`, `starttime`) VALUES (%s,%s,NOW())",
                           [requested_byuser, requested_touser])
        conn.commit()
    except ServerError as e:
        conn.rollback()
        error = "Update failed"
        return error


def get_requests_for_block(conn):
    userid = int(session['uid'])
    error = None
    details = []
    cursor = conn.cursor()
    cursor.execute(
        "select * from Neighborhood_access inner join user_details on user_details.userid=Neighborhood_access.requested_byuser and Neighborhood_access.requested_touser=%s and Neighborhood_access.approval!=1",
        [userid])
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            details.append({'userid': row[3], 'firstname': row[4], 'lastname': row[5]})
            print("details:", details)
        return details
    else:
        raise ServerError("No friends for this user")


def getNeighborList(db):
    print("getting Neighbor list")
    error = None
    neighborlist=[]
    uid = int(session['uid'])
    cursor = db.query("""select user1, user2 from Neighbors where user1 = %s or user2 = %s and starttime is not Null and endtime is NULL""",[uid,uid])
    for row in cursor.fetchall():
        print("User has Neighbors")
        if row[0]!= uid:
            neighborlist.append(row[0])
        if row[1]!=uid :
            neighborlist.append(row[1])
    return neighborlist





