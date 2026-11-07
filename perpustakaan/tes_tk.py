import tkinter as tk

r = tk.Tk()
print("Versi Tk:", r.tk.call("info", "patchlevel"))
tk.Label(r, text="Halo dari Tk", font=("Helvetica", 24)).pack(padx=60, pady=40)
r.mainloop()