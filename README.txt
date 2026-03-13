# University Academic Management System
A desktop database management application developed using **Python**, **Tkinter**, and **SQLite**. The system manages university data such as departments, instructors, students, courses, and enrollments through a graphical interface while maintaining relational database integrity.

The application runs completely **offline** and stores all information in a local SQLite database.

---

## Team Members

| Name                 | Roll Number |
| -------------------- | ----------- |
| Abin Aby             | Roll No  14 |
| Adarsh S. Saji       | Roll No  16 |
| Ajesh S. Sathyan     | Roll No  24 |
| Alwin Alex           | Roll No  30 |
| Aravind Swaminath P. | Roll No  37 |

---

## Course Information

Course: **Database Management Systems**
Project: **University Management System SQL Mini Project**
Institution: *APJ KTU University STIST*

---

## Features

* Add, update, and delete departments
* Manage instructor records
* Manage student records
* Create and manage courses
* Enroll students in courses
* Display database tables in an interactive interface
* Offline database storage using SQLite
* Graphical interface built with Tkinter

---

## Technologies Used

* **Python**
* **Tkinter** (GUI)
* **SQLite** (Database)
* **PyInstaller** (Executable packaging)

---

## Project Structure

```
DBMS_PROJECT
│
├── main.py          # Application entry point
├── gui.py           # Tkinter interface and layout
├── database.py      # Database connection and queries
├── models.py        # Data models and structure
├── university.db    # SQLite database file
└── README.md
```

---

## Database Entities

The system contains five main entities:

| Entity     | Description                    |
| ---------- | ------------------------------ |
| Department | Stores department information  |
| Instructor | Stores faculty details         |
| Student    | Stores student information     |
| Course     | Stores course information      |
| Enrollment | Connects students with courses |

---

## Database Relationships

* A **department offers many courses**
* A **department has multiple instructors**
* A **department is headed by an instructor**
* A **student can enroll in multiple courses**
* A **course can have multiple students**

---

## Running the Project

### Option 1 – Run with Python

```
python main.py
```

### Option 2 – Run Executable

Double-click:

```
UniversityDB.exe
```

No Python installation required.
