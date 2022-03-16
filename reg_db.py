#!/usr/bin/env python

# -------------------------------------------------------------------
# Authors: Ellen Su and Shayna Maleson
# Netids: eysu and smaleson
# File: reg_db.py
# Description: Return information about the classes that match the
# specified department, number, distribution area, and title
# -------------------------------------------------------------------

from contextlib import closing
from sqlite3 import connect

# -------------------------------------------------------------------
DATABASE_URL = "file:reg.sqlite?mode=ro"

# This file may throw a DatabaseError - it does not except these errors


# takes 4 course attributes
# or empty strings if not specified and returns
# may throw a database error
def db_access(dept, num, area, title):
    with connect(DATABASE_URL, isolation_level=None,
                 uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            stmt_str = "SELECT classid, dept, coursenum, area, title "
            stmt_str += "FROM classes, crosslistings, courses "
            # line up the three tables
            stmt_str += "WHERE classes.courseid = " \
                        "crosslistings.courseid "
            stmt_str += "AND classes.courseid = courses.courseid "
            # filter for department
            stmt_str += "AND crosslistings.dept LIKE ? "
            # filter for course number
            stmt_str += "AND crosslistings.coursenum LIKE ? "
            # filter for distribution area
            stmt_str += "AND courses.area LIKE ? "
            # filter for course title
            stmt_str += "AND courses.title LIKE ? ESCAPE '\\'"
            # order of outputted classes
            stmt_str += "ORDER BY dept, coursenum, classid "

            dept_ = '%' + str(dept) + '%'
            num_ = '%' + str(num) + '%'
            area_ = '%' + str(area) + '%'
            title_ = '%' + \
                 str(title).replace(r'%', r'\%').replace(r'_', r'\_')\
                 + '%'
            cursor.execute(stmt_str, [dept_, num_, area_, title_])
            return cursor.fetchall()
