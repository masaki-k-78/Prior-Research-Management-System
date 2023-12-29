import os
from flask import Flask, request, render_template

app = Flask(__name__)

# login処理です
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        print("POSTされたIDは?" + str(request.form['id']))
        print("POSTされたPASSWORDは?" + str(request.form['pwd']))
        return render_template('sample.html')
    else:
        return render_template('sample.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "ok!"

if __name__ == "__main__":
    app.run(port=12345, debug=False)