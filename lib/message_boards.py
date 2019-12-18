from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
import lib.Friends as Friends
import lib.Neighbors as Neighbors
import lib.Block as Block
import lib.Hood as Hood
class ServerError(Exception):pass

def getUserFriendThreads(db, latest = False):
	try:
		logging.info("getting friends")
		#threadlist = []
		uid = session['uid']
		#cur = db.query("""select * from MessageThreads where created_by = %s order by created_time limit 10;""", [uid])
		curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		logging.info(logout_time)
		friends = Friends.getFriendList(db)
		logging.info(friends)
		tids = []
		for friendId in friends:
			tids = getCommentTIDs(db, friendId, logout_time, latest)
			tids.append(getLatestThreads(db, logout_time, friendId, 'f'))
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
		return None

def getUserNeighborThreads(db, latest = False):
	try:
		logging.info("getting neighbor threads")
		#threadlist = []
		uid = session['uid']
		#cur = db.query("""select * from MessageThreads where created_by = %s order by created_time limit 10;""", [uid])
		curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		logging.info(logout_time)
		neighbors = Neighbors.getNeighborList(db)
		logging.info(neighbors)
		tids = []
		for neighborId in neighbors:
			tids = getCommentTIDs(db, neighborId, logout_time, latest)
			tids.append(getLatestThreads(db, logout_time, neighborId, 'n'))
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
		return None


def getUserBlockThreads(db, latest = False):
	try:
		logging.info("getting block threads")
		uid = session['uid']
		curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		logging.info(logout_time)
		cur2 = db.query("""select block_id from user_info where uid = %s""", [uid])
		bid = cur2.fetchone()[0]
		logging.info(bid)
		blockUsers = Block.getBlockUsersResidents(db, bid)
		logging.info(blockUsers)
		tids = []
		for user in blockUsers:
			blockTids = getCommentTIDs(db, user, logout_time, latest)
			if blockTids:
				for b in blockTids:
					tids.append(b)
			tids.append(getLatestThreads(db, logout_time, user, 'b'))
		logging.info("tids")
		logging.info(tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		logging.info("threads")
		logging.info(threads)
		return threads
	except:
		logging.info("error fetching user threads")
		return None

def getUserHoodThreads(db, latest = False):
	try:
		logging.info("getting hood threads")
		# get logout time
		uid = session['uid']
		curTime = db.query("""select logout_time from user_info where uid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		logging.info(logout_time)
		# get users blockid
		cur2 = db.query("""select block_id from user_info where uid = %s""", [uid])
		logging.info("bid")
		bid = cur2.fetchone()[0]
		logging.info(bid)
		# get hood id from block id
		curh = db.query("""select nid from block_details where bid = %s""", [bid])
		hid = curh.fetchone()[0]
		logging.info("hid")
		logging.info(hid)
		hoodUsers = Hood.getHoodResidents(db, hid)
		logging.info('hood users')
		logging.info(hoodUsers)
		tids = []
		for user in hoodUsers:
			hoodTid = getCommentTIDs(db, user, logout_time, latest)
			if hoodTid:
				for h in hoodTid:
					tids.append(h)
			tids.append(getLatestThreads(db, logout_time, user, 'h'))
		logging.info("tids")
		logging.info(tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		logging.info("threads")
		logging.info(threads)
		return threads
	except:
		logging.info("error fetching user threads")
		return None

def postNewThread(db, form):
	error = None
	try:
		logging.info("posting new thread")
		uid = session['uid']
		logging.info(uid)
		threadTitle = form['title']
		logging.info(threadTitle)
		#threadTitle = "thread title"
		description = form['description']
		logging.info(description)
		#description = "description"
		access_level = form['privacy']
		logging.info(access_level)
		#access_level = "f"
		logging.info(uid)
		
		
		
		db.query("""INSERT INTO MessageThreads(Created_By, Title, Description_Msg, Created_Time, Access_Level)VALUES\
			(%s,%s,%s,NOW(),%s)""", [uid, threadTitle, description, access_level])
	except:
		logging.info("error posting in user thread")
		error = "Failed"
		return error

def getCommentTIDs(db, uid, logout_time, latest = False):
	logging.info("getting comments")
	try:
		logging.info(logout_time)

		logout = str(logout_time)
		logging.info(logout)
		logging.info(type(logout_time))
		if latest is True:
			logging.info("Finding latest active threads")
			cur = db.query("""select distinct(tid) from ThreadComments where comment_by = %s and commentTime > %s""", [int(uid), logout])
		else:
			logging.info("Finding all threads")
			cur = db.query("""select distinct(tid) from ThreadComments where comment_by = %s""", [int(uid)])
		logging.info("success query")
		tids = cur.fetchall()
		logging.info(tids)
		threads = []
		for c in tids:
			logging.info(c[0])
			threads.append(c[0])
		logging.info(threads)
		logging.info("got latest comments")
		return threads
	except:
		logging.info("failed to get latest comment threads")
		return None

def getThreadDetails(db, tid, access_level):
	error = None
	try:
		logging.info("getting message threads")
		logging.info(tid)
		cur = db.query("""select * from messagethreads where tid = %s and access_level = %s""", [tid, access_level])
		metaThreadContent = cur.fetchone()
		logging.info(metaThreadContent)
		return metaThreadContent
	except:
		logging.error("error getting thread details")
		error = "Failed"
		return error

def showThreadComments(db, tid):
	error = None
	try:
		logging.info("getting thread comments")
		cur = db.query("""select tid, comment_Msg, commentTime, FName, LName from threadComments, user_info where threadComments.Comment_by = user_info.uid and tid = %s""", [tid])
		comments = cur.fetchall()
		commentList = []
		for c in comments:
			commentList.append(c)
		logging.info(commentList)
		return commentList
	except:
		logging.error("error getting thread comments")
		return error

def getThreadTitle(db, tid):
	error = None
	try:
		logging.info("getting thread title")
		cur = db.query("""select title from messagethreads where tid = %s""", [tid])
		title = cur.fetchone()[0]
		return title
	except:
		logging.error("error fetching thread title")
		return error

	
def postComment(db, form, tid):
	logging.info("posting comments")
	uid = session['uid']
	logging.info(uid)
	commentTxt = form["commentText"]
	logging.info(commentTxt)
	#description = form["description"]
	try:
		cur = db.query("""insert into threadcomments (tid, comment_msg, comment_by, commentTime)values (%s, %s, %s, NOW())""", [tid, commentTxt, uid])
		return None
	except:
		return "error"

def getLatestThreads(db, logout_time, uid, access_level):
	error = None
	try:
		logging.info("getting message threads")
		logging.info(tid)
		cur = db.query("""select * from messagethreads where created_by = %s and access_level = %s and created_time > %s""", [uid, access_level, logout_time])
		metaThreadContent = cur.fetchall()
		logging.info(metaThreadContent)
		return metaThreadContent
	except:
		logging.error("error getting thread details")
		error = "Failed"
		return error
