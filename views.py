import base64
import os
from flask import Blueprint, flash, redirect, render_template, request, json, session
from flask_login import login_required, current_user, logout_user, login_user

from languages import languages_ace
from models import Room, User, db, Invitations
from socket_server import active_users

flask_views = Blueprint("main_routes", "main_routes")




@flask_views.route("/session/<room_name>")
def view_session(room_name,username=''):
    room = Room.query.filter_by(room_name=room_name).first()
    if not room:
        return "Unable to find that room"
    if not room.active and current_user.id != room.owner_id:
        return "Room no longer available"
    if room.require_registered :
        if current_user.is_anonymous:
            return redirect("/login?next=/session/%s"%room_name)
        if not current_user.is_admin:
            if room.invite_only:
                if current_user.email not in [invite.email_address for invite in room.invited_users] + [room.owner.email,]:
                    return "not authorized to enter room"

        elif request.form:
            pass # if request.form.get('')
    try:
        username = current_user.username
    except:
        username = ""
    ctx = dict(
        room = room.to_dict(),
        username=username
    )
    if username in [x['username'] for x in active_users.get(room_name,[])]:
        return "You are already in this room... please check your other tabs and try again"
    return render_template('code_editor.html',**ctx)

@flask_views.route("/logout")
@login_required
def do_logout():
    logout_user()
    return redirect("/login")

@flask_views.route("/login",methods=["GET","POST"])
def do_login():
    if request.form:
        user = request.form.get('username',None)
        pw = request.form.get('password',None)
        if User.login(user,pw):
            return redirect(request.args.get("next","/"))
    return render_template("login.html")

@flask_views.route("/join/<room_id>/<token>")
def join_room(room_id,token):
    invitation = Invitations.query.filter_by(invite_code=token,room_id=room_id).first()
    if not invitation:
        return "sorry buddy"
    session["X-token-coderpad"] = base64.b64encode(token)
    print "OK CREATED TOKEN:",request,session["X-token-coderpad"]
    login_user(User.user_loader("ASDASD"),force=True)
    return redirect('session/'+invitation.room.room_name)


