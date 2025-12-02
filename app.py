from flask import Flask, render_template, jsonify
import os
from services.notion_service import get_courses

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# --------------------------
# ① 環境変数の読み取りテスト
# --------------------------
@app.route('/debug/env')
def debug_env():
    return jsonify({
        "NOTION_API_KEY": os.getenv("NOTION_API_KEY"),
        "NOTION_DB_COURSES_ID": os.getenv("NOTION_DB_COURSES_ID"),
        "NOTION_DB_LAYOUTS_ID": os.getenv("NOTION_DB_LAYOUTS_ID"),
        "NOTION_DB_HOLES_ID": os.getenv("NOTION_DB_HOLES_ID"),
    })

# --------------------------
# ② Notion API の実データ確認
# --------------------------
@app.route('/debug/notion')
def debug_notion():
    try:
        data = get_courses()
        return jsonify({
            "status": "success",
            "count": len(data),
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error_message": str(e)
        }), 500

# --------------------------
# コース一覧画面
# --------------------------
@app.route('/courses')
def courses():
    data = get_courses()
    return render_template('courses.html', courses=data)


if __name__ == '__main__':
    app.run(debug=True)
