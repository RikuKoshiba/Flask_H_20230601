from flask import Flask

app = Flask(__name__)

# http://127.0.0.1:5000/にリクエストがあったら hellow_world()メソッドが起動


@app.route("/")
def hello_world():
    return "Hello World!"


# @app.route("/<username>/")
# def profile(username):
#     return "hello I'm {username}"

# __name__ にはファイルの実行時とライブラリとして呼びだされたときで違うものが入る
# 実行時と呼び出し時で別の挙動をさせるならこの書き方をする
# HTML, CSS, JavaScriptで書くホームページをFlaskを使うことでPython形式で記述できる


if __name__ == "__main__":
    app.run()
