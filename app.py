from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
return render_template('home.html')

@app.route('/list')
def list_page():
return render_template('list.html')

@app.route('/detail')
def detail_page():
return render_template('detail.html')

if __name__ == '__main__':
app.run(debug=True)
