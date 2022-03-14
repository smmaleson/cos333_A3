from flask import Flask, render_template

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def base():
    return render_template('index.html')


@app.route('/regdetails/', methods=['GET'])
def details():
    return render_template('searchresults.html')