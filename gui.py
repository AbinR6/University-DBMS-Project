"""
gui.py — Modern Tkinter GUI using ttkbootstrap for the University Academic
Management System.

Uses frame-switching inside a single window. Each entity has a LabelFrame
form section and a Treeview table with proper padding and modern styling.
Dashboard stat cards are clickable.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter.ttk as std_ttk
from database import DatabaseManager


class UniversityApp:
    """Main application — single window, sidebar navigation, modern forms."""

    def __init__(self, root: ttk.Window):
        self.root = root
        self.root.title("University Database")
        self.root.geometry("1100x680")
        self.root.minsize(960, 600)

        self.db = DatabaseManager()

        self._build_layout()
        self._show_frame("dashboard")

    # ------------------------------------------------------------------ #
    #  Layout
    # ------------------------------------------------------------------ #
    def _build_layout(self):
        # ---- Sidebar ----
        side = ttk.Frame(self.root, bootstyle="light")
        side.pack(side=LEFT, fill=Y)

        # Brand
        brand = ttk.Frame(side, bootstyle="light")
        brand.pack(fill=X, padx=20, pady=(24, 4))
        ttk.Label(brand, text="UniDB", font=("Segoe UI", 18, "bold"),
                  bootstyle="primary").pack(anchor=W)
        ttk.Label(brand, text="Academic Manager",
                  font=("Segoe UI", 9), bootstyle="secondary").pack(anchor=W)

        ttk.Separator(side).pack(fill=X, padx=16, pady=14)

        # Nav items
        nav = [
            ("Dashboard",   "dashboard"),
            ("Departments", "department"),
            ("Students",    "student"),
            ("Instructors", "instructor"),
            ("Courses",     "course"),
            ("Enrollments", "enrollment"),
        ]
        for label, key in nav:
            btn = ttk.Button(side, text=f"  {label}", bootstyle="light",
                             command=lambda k=key: self._show_frame(k),
                             width=20)
            btn.pack(fill=X, padx=8, pady=2)

        # ---- Content area ----
        self.content = ttk.Frame(self.root)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        # ---- Build all frames ----
        self.frames: dict[str, ttk.Frame] = {}
        self._build_dashboard()
        self._build_entity("department",
            title="Department Details",
            fields=[("Dept No", "entry"), ("Dept Name", "entry"),
                    ("Location", "entry"), ("Head Instructor", "combo")],
            columns=("DNo", "DName", "Location", "HeadInstructorID"),
        )
        self._build_entity("student",
            title="Student Details",
            fields=[("Roll No", "entry"), ("Name", "entry"),
                    ("DOB (YYYY-MM-DD)", "entry"), ("Department", "combo")],
            columns=("RollNo", "Name", "DOB", "DeptNo"),
        )
        self._build_entity("instructor",
            title="Instructor Details",
            fields=[("Instructor No", "entry"), ("Name", "entry"),
                    ("Designation", "entry"), ("Mobile No", "entry"),
                    ("Room No", "entry"), ("Department", "combo")],
            columns=("INo", "IName", "Designation", "MobileNo", "RoomNo", "DeptNo"),
            col_widths=[90, 130, 110, 110, 80, 80],
        )
        self._build_entity("course",
            title="Course Details",
            fields=[("Course No", "entry"), ("Course Name", "entry"),
                    ("Duration", "entry"), ("Pre-Requisites", "entry"),
                    ("Department", "combo")],
            columns=("CNo", "CName", "Duration", "PreRequisites", "DeptNo"),
            col_widths=[100, 160, 100, 140, 100],
        )
        self._build_entity("enrollment",
            title="Enrollment Details",
            fields=[("Roll No", "combo"), ("Course No", "combo"),
                    ("Grade", "entry")],
            columns=("RollNo", "CNo", "Grade"),
            col_widths=[220, 220, 160],
        )

    # ------------------------------------------------------------------ #
    #  Frame switching
    # ------------------------------------------------------------------ #
    def _show_frame(self, name: str):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill=BOTH, expand=True, padx=24, pady=24)
        refresh = getattr(self, f"_refresh_{name}", None)
        if refresh:
            refresh()

    # ================================================================== #
    #  DASHBOARD  (clickable stat cards)
    # ================================================================== #
    def _build_dashboard(self):
        fr = ttk.Frame(self.content)
        self.frames["dashboard"] = fr

        ttk.Label(fr, text="Dashboard",
                  font=("Segoe UI", 20, "bold")).pack(anchor=W, pady=(0, 4))
        ttk.Label(fr, text="Click a card to manage that section",
                  font=("Segoe UI", 10),
                  bootstyle="secondary").pack(anchor=W, pady=(0, 24))

        cards_row = ttk.Frame(fr)
        cards_row.pack(fill=X)

        self._stat_labels = {}
        items = [
            ("Departments",  "department",  "primary"),
            ("Students",     "student",     "success"),
            ("Instructors",  "instructor",  "info"),
            ("Courses",      "course",      "warning"),
            ("Enrollments",  "enrollment",  "danger"),
        ]

        for i, (name, key, style) in enumerate(items):
            cards_row.columnconfigure(i, weight=1)

            card = ttk.Frame(cards_row, padding=20)
            card.grid(row=0, column=i, padx=8, pady=8, sticky=NSEW)

            ttk.Label(card, text=name, font=("Segoe UI", 10, "bold"),
                      bootstyle=style).pack(fill=X, pady=(0, 4))

            count_lbl = ttk.Label(card, text="0",
                                  font=("Segoe UI", 28, "bold"),
                                  bootstyle=style, anchor=CENTER)
            count_lbl.pack(fill=X, pady=(4, 8))

            open_btn = ttk.Button(card, text=f"Open {name}",
                                  bootstyle=style,
                                  command=lambda k=key: self._show_frame(k))
            open_btn.pack(fill=X)

            self._stat_labels[name] = count_lbl

    def _refresh_dashboard(self):
        counts = {
            "Departments":  len(self.db.get_all_departments()),
            "Students":     len(self.db.get_all_students()),
            "Instructors":  len(self.db.get_all_instructors()),
            "Courses":      len(self.db.get_all_courses()),
            "Enrollments":  len(self.db.get_all_enrollments()),
        }
        for name, lbl in self._stat_labels.items():
            lbl.config(text=str(counts[name]))

    # ================================================================== #
    #  GENERIC ENTITY FRAME
    # ================================================================== #
    def _build_entity(self, key, *, title, fields, columns, col_widths=None):
        fr = ttk.Frame(self.content)
        self.frames[key] = fr

        ttk.Label(fr, text=title.replace(" Details", ""),
                  font=("Segoe UI", 20, "bold")).pack(anchor=W, pady=(0, 12))

        # ---- Input section (LabelFrame) ----
        form = std_ttk.LabelFrame(fr, text=title, padding=16)
        form.pack(fill=X, pady=(0, 16))

        widgets = []
        for i, (label, kind) in enumerate(fields):
            ttk.Label(form, text=label, font=("Segoe UI", 10)).grid(
                row=i, column=0, sticky=E, padx=(8, 12), pady=8)
            if kind == "entry":
                w = ttk.Entry(form, width=32, font=("Segoe UI", 10))
            else:
                w = ttk.Combobox(form, width=30, state="readonly",
                                 font=("Segoe UI", 10))
            w.grid(row=i, column=1, sticky=W, padx=(0, 16), pady=8)
            widgets.append(w)

        # Buttons row
        btn_row = ttk.Frame(form)
        btn_row.grid(row=len(fields), column=0, columnspan=2, pady=(12, 4))

        ttk.Button(btn_row, text="  Add  ", bootstyle="primary",
                   command=lambda: self._crud(key, "add")).pack(
            side=LEFT, padx=4)
        ttk.Button(btn_row, text="  Update  ", bootstyle="success",
                   command=lambda: self._crud(key, "update")).pack(
            side=LEFT, padx=4)
        ttk.Button(btn_row, text="  Delete  ", bootstyle="danger",
                   command=lambda: self._crud(key, "delete")).pack(
            side=LEFT, padx=4)
        ttk.Button(btn_row, text="  Clear  ", bootstyle="secondary-outline",
                   command=lambda: self._clear(key)).pack(
            side=LEFT, padx=4)

        # ---- Data table (LabelFrame) ----
        table_frame = std_ttk.LabelFrame(fr, text="Records", padding=8)
        table_frame.pack(fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(table_frame, columns=columns, show=HEADINGS,
                            yscrollcommand=scroll.set)
        scroll.config(command=tree.yview)

        for j, col in enumerate(columns):
            w = col_widths[j] if col_widths else 140
            tree.heading(col, text=col, anchor=CENTER)
            tree.column(col, width=w, anchor=CENTER)
        tree.pack(fill=BOTH, expand=True)

        tree.bind("<<TreeviewSelect>>", lambda e, k=key: self._on_select(k))

        setattr(self, f"_{key}_widgets", widgets)
        setattr(self, f"_{key}_tree", tree)

    # ------------------------------------------------------------------ #
    #  Refresh (called on frame show)
    # ------------------------------------------------------------------ #
    def _refresh_department(self):
        self._load_tree("department", self.db.get_all_departments())
        self._department_widgets[3].config(values=self.db.get_instructor_ids())

    def _refresh_student(self):
        self._load_tree("student", self.db.get_all_students())
        self._student_widgets[3].config(values=self.db.get_department_ids())

    def _refresh_instructor(self):
        self._load_tree("instructor", self.db.get_all_instructors())
        self._instructor_widgets[5].config(values=self.db.get_department_ids())

    def _refresh_course(self):
        self._load_tree("course", self.db.get_all_courses())
        self._course_widgets[4].config(values=self.db.get_department_ids())

    def _refresh_enrollment(self):
        self._load_tree("enrollment", self.db.get_all_enrollments())
        self._enrollment_widgets[0].config(values=self.db.get_student_rolls())
        self._enrollment_widgets[1].config(values=self.db.get_course_ids())

    def _load_tree(self, key, rows):
        tree = getattr(self, f"_{key}_tree")
        tree.delete(*tree.get_children())
        for r in rows:
            tree.insert("", END, values=r)

    # ------------------------------------------------------------------ #
    #  Select row → populate form
    # ------------------------------------------------------------------ #
    def _on_select(self, key):
        tree = getattr(self, f"_{key}_tree")
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0], "values")
        self._clear(key)
        for w, v in zip(getattr(self, f"_{key}_widgets"), vals):
            if isinstance(w, ttk.Combobox):
                w.set(v if v else "")
            else:
                w.insert(0, v)

    # ------------------------------------------------------------------ #
    #  Clear form
    # ------------------------------------------------------------------ #
    def _clear(self, key):
        for w in getattr(self, f"_{key}_widgets"):
            if isinstance(w, ttk.Combobox):
                w.set("")
            else:
                w.delete(0, "end")

    # ------------------------------------------------------------------ #
    #  CRUD dispatcher
    # ------------------------------------------------------------------ #
    def _vals(self, key):
        return [w.get().strip() for w in getattr(self, f"_{key}_widgets")]

    def _crud(self, key, action):
        v = self._vals(key)
        try:
            if key == "department":
                if action == "add":
                    self.db.add_department(*v)
                elif action == "update":
                    self.db.update_department(*v)
                elif action == "delete":
                    if not v[0]:
                        messagebox.showwarning("Warning", "Enter Dept No.")
                        return
                    if not messagebox.askyesno("Confirm",
                                              f"Delete department {v[0]}?"):
                        return
                    self.db.delete_department(v[0])

            elif key == "student":
                if action == "add":
                    self.db.add_student(*v)
                elif action == "update":
                    self.db.update_student(*v)
                elif action == "delete":
                    if not v[0]:
                        messagebox.showwarning("Warning", "Enter Roll No.")
                        return
                    if not messagebox.askyesno("Confirm",
                                              f"Delete student {v[0]}?"):
                        return
                    self.db.delete_student(v[0])

            elif key == "instructor":
                if action == "add":
                    self.db.add_instructor(*v)
                elif action == "update":
                    self.db.update_instructor(*v)
                elif action == "delete":
                    if not v[0]:
                        messagebox.showwarning("Warning",
                                               "Enter Instructor No.")
                        return
                    if not messagebox.askyesno("Confirm",
                                              f"Delete instructor {v[0]}?"):
                        return
                    self.db.delete_instructor(v[0])

            elif key == "course":
                if action == "add":
                    self.db.add_course(*v)
                elif action == "update":
                    self.db.update_course(*v)
                elif action == "delete":
                    if not v[0]:
                        messagebox.showwarning("Warning", "Enter Course No.")
                        return
                    if not messagebox.askyesno("Confirm",
                                              f"Delete course {v[0]}?"):
                        return
                    self.db.delete_course(v[0])

            elif key == "enrollment":
                if action == "add":
                    self.db.add_enrollment(*v)
                elif action == "update":
                    self.db.update_enrollment(*v)
                elif action == "delete":
                    if not v[0] or not v[1]:
                        messagebox.showwarning("Warning",
                                               "Select Roll No and Course No.")
                        return
                    if not messagebox.askyesno("Confirm",
                                              f"Delete enrollment "
                                              f"({v[0]}, {v[1]})?"):
                        return
                    self.db.delete_enrollment(v[0], v[1])

            getattr(self, f"_refresh_{key}")()
            self._clear(key)
            label = key.title()
            if action == "delete":
                messagebox.showinfo("Success", f"{label} deleted successfully.")
            else:
                messagebox.showinfo("Success",
                                    f"{label} {action}d successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------ #
    #  Cleanup
    # ------------------------------------------------------------------ #
    def on_close(self):
        self.db.close()
        self.root.destroy()
