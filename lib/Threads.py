from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for

def getMessagesFromTID(db,tid):
    cur = db.query("""select comment_message from messages where threadid = %s order by posted_at""", [tid])
    comments = []
    if cur.fetchall():
        comments.append(cur.fetchall()[0])
    return comments

