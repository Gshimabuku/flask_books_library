from flask import Flask, render_template
from config import NOTION_API_KEY

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list')
def list_page():
    return render_template('list.html')

@app.route('/detail')
def detail_page():
    return render_template('detail.html')

@app.route('/debug/env')
def debug_env():
    # 確認用に NOTION_API_KEY の存在のみ表示
    # 本番では削除してください
    token_status = "読み込めています" if NOTION_API_KEY else "読み込めていません"
    return f"<h1>Notion Token 確認</h1><p>NOTION_API_KEY: {token_status}</p>"

if __name__ == '__main__':
    app.run(debug=True)
