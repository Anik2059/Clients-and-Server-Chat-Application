import socket
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import os

# Sound notification setup using pygame
try:
    import pygame
    pygame.init()
    SOUND_ENABLED = True
    SOUND_FILE = "notify.wav"  # Ensure this file exists in the same directory
except ImportError:
    SOUND_ENABLED = False

class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter your name:").grid(row=0, column=0, padx=10, pady=10)
        self.entry = tk.Entry(master, width=40, font=("Arial", 12))
        self.entry.grid(row=1, column=0, padx=10)
        return self.entry

    def apply(self):
        self.result = self.entry.get()

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")
        self.master.configure(bg="mint cream")

        dialog = CustomDialog(master, title="Username")
        self.username = dialog.result
        if not self.username:
            messagebox.showerror("Error", "Username is required!")
            self.master.destroy()
            return

        self.display_area = scrolledtext.ScrolledText(master, height=15, width=50, bg="azure", font=("Segoe UI Emoji", 11))
        self.display_area.pack(padx=10, pady=(10, 5))
        self.display_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(master, width=40, bg="honeydew", font=("Segoe UI Emoji", 11))
        self.message_entry.pack(padx=10, pady=(0, 5), side=tk.LEFT)

        button_frame = tk.Frame(master, bg="mint cream")
        button_frame.pack(pady=5)

        send_button = tk.Button(button_frame, text="Send 💬", command=self.send_message, bg="light blue", width=12)
        send_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Close ❌", command=self.confirm_close, bg="light coral", width=15)
        close_button.pack(side=tk.LEFT, padx=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("127.0.0.1", 5555))
            self.client_socket.send(self.username.encode('utf-8'))  # send username to server
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))
            self.master.destroy()
            return

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.master.protocol("WM_DELETE_WINDOW", self.confirm_close)

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.update_display("🔔 " + message)
                    if SOUND_ENABLED and os.path.exists(SOUND_FILE):
                        try:
                            pygame.mixer.music.load(SOUND_FILE)
                            pygame.mixer.music.play()
                        except Exception as e:
                            print(f"Sound error: {e}")
                else:
                    self.running = False
                    messagebox.showinfo("Disconnected", "Server has closed the connection.")
                    self.master.quit()
            except:
                break

    def send_message(self):
        if not self.running:
            return

        message = self.message_entry.get()
        if message:
            timestamp = datetime.now().strftime("%H:%M")
            full_msg = f"{self.username} 🗣️: {message} [{timestamp}]"
            try:
                self.client_socket.send(full_msg.encode('utf-8'))
            except:
                messagebox.showerror("Error", "Failed to send message.")
            self.message_entry.delete(0, tk.END)

    def update_display(self, message):
        self.display_area.config(state=tk.NORMAL)
        self.display_area.insert(tk.END, message + "\n")
        self.display_area.config(state=tk.DISABLED)
        self.display_area.see(tk.END)

    def confirm_close(self):
        if messagebox.askyesno("Exit", "Are you sure you want to disconnect?"):
            self.close_connection()

    def close_connection(self):
        if self.running:
            try:
                goodbye_msg = f"{self.username} has left the chat. 👋"
                self.client_socket.send(goodbye_msg.encode('utf-8'))
                self.client_socket.close()
            except:
                pass
            self.running = False
        self.master.destroy()

# Run client
if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
