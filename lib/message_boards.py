from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import logging
class ServerError(Exception):pass

def getUserThreads(db):
	error = None
	try:
		logging.info("getting user threads")
		threadlist = []
		uid = session['uid']
		cur = db.query("""select * from MessageThreads where created_by = %s order by created_time limit 10;""", [uid])
		for row in cur.fetchall():
			threadlist.append({'CreatedBy': row[0], 'Title': row[1], 'Description_Msg': row[2], 'CreatedAt': row[3]})
		return threadlist
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
		cur = db.query("""INSERT INTO MessageThreads(Created_By, Title, Description_Msg, Created_Time, Access_Level)VALUES\
			(%s,%s,%s,NOW(),%s)""", [uid, threadTitle, description, access_level])
	except:
		logging.info("error fetching user threads")
		error = "Failed"
		return error

