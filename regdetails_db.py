########################################################################
# Authors: Ellen Su and Shayna Maleson                                 #
# Netids: eysu and smaleson                                            #
# File: regdetails_db.py                                               #
# Description: Module for DB operations for regdetails.py.  Catches    #
#              database errors and prints an error message to stderr.  #
########################################################################

from contextlib import closing
from sqlite3 import connect

# This file may throw a DatabaseError - it does not except these errors

DATABASE_URL = "file:reg.sqlite?mode=ro"


# returns a boolean: True if the given classid appears in the classes
# table, False otherwise. Validate classid before calling any other
# methods that use classid.
def is_valid_classid(classid):
    stmt = "SELECT 1 FROM classes WHERE classid=?"
    # if length of list is 0, no class with that classid exists
    return len(db_access(stmt, [classid])) != 0


# returns a tuple containing the courseid, days,
# starttime, endtime, bldg, and roomnum for the given classid.
def get_class_info(classid):
    stmt = "SELECT courseid, days, starttime, endtime, " \
           "bldg, roomnum FROM classes WHERE classid=?"
    return db_access(stmt, [classid])[0]


# returns the courseid for a given classid
def get_course_id(classid):
    stmt = "SELECT courseid FROM classes WHERE classid=?"
    return db_access(stmt, [classid])[0][0]


# returns a list of tuples of department and coursenum for the
# given courseid
def get_dept_and_num(courseid):
    stmt = "SELECT dept, coursenum FROM crosslistings " \
           "WHERE courseid=? ORDER BY dept, coursenum"
    return db_access(stmt, [courseid])


# returns a tuple of area, title, descrip, and
# prereqs for the given courseid.
def get_course_info(courseid):
    stmt = "SELECT area, title, descrip, prereqs FROM" \
           " courses WHERE courseid=?"
    return db_access(stmt, [courseid])[0]


# returns a list of tuples of profnames for the given courseid
def get_profs(courseid):
    stmt = "SELECT profname FROM coursesprofs, profs " \
           "WHERE courseid=? AND coursesprofs.profid" \
           "=profs.profid ORDER BY profname"
    return db_access(stmt, [courseid])


# method to access the database with the given prepared
# statement and argument list. Returns a list of matching rows,
# which is empty if no rows match.
# may throw a database error
def db_access(stmt, arglist):
    with connect(DATABASE_URL, isolation_level=None,
                 uri=True) as connection:
        with closing(connection.cursor()) as cursor:

            cursor.execute(stmt, arglist)
            return cursor.fetchall()
