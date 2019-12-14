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
		curTime = db.query("""select logout_at from user_details where userid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		print("logout_time:",logout_time)
		friends = Friends.getFriendList(db)
		print("friends is:",friends)
		tids = []
		for friendId in friends:
			tids = getCommentTIDs(db, friendId, logout_time, latest)
		print("thread:",tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		#logging.info("threads")
		#logging.info(threads)

		# for row in cur.fetchall():
		# 	threadlist.append({'CreatedBy': row[1], 'Title': row[2], 'Description_Msg': row[3], 'CreatedAt': row[4]})
		print("threads returned for friemds:",threads)
		return threads
	except:
		#logging.info("error fetching user threads")
		return None

def getUserNeighborThreads(db, latest = False):
	try:
		print("getting neighbor threads")
		#threadlist = []
		uid = session['uid']
		print("uid is:",uid)
		#cur = db.query("""select * from MessageThreads where created_by = %s order by created_time limit 10;""", [uid])
		curTime = db.query("""select logout_at from user_details where userid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		#logging.info(logout_time)
		neighbors = Neighbors.getNeighborList(db)
		print("neighbors are:",neighbors)
		tids = []
		for neighborId in neighbors:
			tids = getCommentTIDs(db, neighborId, logout_time, latest)
			print("thread ids:",tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		#logging.info("threads")
		#logging.info(threads)

		# for row in cur.fetchall():
		# 	threadlist.append({'CreatedBy': row[1], 'Title': row[2], 'Description_Msg': row[3], 'CreatedAt': row[4]})
		print("thread returned for neighbors:",threads)
		return threads
	except:
		#logging.info("error fetching user threads")
		return None


def getUserBlockThreads(db, latest = False):
	try:
		print("getting block threads")
		uid = session['uid']
		curTime = db.query("""select logout_at from user_details where userid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		#logging.info(logout_time)
		cur2 = db.query("""select blockid from user_details where userid = %s""", [uid])
		bid = cur2.fetchone()[0]
		#logging.info(bid)
		blockUsers = Block.getBlockUsersResidents(db, bid)
		#logging.info(blockUsers)
		tids = []
		for user in blockUsers:
			blockTids = getCommentTIDs(db, user, logout_time, latest)
			if blockTids:
				for b in blockTids:
					tids.append(b)
		#logging.info("tids")
		#logging.info(tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		#logging.info("threads")
		#logging.info(threads)
		return threads
	except:
		#logging.info("error fetching user threads")
		return None

def getUserHoodThreads(db, latest = False):
	try:
		print("getting hood threads")
		# get logout time
		uid = session['uid']
		curTime = db.query("""select logout_at from user_details where userid = %s""", [uid])
		logout_time = curTime.fetchone()[0]
		#logging.info(logout_time)
		# get users blockid
		cur2 = db.query("""select blockid from user_details where userid = %s""", [uid])
		#logging.info("bid")
		bid = cur2.fetchone()[0]
		#logging.info(bid)
		# get hood id from block id
		curh = db.query("""select neighborhood_id from block_details where blockid = %s""", [bid])
		hid = curh.fetchone()[0]
		#logging.info("hid")
		#logging.info(hid)
		hoodUsers = Hood.getHoodResidents(db, hid)
		#logging.info('hood users')
		#logging.info(hoodUsers)
		tids = []
		for user in hoodUsers:
			hoodTid = getCommentTIDs(db, user, logout_time, latest)
			if hoodTid:
				for h in hoodTid:
					tids.append(h)
		#logging.info("tids")
		#logging.info(tids)
		threads = []
		for tid in tids:
			threads.append(tid)
		#logging.info("threads")
		#logging.info(threads)
		return threads
	except:
		#logging.info("error fetching user threads")
		return None

def postNewThread(db, form):
	error = None
	try:
		print("posting new thread")
		uid = session['uid']
		threadTitle = form['title']
		#threadTitle = "thread title"
		description = form['description']
		#description = "description"
		access_level = form['privacy']
		#access_level = "f"
		db.query("""INSERT INTO Threads('author','thread_title','thread_description','postedat','view_level')VALUES
			(%s,%s,%s,NOW(),%s)""", [uid, threadTitle, description, access_level])
	except:
		logging.info("error posting in user thread")
		error = "Failed"
		return error

def getCommentTIDs(db, uid, logout_time, latest = False):
	print("getting comments")
	try:

		logout = str(logout_time)
		if latest is True:
			#logging.info("Finding latest active threads")
			cur = db.query("""select distinct(threadid) from messages where replied_by = %s and posted_at > %s""", [int(uid), logout])
		else:
			#logging.info("Finding all threads")
			cur = db.query("""select distinct(threadid) from messages where replied_by = %s""", [int(uid)])
		#logging.info("success query")
		tids = cur.fetchall()
		#logging.info(tids)
		threads = []
		for c in tids:
			#logging.info(c[0])
			threads.append(c[0])
		#logging.info(threads)
		#logging.info("got latest comments")
		return threads
	except:
		#logging.info("failed to get latest comment threads")
		return None

def getThreadDetails(db, tid, access_level):
	error = None
	try:
		print("getting message threads")
		#logging.info(tid)
		cur = db.query("""select * from Threads where threadid = %s and view_level = %s""", [tid, access_level])
		metaThreadContent = cur.fetchone()
		#logging.info(metaThreadContent)
		print("metathreadcount is:",metaThreadContent)
		return metaThreadContent
	except:
		#logging.error("error getting thread details")
		error = "Failed"
		return error


def showThreadComments(db, tid):
	error = None
	try:
		print("threadid is:",tid)
		print("getting thread comments")
		cur = db.query(
			"""select messages.threadid, messages.comment_message, messages.posted_at, user_details.firstname, user_details.lastname from messages, user_details where messages.replied_by = user_details.userid and threadid = %s""",
			[tid])
		comments = cur.fetchall()
		commentList = []
		for c in comments:
			commentList.append(c)
		print("commentlist is:",commentList)
		return commentList
	except:
		return error



def getThreadTitle(db, tid):
	error = None
	try:
		logging.info("getting thread title")
		cur = db.query("""select thread_title from threads where threadid = %s""", [tid])
		title = cur.fetchone()[0]
		return title
	except:
		#logging.error("error fetching thread title")
		return error


def postComment(db, form, tid):
	logging.info("posting comments")
	uid = session['uid']
	logging.info(uid)
	commentTxt = form["commentText"]
	logging.info(commentTxt)
	# description = form["description"]
	try:
		cur = db.query(
			"""insert into messages (threadid, comment_message, author, posted_at)values (%s, %s, %s, NOW())""",
			[tid, commentTxt, uid])
		return None
	except:
		return "error"