from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from flask_blog.models.entries import Entry
from flask_blog.models.users import Users
from flask_blog import db
from datetime import datetime
from flask_blog.views.views import login_required
from functools import wraps


def search_session_reset(view):
    @wraps(view)
    def inner(*args, **kwargs):
        session.pop("search_keyword_title", "")
        session.pop("search_keyword_username", "")
        session.pop("search_keyword_maintext", "")
        session.pop("search_time_start_str", "")
        session.pop("search_time_end_str", "")
        return view(*args, **kwargs)
    return inner


@app.route("/entries/search", methods=["POST"])
# @login_required
def search_result():
    if request.form["btn"] == "back":
        search_keyword_title = session.pop("search_keyword_title", "")
        search_keyword_username = session.pop("search_keyword_username", "")
        search_keyword_maintext = session.pop("search_keyword_maintext", "")

        search_time_start_str = session.pop("search_time_start_str", "")
        search_time_end_str = session.pop("search_time_end_str", "")

        search_time_start_datetime = str2datetime(search_time_start_str)
        search_time_end_datetime = str2datetime(search_time_end_str)
    else:
        search_keyword_title = request.form["title"]
        search_keyword_username = request.form["username"]
        search_keyword_maintext = request.form["maintext"]
        search_time_start_str = request.form["startdatetime"]
        search_time_end_str = request.form["enddatetime"]

        search_time_start_datetime = str2datetime(search_time_start_str)
        search_time_end_datetime = str2datetime(search_time_end_str)
        # print(search_time_start_datetime, search_time_end_datetime)

    entries = db.session.query(
        Entry.id,
        Entry.title,
        Entry.text,
        Entry.user_id,
        Entry.created_at,
        Entry.last_edited_at,
        Users.username
        ).\
        join(Users, Users.id == Entry.user_id)
    if search_keyword_title != "":
        entries = entries.filter(Entry.title.contains(search_keyword_title))

    if search_keyword_username != "":
        entries = entries.\
            filter(Users.username.contains(search_keyword_username))

    if search_keyword_maintext != "":
        entries = entries.\
            filter(Entry.text.contains(search_keyword_maintext))

    if search_time_start_str != "":
        entries = entries.\
            filter(Entry.created_at >= search_time_start_datetime)

    if search_time_end_str != "":
        entries = entries.\
            filter(Entry.created_at <= search_time_end_datetime)

    entries = entries.order_by(Entry.id.desc()).all()
    session["before_page"] = "search_result"
    # session["entries"] = [entries]
    session["search_keyword_title"] = search_keyword_title
    session["search_keyword_username"] = search_keyword_username
    session["search_keyword_maintext"] = search_keyword_maintext
    session["search_time_start_str"] = search_time_start_str
    session["search_time_end_str"] = search_time_end_str
    return render_template("entries/index.html", entries=entries)


@app.route("/", methods=["GET", "POST"])
# @login_required
@search_session_reset
def show_entries():
    entries = db.session.query(
        Entry.id,
        Entry.title,
        Entry.text,
        Entry.user_id,
        Entry.created_at,
        Entry.last_edited_at,
        Users.username
        ).join(Users, Users.id == Entry.user_id).\
        order_by(Entry.id.desc()).all()
    session["before_page"] = "show_entries"
    return render_template("entries/index.html", entries=entries)


@app.route("/entries/new", methods=["GET"])
@login_required
def new_entry():
    return render_template("entries/new.html")


@app.route("/entries", methods=["POST"])
@login_required
def add_entry():
    user_id = session.get("user_id")
    entry = Entry(
        title=request.form["title"],
        text=request.form["text"],
        user_id=user_id
        )
    db.session.add(entry)
    db.session.commit()
    flash("新しく記事が作成されました")
    return redirect(url_for("show_entries"))


@app.route("/my_entries", methods=["GET", "POST"])
@login_required
@search_session_reset
def show_user_entries():
    user_id = session.get("user_id", None)
    entries = db.session.query(
        Entry.id,
        Entry.title,
        Entry.text,
        Entry.user_id,
        Entry.created_at,
        Entry.last_edited_at,
        Users.username
        ).\
        join(Users, Users.id == Entry.user_id).\
        filter(Entry.user_id == user_id).\
        order_by(Entry.id.desc()).all()
    session["before_page"] = "show_user_entries"
    return render_template("entries/index.html", entries=entries)


@app.route("/entries/<int:id>", methods=["GET"])
# @login_required
def show_entry(id):
    entry = Entry.query.get(id)
    user_id = session.get("user_id", None)
    writer = Users.query.get(entry.user_id)
    return render_template("entries/show.html",
                           entry=entry,
                           user_id=user_id,
                           writer=writer)


@app.route("/entries/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry(id):
    entry = Entry.query.get(id)
    return render_template("entries/edit.html", entry=entry)


@app.route("/entries/<int:id>/update", methods=["POST"])
@login_required
def update_entry(id):
    entry = Entry.query.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    entry.last_edited_at = datetime.utcnow()
    db.session.merge(entry)
    db.session.commit()
    flash("記事が更新されました")
    return redirect(url_for("show_entries"))


@app.route("/entries/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash("投稿が削除されました")
    return redirect(url_for("show_entries"))


def str2datetime(string):
    if string == "":
        return None
    res = datetime.strptime(
        string,
        '%Y-%m-%dT%H:%M'
        )
    return res
