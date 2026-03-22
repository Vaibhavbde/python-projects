# ============================================================
# Level 2 - Task 1: To-Do List Application
# Codveda Python Development Internship
# ============================================================

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# ── Persistence helpers ──────────────────────────────────────

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file is absent."""
    if not os.path.isfile(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[Warning] Could not read tasks file. Starting with an empty list.")
        return []

def save_tasks(tasks):
    """Persist tasks to the JSON file."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except IOError as e:
        print(f"[Error] Could not save tasks: {e}")

# ── Core operations ──────────────────────────────────────────

def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("[Error] Task title cannot be empty.")
        return
    task = {
        "id":        len(tasks) + 1,
        "title":     title,
        "done":      False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task #{task['id']} added: '{title}'")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    print("\n" + "=" * 55)
    print(f"  {'#':<4} {'Status':<10} {'Title':<30} {'Created'}")
    print("-" * 55)
    for t in tasks:
        status = "✔ Done" if t["done"] else "○ Pending"
        print(f"  {t['id']:<4} {status:<10} {t['title']:<30} {t['created_at']}")
    print("=" * 55)

def complete_task(tasks):
    list_tasks(tasks)
    try:
        task_id = int(input("Enter task # to mark as done: "))
    except ValueError:
        print("[Error] Please enter a valid number.")
        return
    for t in tasks:
        if t["id"] == task_id:
            if t["done"]:
                print(f"Task #{task_id} is already marked as done.")
            else:
                t["done"] = True
                save_tasks(tasks)
                print(f"✔ Task #{task_id} marked as complete.")
            return
    print(f"[Error] No task found with id #{task_id}.")

def delete_task(tasks):
    list_tasks(tasks)
    try:
        task_id = int(input("Enter task # to delete: "))
    except ValueError:
        print("[Error] Please enter a valid number.")
        return
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            print(f"🗑  Task #{task_id} ('{removed['title']}') deleted.")
            return
    print(f"[Error] No task found with id #{task_id}.")

# ── Main loop ────────────────────────────────────────────────

def main():
    tasks = load_tasks()
    menu = {
        "1": ("Add task",           add_task),
        "2": ("List tasks",         lambda t: list_tasks(t)),
        "3": ("Mark task as done",  complete_task),
        "4": ("Delete task",        delete_task),
        "5": ("Exit",               None),
    }

    print("=" * 40)
    print("     To-Do List Application")
    print("=" * 40)

    while True:
        print("\nMenu:")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        choice = input("\nYour choice: ").strip()

        if choice == "5":
            print("Goodbye! Stay productive 🚀")
            break
        elif choice in menu:
            _, action = menu[choice]
            action(tasks)
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
