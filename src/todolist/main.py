from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.orm import Session

from .db.session import SessionLocal
from .repositories.project_repository import ProjectRepository
from .repositories.task_repository import TaskRepository
from .services.project_service import ProjectService
from .services.task_service import TaskService
from .exceptions.service_exceptions import ValidationError
from typing import Iterator


@contextmanager
def get_db() -> Iterator[Session]:
    """Context manager for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ToDoListCLI:
    """Command Line Interface for ToDoList Application"""
    
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.task_repo = TaskRepository(db)
        self.project_service = ProjectService(self.project_repo, self.task_repo)
        self.task_service = TaskService(self.task_repo)
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("⚠️  WARNING: CLI interface is deprecated and will be removed in the next release.")
        print("⚠️  Please use the FastAPI HTTP interface instead.")
        print("=" * 60)
        print("\n=== ToDoList Application (Phase 2 - RDB) ===")
 
        print("Project and Task Management System with SQLite Database")
        
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
            elif choice == "11":
                self.show_overdue_tasks()
            elif choice == "12":
                self.auto_close_overdue_tasks()
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
        print("11. Show Overdue Tasks")
        print("12. Auto-Close Overdue Tasks")
        print("0. Exit")
    
    def create_project(self):
        """Handle project creation"""
        try:
            print("\n--- Create New Project ---")
            name = input("Project name: ").strip()
            description = input("Project description: ").strip()
            
            project = self.project_service.create_project(name, description)
            print(f"✅ Project '{project.name}' created successfully. ID: {project.id}")
        
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
            tasks_count = self.task_repo.count_by_project(project.id)
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
            
            # Check if project exists
            if not self.project_service.project_exists(project_id):
                print("❌ Project not found.")
                return
            
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()
            
            deadline_str = input("Deadline (YYYY-MM-DD HH:MM or empty): ").strip()
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            
            task = self.task_service.create_task(project_id, title, description, deadline)
            print(f"✅ Task '{task.title}' created successfully. ID: {task.id}")
        
        except (ValidationError, ValueError) as e:
            print(f"❌ Error: {e}")
    
    def list_tasks(self):
        """Display tasks for a project"""
        try:
            print("\n--- Task List ---")
            project_id = int(input("Project ID: "))
            
            if not self.project_service.project_exists(project_id):
                print("❌ Project not found.")
                return
            
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
            
            task = self.task_service.update_task(task_id, title, description, status, deadline)
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
    
    def show_overdue_tasks(self):
        """Display overdue tasks"""
        try:
            print("\n--- Overdue Tasks ---")
            project_id_str = input("Project ID (or empty for all projects): ").strip()
            project_id = int(project_id_str) if project_id_str else None
            
            overdue_tasks = self.task_service.get_overdue_tasks(project_id)
            
            if not overdue_tasks:
                print("✅ No overdue tasks found.")
                return
            
            print(f"Found {len(overdue_tasks)} overdue task(s):")
            for task in overdue_tasks:
                deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "N/A"
                print(f"  Task {task.id}: {task.title} | Deadline: {deadline_str} | Status: {task.status}")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def auto_close_overdue_tasks(self):
        """Auto-close overdue tasks"""
        try:
            print("\n--- Auto-Close Overdue Tasks ---")
            project_id_str = input("Project ID (or empty for all projects): ").strip()
            project_id = int(project_id_str) if project_id_str else None
            
            confirm = input("Close all overdue tasks? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Operation cancelled.")
                return
            
            overdue_tasks = self.task_service.get_overdue_tasks(project_id)
            
            if not overdue_tasks:
                print("✅ No overdue tasks found.")
                return
            
            closed_count = 0
            for task in overdue_tasks:
                try:
                    self.task_service.change_task_status(task.id, "done")
                    closed_count += 1
                    print(f"  ✅ Closed task {task.id}: {task.title}")
                except Exception as e:
                    print(f"  ❌ Failed to close task {task.id}: {e}")
            
            print(f"\n✅ Successfully closed {closed_count} overdue task(s)")
        
        except ValueError as e:
            print(f"❌ Error: {e}")


def main():
    """Application entry point"""
    with get_db() as db:
        cli = ToDoListCLI(db)
        cli.run()


if __name__ == "__main__":
    main()