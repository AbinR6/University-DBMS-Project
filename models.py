"""
models.py — Data structures for the University Academic Management System.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Department:
    dno: str
    dname: str
    location: str
    head_instructor_id: Optional[str] = None


@dataclass
class Student:
    roll_no: str
    name: str
    dob: str
    dept_no: str


@dataclass
class Instructor:
    ino: str
    iname: str
    designation: str
    mobile_no: str
    room_no: str
    dept_no: str


@dataclass
class Course:
    cno: str
    cname: str
    duration: str
    prerequisites: str
    dept_no: str


@dataclass
class Enrollment:
    roll_no: str
    cno: str
    grade: str
