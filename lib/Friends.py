from flask import Flask , jsonify


class ServerError(Exception):pass


def send_friend_request(conn,form):
    error = None
    user1 = ""
    user2 = ""   #request from ui
    status = "pending"
    if not user1 or user2 :
        raise ServerError("user ids should be present")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO friendrequest (`requested_by`, `requested_to`, 'status') VALUES (%s,%s,%s)",[user1, user2,status])
        conn.commit()
        return None
    except ServerError as e:
        error = "Update failed"
        return error

def accept_friend_request(conn,form):
    error = None
    user1 =""
    user2 =""
    status = ""
    if not user1 or user2 or status:
        raise ServerError("Mandatory fields not present in request")
    cursor = conn.cursor()
    if status.casefold() == "declined":
        try :
            cursor.execute("UPDATE friendrequest set status = %s where user1 = %s and user2 = %s",[status.lower(),user1,user2])
            conn.commit()
            return None
        except:
            error = "Db error"
            return error
    elif status.casefold() == "approved":
        try:
            cursor.execute("UPDATE friendrequest set status = %s where user1 = %s and user2 = %s",[status.lower(),user1,user2])
            cursor.execute("INSERT INTO friendship (`user1`, `user2`, 'starttime') VALUES (%s,%s,NOW())",[user1, user2,status])
            conn.commit()
            return None
        except:
            print("in rollback")
            conn.rollback()
            error = "Error"
            return error
    else:
        raise ServerError("status not expected")



def get_friends_details(conn,form):
    error = None
    userid = 1
    friendslist=[]
    if not userid:
        raise ServerError("Mandatory fields not present in request")

    cursor=conn.cursor()
    cursor.execute("select user1,user2 from friendship where user1 = %s or user2 = %s and starttime is not Null and "
                   "endtime is NULL",[userid,userid])
    if cursor.fetchall is not None:
        for row in cursor.fetchall():
            if row[0]!= userid:
                friendslist.append(row[0])
            if row[1]!=userid :
                friendslist.append(row[1])
        return jsonify(friendslist)
    else :
        raise ServerError("No friends for this user")

