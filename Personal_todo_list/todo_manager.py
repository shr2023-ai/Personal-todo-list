import json
import datetime

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(tasks):
    description = input("Enter the task description: ")
    due_date = input("Enter the due date (YYYY-MM-DD, optional): ")
    if due_date:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
    else:
        due_date = None

    task = {
        "description": description,
        "due_date": str(due_date) if due_date else None,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added!")

# View tasks with filters
def view_tasks(tasks, filter_type=None):
    for idx, task in enumerate(tasks):
        if filter_type == "completed" and not task["completed"]:
            continue
        elif filter_type == "pending" and task["completed"]:
            continue
        elif filter_type == "due_soon":
            due_date = task.get("due_date")
            if due_date:
                days_remaining = (datetime.datetime.strptime(due_date, "%Y-%m-%d").date() - datetime.date.today()).days
                if days_remaining > 3:
                    continue
        status = "Completed" if task["completed"] else "Pending"
        due = task["due_date"] if task["due_date"] else "No due date"
        print(f"{idx + 1}. {task['description']} | Due: {due} | Status: {status}")

# Mark a task as complete
def mark_task_complete(tasks):
    task_id = int(input("Enter the task number to mark as completed: ")) - 1
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task number!")

# Edit a task
def edit_task(tasks):
    task_id = int(input("Enter the task number to edit: ")) - 1
    if 0 <= task_id < len(tasks):
        new_desc = input(f"Enter new description (current: {tasks[task_id]['description']}): ")
        new_due = input(f"Enter new due date (YYYY-MM-DD, current: {tasks[task_id]['due_date']}): ")
        if new_due:
            new_due = datetime.datetime.strptime(new_due, "%Y-%m-%d").date()
        tasks[task_id]["description"] = new_desc if new_desc else tasks[task_id]["description"]
        tasks[task_id]["due_date"] = str(new_due) if new_due else tasks[task_id]["due_date"]
        save_tasks(tasks)
        print("Task updated!")
    else:
        print("Invalid task number!")

# Delete a task
def delete_task(tasks):
    task_id = int(input("Enter the task number to delete: ")) - 1
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
        print("Task deleted!")
    else:
        print("Invalid task number!")

# Main menu
def main_menu():
    tasks = load_tasks()
    
    while True:
        print("\nTo-Do List Manager")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. View completed tasks")
        print("4. View pending tasks")
        print("5. View tasks due soon")
        print("6. Mark task as completed")
        print("7. Edit a task")
        print("8. Delete a task")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, "completed")
        elif choice == "4":
            view_tasks(tasks, "pending")
        elif choice == "5":
            view_tasks(tasks, "due_soon")
        elif choice == "6":
            mark_task_complete(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            delete_task(tasks)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()