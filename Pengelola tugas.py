import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append({"task": task, "done": False})
        save_tasks(tasks)
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Tugas tidak boleh kosong!")

def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_index = selected_task[0]
        task_text = tasks[task_index]["task"]
        confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus tugas: {task_text}?")
        if confirm:
            del tasks[task_index]
            save_tasks(tasks)
            update_task_list()
    else:
        messagebox.showwarning("Peringatan", "Pilih tugas yang akan dihapus!")

def mark_task_done():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_index = selected_task[0]
        tasks[task_index]["done"] = True
        save_tasks(tasks)
        update_task_list()
    else:
        messagebox.showwarning("Peringatan", "Pilih tugas yang akan ditandai selesai!")

def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_str = task["task"]
        if task["done"]:
            task_str += " (Selesai)"
            task_listbox.insert(tk.END, task_str)
            task_listbox.itemconfig(tk.END, {'fg': 'green'})
        else:
            task_listbox.insert(tk.END, task_str)

def save_tasks_to_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            for task in tasks:
                task_str = task["task"]
                if task["done"]:
                    task_str += " (Selesai)"
                file.write(task_str + "\n")
        messagebox.showinfo("Info", f"Tugas berhasil disimpan ke {file_path}")

window = tk.Tk()
window.title("Pengelola Tugas")
window.resizable(False, False)
window.geometry("400x470") 

tasks = load_tasks()

add_button = tk.Button(window, text="Tambah Tugas", command=add_task)
add_button.pack(pady=5)

delete_button = tk.Button(window, text="Hapus Tugas", command=delete_task)
delete_button.pack(pady=5)

mark_done_button = tk.Button(window, text="Tandai Selesai", command=mark_task_done)
mark_done_button.pack(pady=5)

save_txt_button = tk.Button(window, text="Simpan Tugas", command=save_tasks_to_txt)
save_txt_button.pack(pady=5)

task_entry = tk.Entry(window, width=50)
task_entry.pack(pady=10)

task_listbox = tk.Listbox(window, width=50, height=15)
task_listbox.pack(pady=10)

update_task_list()

window.mainloop()
