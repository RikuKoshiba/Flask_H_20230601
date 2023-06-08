from flask import request, redirect, url_for, render_template, flash, session
from login_hack import app  # __init__.py が読まれている


def count_match_char(char, true_char):
    count = 0
    new_char = ""
    for i in range(len(char)):
        if char[i] not in new_char:
            new_char = new_char + char[i]
    for i in range(len(new_char)):
        if new_char[i] in true_char:
            count += 1
    return count


def count_match_char_and_pos(char, true_char, user=True):
    count = 0
    length = len(true_char) if len(char) >= len(true_char) else len(char)
    for i in range(length):
        if char[i] == true_char[i]:
            count += 1
            if session["flag_user"] and user:
                # print(session["msg_user"], type(session["msg_user"]))
                list1 = list(session["msg_user"])
                list1[i] = char[i]
                session["msg_user"] = "".join(list1)
            if session["flag_pass"] and user is not True:
                list1 = list(session["msg_pass"])
                list1[i] = char[i]
                session["msg_pass"] = "".join(list1)
    return count


@app.route("/")
def show_entries():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("result.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        comment = request.form["comment"]
        if session["comment_count"] == 2:
            flash("何も教えませんよ")
        elif session["comment_count"] == 3:
            flash("何も教えませんよ")
        elif session["comment_count"] == 4:
            flash("何も教えませんよ")
        elif session["comment_count"] == 5:
            flash("何も教えませんよ")
        elif session["comment_count"] == 6:
            flash("何も教えませんよ？")
        elif session["comment_count"] == 7:
            flash("・・・")
        elif session["comment_count"] == 8:
            flash("なんですか？")
        elif session["comment_count"] == 9:
            flash("何も教えません！")
        elif session["comment_count"] == 10:
            flash("・・・")
        elif session["comment_count"] == 11:
            flash("あの・・・")
        elif session["comment_count"] == 12:
            flash("えーと・・・")
        elif session["comment_count"] == 13:
            flash("・・・")
        elif session["comment_count"] == 14:
            flash("ヒ、ヒント・・")
        elif session["comment_count"] == 15:
            flash("ヒント出します・・・")
        elif session["comment_count"] == 20:
            flash("通算で20回教えを請われました")
        elif session["comment_count"] == 30:
            flash("教えちゃいまーす♪")
            flash(f"ユーザ名: {app.config['USERNAME']} パスワード: {app.config['PASSWORD']}")

        if "教えて" in comment:
            session["comment_count"] += 1

        if session["comment_count"] < 16:
            if username != app.config["USERNAME"]:
                session["count"] += 1
                flash("ユーザ名が違います")
            elif password != app.config["PASSWORD"]:
                session["count"] += 1
                flash("パスワードが異なります")
            else:
                session["count"] += 1
                session["logged_in"] = True
                flash("ログインしました")
                return render_template("result.html", count=session["count"])
        else:
            if not session["flag_user"]:
                if len(username) != len(app.config["USERNAME"]):
                    flash("ユーザ名の長さが違います ＞＜")
                else:
                    session["flag_user"] = True
                    for _ in range(len(app.config["USERNAME"])):
                        session["msg_user"] = session["msg_user"] + "?"
                    flash("ユーザ名の長さがあってます！やったー！")
            if not session["flag_pass"]:
                if len(password) != len(app.config["PASSWORD"]):
                    flash("パスワードの長さが違います　すいません ＞＜")
                else:
                    session["flag_pass"] = True
                    for _ in range(len(app.config["PASSWORD"])):
                        session["msg_pass"] = session["msg_pass"] + "?"
                    flash("ユーザ名の長さがあってます！やったー！")
            if (username == app.config["USERNAME"]) and (password == app.config["PASSWORD"]):
                session["count"] += 1
                session["logged_in"] = True
                flash("ログインしました")
                return render_template("result.html", count=session["count"])
            else:
                flash(f"ユーザ名は{count_match_char_and_pos(username, app.config['USERNAME'])}文字 位置と種類があってます！")
                flash(f"パスワードは{count_match_char_and_pos(password, app.config['PASSWORD'], user=False)}文字 位置と種類があってます！")

    elif request.method == "GET":
        session["count"] = 0
        session["comment_count"] = 29
        session["msg_user"] = ""
        session["msg_pass"] = ""
        session["flag_user"] = False
        session["flag_pass"] = False
        flash("天の声を誘導してユーザ名とパスワードを聞き出そう")
    return render_template("login.html", usr=session["msg_user"], pas=session["msg_pass"])


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))
