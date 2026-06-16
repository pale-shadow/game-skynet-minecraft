import tkinter as tk
from mcstatus import JavaServer
import threading
import time

SERVER = "10.10.8.60:25565"
REFRESH = 30 

def update_status():
    try:
        server = JavaServer.lookup(SERVER)
        status = server.status()
        txt = (f"Server: {SERVER}\n"
               f"Version: {status.version.name}\n"
               f"Players: {status.players.online}/{status.players.max}\n"
               f"Latency: {status.latency} ms")
    except Exception as e:
        txt = f"Server offline\n{e}"
    label.config(text=txt)
    root.after(REFRESH*1000, lambda: threading.Thread(target=update_status).start())

root = tk.Tk()
root.title("Minecraft Server Status")
root.geometry("300x150")
label = tk.Label(root, font=("Helvetica", 12), justify="left")
label.pack(expand=True, fill="both", padx=10, pady=10)

threading.Thread(target=update_status).start()
root.mainloop()
