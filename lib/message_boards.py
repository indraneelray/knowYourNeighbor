from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
import lib.Friends as Friends
import lib.Neighbors as Neighbors
import lib.Block as Block
import lib.Hood as Hood
class ServerError(Exception):pass

def getUserFriendThreads(db):
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
			tids = getLatestCommentTIDs(db, friendId, logout_time)
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

def getUserNeighborThreads(db):
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
			tids = getLatestCommentTIDs(db, neighborId, logout_time)
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


def getUserBlockThreads(db):
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
			blockTid = getLatestCommentTIDs(db, user, logout_time)
			if blockTid:
				tids.append(blockTid)
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

def getUserHoodThreads(db):
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
			hoodTid = getLatestCommentTIDs(db, user, logout_time)
			if hoodTid:
				tids.append(hoodTid)
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
	logging.info("getting latest comments")
	try:
		logging.info(logout_time)

		logout = str(logout_time)
		logging.info(logout)
		logging.info(type(logout_time))
		cur = db.query("""select distinct(tid) from ThreadComments where comment_by = %s and commentTime > %s""", (int(uid), logout))
		logging.info("success query")
		threads = []
		for c in cur.fetchall()[0]:
			threads.append(c)
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
	