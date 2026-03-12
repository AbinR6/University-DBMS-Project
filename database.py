"""
database.py — SQLite connection manager and CRUD operations for all entities.
"""

import sqlite3
import os
import sys


def _get_base_dir():
    """Return the directory where the .exe (or .py script) lives."""
    if getattr(sys, "frozen", False):
        # Running as a PyInstaller bundle
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


DB_PATH = os.path.join(_get_base_dir(), "university.db")


class DatabaseManager:
    """Single persistent connection manager for the SQLite database."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self._create_tables()

    # ------------------------------------------------------------------ #
    #  Table creation
    # ------------------------------------------------------------------ #
    def _create_tables(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Department (
                DNo        TEXT PRIMARY KEY,
                DName      TEXT NOT NULL,
                Location   TEXT NOT NULL,
                HeadInstructorID TEXT
            );

            CREATE TABLE IF NOT EXISTS Student (
                RollNo  TEXT PRIMARY KEY,
                Name    TEXT NOT NULL,
                DOB     TEXT NOT NULL,
                DeptNo  TEXT NOT NULL,
                FOREIGN KEY (DeptNo) REFERENCES Department(DNo)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Instructor (
                INo         TEXT PRIMARY KEY,
                IName       TEXT NOT NULL,
                Designation TEXT NOT NULL,
                MobileNo    TEXT NOT NULL,
                RoomNo      TEXT NOT NULL,
                DeptNo      TEXT NOT NULL,
                FOREIGN KEY (DeptNo) REFERENCES Department(DNo)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Course (
                CNo           TEXT PRIMARY KEY,
                CName         TEXT NOT NULL,
                Duration      TEXT NOT NULL,
                PreRequisites TEXT,
                DeptNo        TEXT NOT NULL,
                FOREIGN KEY (DeptNo) REFERENCES Department(DNo)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Enrollment (
                RollNo TEXT NOT NULL,
                CNo    TEXT NOT NULL,
                Grade  TEXT,
                PRIMARY KEY (RollNo, CNo),
                FOREIGN KEY (RollNo) REFERENCES Student(RollNo)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (CNo) REFERENCES Course(CNo)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)
        self.conn.commit()

    # ------------------------------------------------------------------ #
    #  Generic helpers
    # ------------------------------------------------------------------ #
    def _execute(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()

    def _fetchall(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    # ================================================================== #
    #  DEPARTMENT CRUD
    # ================================================================== #
    def add_department(self, dno, dname, location, head_id=""):
        self._execute(
            "INSERT INTO Department (DNo, DName, Location, HeadInstructorID) VALUES (?, ?, ?, ?)",
            (dno, dname, location, head_id),
        )

    def get_all_departments(self):
        return self._fetchall("SELECT * FROM Department")

    def update_department(self, dno, dname, location, head_id):
        self._execute(
            "UPDATE Department SET DName=?, Location=?, HeadInstructorID=? WHERE DNo=?",
            (dname, location, head_id, dno),
        )

    def delete_department(self, dno):
        self._execute("DELETE FROM Department WHERE DNo=?", (dno,))

    # ================================================================== #
    #  STUDENT CRUD
    # ================================================================== #
    def add_student(self, roll_no, name, dob, dept_no):
        self._execute(
            "INSERT INTO Student (RollNo, Name, DOB, DeptNo) VALUES (?, ?, ?, ?)",
            (roll_no, name, dob, dept_no),
        )

    def get_all_students(self):
        return self._fetchall("SELECT * FROM Student")

    def update_student(self, roll_no, name, dob, dept_no):
        self._execute(
            "UPDATE Student SET Name=?, DOB=?, DeptNo=? WHERE RollNo=?",
            (name, dob, dept_no, roll_no),
        )

    def delete_student(self, roll_no):
        self._execute("DELETE FROM Student WHERE RollNo=?", (roll_no,))

    # ================================================================== #
    #  INSTRUCTOR CRUD
    # ================================================================== #
    def add_instructor(self, ino, iname, designation, mobile, room, dept_no):
        self._execute(
            "INSERT INTO Instructor (INo, IName, Designation, MobileNo, RoomNo, DeptNo) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (ino, iname, designation, mobile, room, dept_no),
        )

    def get_all_instructors(self):
        return self._fetchall("SELECT * FROM Instructor")

    def update_instructor(self, ino, iname, designation, mobile, room, dept_no):
        self._execute(
            "UPDATE Instructor SET IName=?, Designation=?, MobileNo=?, RoomNo=?, DeptNo=? "
            "WHERE INo=?",
            (iname, designation, mobile, room, dept_no, ino),
        )

    def delete_instructor(self, ino):
        self._execute("DELETE FROM Instructor WHERE INo=?", (ino,))

    # ================================================================== #
    #  COURSE CRUD
    # ================================================================== #
    def add_course(self, cno, cname, duration, prerequisites, dept_no):
        self._execute(
            "INSERT INTO Course (CNo, CName, Duration, PreRequisites, DeptNo) "
            "VALUES (?, ?, ?, ?, ?)",
            (cno, cname, duration, prerequisites, dept_no),
        )

    def get_all_courses(self):
        return self._fetchall("SELECT * FROM Course")

    def update_course(self, cno, cname, duration, prerequisites, dept_no):
        self._execute(
            "UPDATE Course SET CName=?, Duration=?, PreRequisites=?, DeptNo=? WHERE CNo=?",
            (cname, duration, prerequisites, dept_no, cno),
        )

    def delete_course(self, cno):
        self._execute("DELETE FROM Course WHERE CNo=?", (cno,))

    # ================================================================== #
    #  ENROLLMENT CRUD
    # ================================================================== #
    def add_enrollment(self, roll_no, cno, grade):
        self._execute(
            "INSERT INTO Enrollment (RollNo, CNo, Grade) VALUES (?, ?, ?)",
            (roll_no, cno, grade),
        )

    def get_all_enrollments(self):
        return self._fetchall("SELECT * FROM Enrollment")

    def update_enrollment(self, roll_no, cno, grade):
        self._execute(
            "UPDATE Enrollment SET Grade=? WHERE RollNo=? AND CNo=?",
            (grade, roll_no, cno),
        )

    def delete_enrollment(self, roll_no, cno):
        self._execute("DELETE FROM Enrollment WHERE RollNo=? AND CNo=?", (roll_no, cno))

    # ================================================================== #
    #  LOOKUP HELPERS  (for Combobox drop-downs)
    # ================================================================== #
    def get_department_ids(self):
        return [row[0] for row in self._fetchall("SELECT DNo FROM Department")]

    def get_student_rolls(self):
        return [row[0] for row in self._fetchall("SELECT RollNo FROM Student")]

    def get_instructor_ids(self):
        return [row[0] for row in self._fetchall("SELECT INo FROM Instructor")]

    def get_course_ids(self):
        return [row[0] for row in self._fetchall("SELECT CNo FROM Course")]
