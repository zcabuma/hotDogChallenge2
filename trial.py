from flask import Flask, render_template
from flask import request
app = Flask(__name__)
import testingAPI

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    src = request.args.get('src')
    print(src)
    result = testingAPI.callAPI(src)
    return render_template('result.html', result=result)

