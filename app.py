from flask import Flask, render_template
from notion_service import get_courses
import os

app = Flask(__name__)

# ホーム画面
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------
# /courses 一覧表示
# -------------------------
@app.route('/courses')
def courses_list():
    courses = get_courses()
    return render_template('courses/list.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
