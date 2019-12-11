from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
import lib.Friends as Friends
class ServerError(Exception):pass

def getUserFriendThreads(db):
	error = None
	try:
		logging.info("getting friends")
		#threadlist = []
		uid = session['uid']
		logging.info(uid)
		#cur = db.query("""select * from MessageThreads where created_by = %s order by created_time limit 10;""", [uid])
		curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		logging.info(logout_time)
		friends = Friends.getFriendList(db)
		logging.info(friends)
		#for friendId in friends:
		tids = getLatestCommentTIDs(db, friends, logout_time) 
		logging.info(tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		logging.info("threads")
		logging.info(threads)

		# for row in cur.fetchall():
		# 	threadlist.append({'CreatedBy': row[1], 'Title': row[2], 'Description_Msg': row[3], 'CreatedAt': row[4]})
		return threads
	except:
		logging.info("error fetching user threads")
		error = "Failed"
		return error

def postNewThread(db, form):
	error = None
	try:
		logging.info("posting new thread")
		uid = session['uid']
		threadTitle = form['title']
		#threadTitle = "thread title"
		description = form['description']
		#description = "description"
		access_level = form['privacy']
		#access_level = "f"
		logging.info(uid)
		logging.info(threadTitle)
		logging.info(description)
		logging.info(access_level)
		db.query("""INSERT INTO MessageThreads(Created_By, Title, Description_Msg, Created_Time, Access_Level)VALUES\
			(%s,%s,%s,NOW(),%s)""", [uid, threadTitle, description, access_level])
	except:
		logging.info("error posting in user thread")
		error = "Failed"
		return error

def getLatestCommentTIDs(db, uid, logout_time):
	#TODO this stuff is hard coded right now for testing purposes
	logging.info("getting latest comments")
	try:
		uid = 2
		cur = db.query("""select distinct(tid) from ThreadComments where comment_by = 3 and commentTime > 2017-08-02""")
		threads = cur.fetchall()[0]
		logging.info("got latest comments")
		return threads
	except:
		logging.info("failed to get latest comments")

#access level
def getThreadDetails(db, tid, access_level = 'h'):
	error = None
	try:
		logging.info("getting message threads")
		cur = db.query("""select * from messagethreads where tid = %s and access_level = %s""", [tid, access_level])
		threadContent = cur.fetchall()[0]
		logging.info(threadContent)
		return threadContent
	except:
		logging.info("error posting in user thread")
		error = "Failed"
		return error
	