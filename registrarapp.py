from flask import Flask, render_template, request, make_response
import reg_db
import regdetails_db

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def base():

    dept = request.args.get('dept')
    print('dept:', dept)
    num = request.args.get('number')
    print('num:', num)
    print(type(num))
    area = request.args.get('area')
    print('area:', area)
    title = request.args.get('title')
    print('title:', title)

    courses = reg_db.db_access(dept, num, area, title)

    html = render_template('index.html', courses=courses)
    response = make_response(html)
    # response.set_cookie('prev_author', author)

    return response


@app.route('/regdetails/', methods=['GET'])
def details():
    return render_template('searchresults.html')