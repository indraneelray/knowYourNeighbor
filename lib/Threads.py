from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for

def getMessagesFromTID(db,tid):
    cur = db.query("""select comment_Msg from threadcomments where tid = %s order by commentTime""", [tid])
    comments = []
    if cur.fetchall():
        comments.append(cur.fetchall()[0])
    return comments

