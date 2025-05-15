import socket
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Server")
        self.master.configure(bg="floral white")

        self.clients = {}  # username: client_socket

        self.display_area = tk.Text(master, height=10, width=60, bg="thistle", font=("Arial", 12))
        self.display_area.pack(padx=10, pady=(10, 5))
        self.display_area.config(state=tk.DISABLED)

        self.chat_history = scrolledtext.ScrolledText(master, height=10, width=40, bg="misty rose")
        self.chat_history.pack(padx=10, pady=(0, 5), side=tk.LEFT)

        right_frame = tk.Frame(master, bg="floral white")
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.message_entry = tk.Entry(master, width=40, bg="lemon chiffon")
        self.message_entry.pack(pady=(0, 5))

        tk.Button(right_frame, text="Send to All", command=self.send_message_all, bg="light cyan", width=20).pack(pady=5)
        tk.Button(right_frame, text="Send to User", command=self.send_message_user, bg="light cyan", width=20).pack(pady=5)
        tk.Button(right_frame, text="Close Server", command=self.close_server, bg="light cyan", width=20).pack(pady=5)
        tk.Button(right_frame, text="Delete History", command=self.delete_history, bg="light cyan", width=20).pack(pady=5)

        self.start_server()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 5555))
        self.server.listen(5)
        self.update_display("Server started. Waiting for clients...\n")
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            client_socket, address = self.server.accept()
            try:
                username = client_socket.recv(1024).decode('utf-8')
                if not username:
                    client_socket.close()
                    continue

                self.clients[username] = client_socket
                self.update_display(f"{username} connected from {address}.\n")
                self.broadcast_message(f"*** {username} has joined the chat ***", None)

                client_socket.send("Welcome to the chat!".encode('utf-8'))
                threading.Thread(target=self.handle_client, args=(client_socket, username), daemon=True).start()
            except Exception as e:
                print(f"Error accepting client: {e}")

    def handle_client(self, client, username):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message:
                    self.update_display(message + "\n")
                    self.chat_history.insert(tk.END, message + "\n")
                    self.broadcast_message(message, client)
                else:
                    self.remove_client(username)
                    break
            except:
                self.remove_client(username)
                break

    def remove_client(self, username):
        client = self.clients.pop(username, None)
        if client:
            client.close()
            self.broadcast_message(f"*** {username} has left the chat ***", None)
            self.update_display(f"{username} disconnected.\n")

    def broadcast_message(self, message, sender_socket):
        for user, client in list(self.clients.items()):
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(user)

    def send_message_all(self):
        message = self.message_entry.get()
        if message:
            timestamp = datetime.now().strftime("%H:%M")
            full_msg = f"Server: {message} [{timestamp}]"
            self.update_display(full_msg + "\n")
            self.broadcast_message(full_msg, None)
            self.message_entry.delete(0, tk.END)

    def send_message_user(self):
        target_username = simpledialog.askstring("Send to User", "Enter the recipient's username:", parent=self.master)
        if target_username and target_username in self.clients:
            message = self.message_entry.get()
            if message:
                timestamp = datetime.now().strftime("%H:%M")
                full_msg = f"(Private) Server to {target_username}: {message} [{timestamp}]"
                try:
                    self.clients[target_username].send(full_msg.encode('utf-8'))
                    self.update_display(full_msg + "\n")
                    self.message_entry.delete(0, tk.END)
                except:
                    self.remove_client(target_username)
        else:
            messagebox.showerror("Error", "User not found or not connected.")

    def update_display(self, message):
        self.display_area.config(state=tk.NORMAL)
        self.display_area.insert(tk.END, message)
        self.display_area.config(state=tk.DISABLED)

    def close_server(self):
        for username, client in self.clients.items():
            try:
                client.send("Server is ending the chat. Goodbye!".encode('utf-8'))
                client.close()
            except:
                pass
        self.server.close()
        self.master.destroy()

    def delete_history(self):
        self.chat_history.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
