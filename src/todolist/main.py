from datetime import datetime
from .storage.in_memory_storage import ProjectStorage, TaskStorage
from .services.project_service import ProjectService
from .services.task_service import TaskService
from .utils.validators import ValidationError


class ToDoListCLI:
    """
    Command Line Interface for ToDoList Application
    Handles user interactions and menu management
    """

    def __init__(self):
        self.project_storage = ProjectStorage()
        self.task_storage = TaskStorage()
        self.project_service = ProjectService(self.project_storage, self.task_storage)
        self.task_service = TaskService(self.task_storage, self.project_service)

    def run(self):
        """Main application loop"""
        print("=== ToDoList Application ===")
        print("Project and Task Management System")

        while True:
            self.show_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.update_project()
            elif choice == "4":
                self.delete_project()
            elif choice == "5":
                self.create_task()
            elif choice == "6":
                self.list_tasks()
            elif choice == "7":
                self.update_task()
            elif choice == "8":
                self.change_task_status()
            elif choice == "9":
                self.delete_task()
            elif choice == "10":
                self.show_project_stats()
            elif choice == "0":
                print("Exiting program. Goodbye!")
                break
            else:
                print("⚠️  Invalid choice. Please try again.")

    def show_main_menu(self):
        """Display main menu options"""
        print("\n--- Main Menu ---")
        print("1. Create New Project")
        print("2. List All Projects")
        print("3. Edit Project")
        print("4. Delete Project")
        print("5. Create New Task")
        print("6. List Project Tasks")
        print("7. Edit Task")
        print("8. Change Task Status")
        print("9. Delete Task")
        print("10. Project Statistics")
        print("0. Exit")

    def create_project(self):
        """Handle project creation"""
        try:
            print("\n--- Create New Project ---")
            name = input("Project name: ").strip()
            description = input("Project description: ").strip()

            project = self.project_service.create_project(name, description)
            message = (
                f"✅ Project '{project.name}' created successfully. " 
                f"ID: {project.id}"
            )
            print(message)

        except ValidationError as e:
            print(f"❌ Error: {e}")

    def list_projects(self):
        """Display all projects"""
        print("\n--- Projects List ---")
        projects = self.project_service.get_all_projects()

        if not projects:
            print("📭 No projects found.")
            return

        for project in projects:
            project_tasks = self.task_service.get_tasks_by_project(project.id)
            tasks_count = len(project_tasks)
            print(f"{project.id}: {project.name} - {tasks_count} tasks")
            print(f"   Description: {project.description}")
            print("-" * 50)

    def update_project(self):
        """Handle project update"""
        try:
            print("\n--- Edit Project ---")
            project_id = int(input("Project ID: "))

            name = input("New project name: ").strip()
            description = input("New project description: ").strip()

            project = self.project_service.update_project(project_id, name, description)
            print(f"✅ Project '{project.name}' updated successfully.")

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")

    def delete_project(self):
        """Handle project deletion"""
        try:
            print("\n--- Delete Project ---")
            project_id = int(input("Project ID to delete: "))

            success = self.project_service.delete_project(project_id)
            if success:
                print("✅ Project and related tasks deleted successfully.")
            else:
                print("❌ Project not found.")

        except ValueError as e:
            print(f"❌ Error: {e}")

    def create_task(self):
        """Handle task creation"""
        try:
            print("\n--- Create New Task ---")
            project_id = int(input("Project ID: "))
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()

            deadline_str = input("Deadline (YYYY-MM-DD HH:MM or empty): ").strip()
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            task = self.task_service.create_task(
                project_id, title, description, deadline
            )
            print(f"✅ Task '{task.title}' created successfully. ID: {task.id}")

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")

    def list_tasks(self):
        """Display tasks for a project"""
        try:
            print("\n--- Task List ---")
            project_id = int(input("Project ID: "))

            tasks = self.task_service.get_tasks_by_project(project_id)

            if not tasks:
                print("📭 No tasks found for this project.")
                return

            project = self.project_service.get_project(project_id)
            print(f"Tasks for project '{project.name}':")

            for task in tasks:
                deadline_str = (
                    task.deadline.strftime("%Y-%m-%d %H:%M")
                    if task.deadline
                    else "No deadline"
                )
                status_icon = (
                    "🔴"
                    if task.status == "todo"
                    else "🟡" if task.status == "doing" else "🟢"
                )
                print(
                    f"{status_icon} {task.id}: {task.title} | "
                    f"Status: {task.status} | Deadline: {deadline_str}"
                )

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")

    def update_task(self):
        """Handle task update"""
        try:
            print("\n--- Edit Task ---")
            task_id = int(input("Task ID: "))
            title = input("New task title: ").strip()
            description = input("New task description: ").strip()
            status = input("New status (todo/doing/done): ").strip().lower()

            deadline_str = input("New deadline (YYYY-MM-DD HH:MM or empty): ").strip()
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            task = self.task_service.update_task(
                task_id, title, description, status, deadline
            )
            print(f"✅ Task '{task.title}' updated successfully.")

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")

    def change_task_status(self):
        """Handle task status change"""
        try:
            print("\n--- Change Task Status ---")
            task_id = int(input("Task ID: "))
            status = input("New status (todo/doing/done): ").strip().lower()

            task = self.task_service.change_task_status(task_id, status)
            print(f"✅ Task '{task.title}' status changed to '{status}'.")

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")

    def delete_task(self):
        """Handle task deletion"""
        try:
            print("\n--- Delete Task ---")
            task_id = int(input("Task ID to delete: "))

            success = self.task_service.delete_task(task_id)
            if success:
                print("✅ Task deleted successfully.")
            else:
                print("❌ Task not found.")

        except ValueError as e:
            print(f"❌ Error: {e}")

    def show_project_stats(self):
        """Display project statistics"""
        try:
            print("\n--- Project Statistics ---")
            project_id = int(input("Project ID: "))

            stats = self.project_service.get_project_stats(project_id)
            project = stats["project"]

            print(f"\nStatistics for project '{project.name}':")
            print(f"Total tasks: {stats['total_tasks']}")
            for status, count in stats["status_count"].items():
                status_text = {
                    "todo": "To Do",
                    "doing": "In Progress", 
                    "done": "Completed",
                }
                print(f"  {status_text[status]}: {count}")

        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")


def main():
    """Application entry point"""
    cli = ToDoListCLI()
    cli.run()


if __name__ == "__main__":
    main()