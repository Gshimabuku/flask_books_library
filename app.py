from flask import Flask, render_template, jsonify
import os
from services.notion_service import get_courses

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

# --------------------------
# コース
# --------------------------
@app.route('/course/list')
def courses():
    data = get_courses()
    return render_template('courses/list.html', courses=data)

# --------------------------
# ラウンド
# --------------------------


if __name__ == '__main__':
    app.run(debug=True)
