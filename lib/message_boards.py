from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import bcrypt
import logging
class ServerError(Exception):pass

def getUserThreads(db):
	error = None
	try:
		threadlist = []
		cur = db.query('select * from MessageThreads')
		for row in cur.fetchall():
			threadlist.append({'CreatedBy': row[0], 'Title': row[1], 'Description_Msg': row[2], 'CreatedAt': row[3]})
		return threadlist
	except:
		error = "Failed"
		return error