from flask import Flask , jsonify

class ServerError(Exception):pass



def search_people(conn,form):
    error = None
    search_list=[]
    cursor = conn.cursor()
    userid=19
    #check userid not null and invalid
    people_list =[{}]

    neighborhoodid = find_neighborhood_id(cursor,userid)
    print("neighborhood id:",neighborhoodid)
    try:
        if neighborhoodid is not None:
            #filter on name
            neighborhood_list = find_neighborhors_by_id(cursor,neighborhoodid)
            for neighbor in neighborhood_list:
                addFriend=False
                addNeighbor=False
                for d in neighborhood_list:
                    print("first neighbor:",d.get('userid'))
                    #check friend
                    addFriend = is_friend(cursor,userid,d.get('userid'))
                    print("add friend is:",addFriend)
                    addNeighbor = is_neighbor(cursor,userid,d.get('userid'))
                    people_list.append({'userid':})

                #check already friends if yes, add friend false
        else:
            print("not")
    except ServerError as e:
        error = "failure"
        return error











def is_friend(cursor,user1,user2):
    add = True
    try:
        cursor.execute("select count(*) from friendship where (user1=%s and user2=%s ) or (user1=2 and user2=1) and endtime is NULL",[user1,user2,user2,user1])
        c = cursor.fetchall()
        if c[0] >=1:
            add=False
        return add
    except ServerError as e:
        error = "failure"
        return error

def is_neighbor(cursor,user1,user2):
    add = True
    try:
        cursor.execute("select count(*) from neighbors where (user1=%s and user2=%s ) or (user1=%s and user2=%s) and endtime is NULL",[user1,user2,user2,user1])
        c = cursor.fetchall()
        if c[0] >=1:
            add=False
        return add
    except ServerError as e:
        error = "failure"
        return error



def find_neighborhood_id(cursor,userid):
    error=None
    neighborhood = 0
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



def find_neighborhors_by_id(cursor,neighborhoodid):
    error=None
    print("in neighbors")
    neighbors_list=[]
    if not neighborhoodid:
        raise ServerError("Request incomplete")
    try :
        #validate neighborhood id returned of no neighborhood
        cursor.execute("select * from user_details,block_details where block_details.neighborhood_id=%s and block_details.blockid=user_details.blockid",[neighborhoodid])
        for row in cursor.fetchall():
            print("userid is:",row[0])
            neighbors_list.append({'userid': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3],'phone_number': row[4],'gender':row[5],'user_bio':row[6]})
        #conn.commit()
        return neighbors_list
    except:
        #conn.rollback()
        error = "Error in fetching neighborhood id"
        return error


