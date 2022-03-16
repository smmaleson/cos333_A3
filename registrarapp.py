from flask import Flask, render_template, request, make_response
import reg_db
import regdetails_db

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def base():

    umm = request.cookies.get('prev_dept')

    dept = request.args.get('dept')
    dept = dept if (dept is not None) else ''  # for initial search

    num = request.args.get('number')
    num = num if (num is not None) else ''

    area = request.args.get('area')
    area = area if (area is not None) else ''

    title = request.args.get('title')
    title = title if (title is not None) else ''

    # DEBUG
    # print('dept:', dept)
    # print('num:', num)
    # print('area:', area)
    # print('title:', title)
    # print('umm: ', umm)
    # DEBUG

    courses = reg_db.db_access(dept, num, area, title)

    html = render_template('index.html', courses=courses)
    response = make_response(html)

    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', num)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)

    return response


@app.route('/regdetails/', methods=['GET'])
def details():
    classid = request.args.get('classid')

    # print(request.cookies.get('prev_dept'))

    if not regdetails_db.is_valid_classid(classid):
        None # ERROR HANDLING

    courseid, days, starttime, endtime, bldg, roomnum = regdetails_db.get_class_info(classid)

    area, title, descrip, prereqs = regdetails_db.get_course_info(courseid)

    depts = regdetails_db.get_dept_and_num(courseid)
    profs = regdetails_db.get_profs(courseid)

    return render_template('details.html', classid=classid, courseid=courseid, days=days,
                           starttime=starttime, endtime=endtime, bldg=bldg, roomnum=roomnum,
                           area=area, title=title, descrip=descrip, prereqs=prereqs,
                           depts=depts, profs=profs,
                           prev_dept=request.cookies.get('prev_dept'),
                           prev_num=request.cookies.get('prev_num'),
                           prev_area=request.cookies.get('prev_area'),
                           prev_title=request.cookies.get('prev_title'))
