from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from flask_blog.models.entries import Entry
from flask_blog.models.users import Users
from flask_blog import db
from datetime import datetime
from flask_blog.views.views import login_required


@app.route("/", methods=["GET", "POST"])
@login_required
def show_entries():
    # entries = Entry.query.order_by(Entry.id.desc()).all()
    # entries = Entry.query.join(Users, Users.id == Entry.user_id).all()
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


@app.route("/entries/user_entries", methods=["GET", "POST"])
@login_required
def show_user_entries():
    user_id = session["user_id"]
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
@login_required
def show_entry(id):
    entry = Entry.query.get(id)
    user_id = session["user_id"]
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
    entry.tite = request.form["title"]
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
