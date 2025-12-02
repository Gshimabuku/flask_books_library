from flask import Flask, render_template
from services.notion_service import get_courses
from config import NOTION_API_KEY

app = Flask(__name__)


# -------------------------
# ホーム
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')


# -------------------------
# コース一覧
# -------------------------
@app.route('/courses')
def courses_list():
    courses = get_courses()
    return render_template('courses/list.html', courses=courses)


# -------------------------
# デバッグ：環境変数確認
# -------------------------
@app.route('/debug/env')
def debug_env():
    return {
        "NOTION_API_KEY_exists": bool(NOTION_API_KEY),
    }


if __name__ == '__main__':
    app.run(debug=True)
