from flask import Flask

app = Flask(__name__)
app.config.from_object('holiday.config')

# 使用するすべてのviewsファイルを読み込む
from holiday.views import views, list