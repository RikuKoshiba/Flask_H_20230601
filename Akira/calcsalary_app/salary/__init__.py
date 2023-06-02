from flask import Flask

app = Flask(__name__)
app.config.from_object('salary.config') 
#このモジュールがFlaskアプリケーションの環境設定用のオブジェクトになっているから
#このモジュールから(大文字だけの変数を)環境設定として読み込んでねという役割

import salary.views.views