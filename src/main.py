# main.py
from .database import initialize_database
from .gui import create_gui

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Create and serve the GUI
    gui = create_gui()
    pn.serve(gui, port=5006, show=True)
