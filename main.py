from tkinter import Tk
from controller import AppController

if __name__ == "__main__":
    ui = Tk()
    app = AppController(ui)
    ui.mainloop() # wartet auf Benutzer interaktionen
