#!/usr/bin/env python

# ----------------------------------------------------------------------
# registrarapp.py
# Author: Shayna Maleson, Ellen Su
# ----------------------------------------------------------------------

from sqlite3 import DatabaseError
from sys import stderr

from flask import Flask, render_template, request, make_response
import reg_db
import regdetails_db

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def base():

    dept = request.args.get('dept')
    dept = dept if (dept is not None) else ''  # for initial search

    num = request.args.get('number')
    num = num if (num is not None) else ''

    area = request.args.get('area')
    area = area if (area is not None) else ''

    title = request.args.get('title')
    title = title if (title is not None) else ''

    try:
        courses = reg_db.db_access(dept, num, area, title)
    except DatabaseError as ex:
        errormsg = 'A server error occurred. Please contact a system ' \
                   'administrator.'
        print(ex, file=stderr)
        return render_template('errorpage.html', errormessage=errormsg)

    html = render_template('index.html', courses=courses, dept=dept,
                           num=num, area=area, title=title)
    response = make_response(html)

    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', num)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)

    return response


@app.route('/regdetails', methods=['GET'])
def details():
    classid = request.args.get('classid')

    if classid is None or classid == '':
        errormsg = 'Error: missing classid'
        return render_template('errorpage.html', errormessage=errormsg)

    try:
        int(classid)
    except Exception:
        errormsg = 'Error: non-integer classid'
        return render_template('errorpage.html', errormessage=errormsg)

    try:
        if not regdetails_db.is_valid_classid(classid):
            errormsg = f'Error: No class with classid {classid} exists'
            return render_template('errorpage.html',
                                   errormessage=errormsg)

        courseid, days, starttime, \
        endtime, bldg, roomnum = regdetails_db.get_class_info(classid)

        area, title, \
        descrip, prereqs = regdetails_db.get_course_info(courseid)

        depts = regdetails_db.get_dept_and_num(courseid)
        profs = regdetails_db.get_profs(courseid)
    except DatabaseError as ex:
        errormsg = 'A server error occurred. Please contact a system ' \
                   'administrator.'
        print(ex, file=stderr)
        return render_template('errorpage.html', errormessage=errormsg)

    return render_template('details.html', classid=classid,
                           courseid=courseid, days=days,
                           starttime=starttime, endtime=endtime,
                           bldg=bldg, roomnum=roomnum, area=area,
                           title=title, descrip=descrip,
                           prereqs=prereqs, depts=depts, profs=profs,
                           prev_dept=request.cookies.get('prev_dept'),
                           prev_num=request.cookies.get('prev_num'),
                           prev_area=request.cookies.get('prev_area'),
                           prev_title=request.cookies.get('prev_title'))

if __name__ == '__main__':
    main()
