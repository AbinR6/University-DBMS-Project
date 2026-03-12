"""
main.py — Entry point for the University Academic Management System.
"""

import ttkbootstrap as ttk
from gui import UniversityApp


def main():
    root = ttk.Window(themename="flatly")
    app = UniversityApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
