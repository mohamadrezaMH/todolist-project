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
        print("مدیریت پروژه‌ها و وظایف")

        while True:
            self.show_main_menu()
            choice = input("انتخاب شما: ").strip()

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
                print("خروج از برنامه. خداحافظ!")
                break
            else:
                print("⚠️  انتخاب نامعتبر. لطفاً مجدد تلاش کنید.")

    def show_main_menu(self):
        """Display main menu options"""
        print("\n--- منوی اصلی ---")
        print("1. ایجاد پروژه جدید")
        print("2. نمایش تمام پروژه‌ها")
        print("3. ویرایش پروژه")
        print("4. حذف پروژه")
        print("5. ایجاد تسک جدید")
        print("6. نمایش تسک‌های یک پروژه")
        print("7. ویرایش تسک")
        print("8. تغییر وضعیت تسک")
        print("9. حذف تسک")
        print("10. آمار پروژه")
        print("0. خروج")

    def create_project(self):
        """Handle project creation"""
        try:
            print("\n--- ایجاد پروژه جدید ---")
            name = input("نام پروژه: ").strip()
            description = input("توضیحات پروژه: ").strip()

            project = self.project_service.create_project(name, description)
            message = (
                f"✅ پروژه '{project.name}' با موفقیت ایجاد شد. " f"شناسه: {project.id}"
            )
            print(message)

        except ValidationError as e:
            print(f"❌ خطا: {e}")

    def list_projects(self):
        """Display all projects"""
        print("\n--- لیست پروژه‌ها ---")
        projects = self.project_service.get_all_projects()

        if not projects:
            print("📭 هیچ پروژه‌ای یافت نشد.")
            return

        for project in projects:
            project_tasks = self.task_service.get_tasks_by_project(project.id)
            tasks_count = len(project_tasks)
            print(f"{project.id}: {project.name} - {tasks_count} تسک")
            print(f"   توضیحات: {project.description}")
            print("-" * 50)

    def update_project(self):
        """Handle project update"""
        try:
            print("\n--- ویرایش پروژه ---")
            project_id = int(input("شناسه پروژه: "))

            name = input("نام جدید پروژه: ").strip()
            description = input("توضیحات جدید پروژه: ").strip()

            project = self.project_service.update_project(project_id, name, description)
            print(f"✅ پروژه '{project.name}' با موفقیت بروزرسانی شد.")

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")

    def delete_project(self):
        """Handle project deletion"""
        try:
            print("\n--- حذف پروژه ---")
            project_id = int(input("شناسه پروژه برای حذف: "))

            success = self.project_service.delete_project(project_id)
            if success:
                print("✅ پروژه و تسک‌های مرتبط با موفقیت حذف شدند.")
            else:
                print("❌ پروژه یافت نشد.")

        except ValueError as e:
            print(f"❌ خطا: {e}")

    def create_task(self):
        """Handle task creation"""
        try:
            print("\n--- ایجاد تسک جدید ---")
            project_id = int(input("شناسه پروژه: "))
            title = input("عنوان تسک: ").strip()
            description = input("توضیحات تسک: ").strip()

            deadline_str = input("ددلاین (YYYY-MM-DD HH:MM یا خالی): ").strip()
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            task = self.task_service.create_task(
                project_id, title, description, deadline
            )
            print(f"✅ تسک '{task.title}' با موفقیت ایجاد شد. شناسه: {task.id}")

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")

    def list_tasks(self):
        """Display tasks for a project"""
        try:
            print("\n--- لیست تسک‌ها ---")
            project_id = int(input("شناسه پروژه: "))

            tasks = self.task_service.get_tasks_by_project(project_id)

            if not tasks:
                print("📭 هیچ تسکی برای این پروژه یافت نشد.")
                return

            project = self.project_service.get_project(project_id)
            print(f"تسک‌های پروژه '{project.name}':")

            for task in tasks:
                deadline_str = (
                    task.deadline.strftime("%Y-%m-%d %H:%M")
                    if task.deadline
                    else "بدون ددلاین"
                )
                status_icon = (
                    "🔴"
                    if task.status == "todo"
                    else "🟡" if task.status == "doing" else "🟢"
                )
                print(
                    f"{status_icon} {task.id}: {task.title} | "
                    f"وضعیت: {task.status} | ددلاین: {deadline_str}"
                )

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")

    def update_task(self):
        """Handle task update"""
        try:
            print("\n--- ویرایش تسک ---")
            task_id = int(input("شناسه تسک: "))
            title = input("عنوان جدید تسک: ").strip()
            description = input("توضیحات جدید تسک: ").strip()
            status = input("وضعیت جدید (todo/doing/done): ").strip().lower()

            deadline_str = input("ددلاین جدید (YYYY-MM-DD HH:MM یا خالی): ").strip()
            deadline = None
            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            task = self.task_service.update_task(
                task_id, title, description, status, deadline
            )
            print(f"✅ تسک '{task.title}' با موفقیت بروزرسانی شد.")

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")

    def change_task_status(self):
        """Handle task status change"""
        try:
            print("\n--- تغییر وضعیت تسک ---")
            task_id = int(input("شناسه تسک: "))
            status = input("وضعیت جدید (todo/doing/done): ").strip().lower()

            task = self.task_service.change_task_status(task_id, status)
            print(f"✅ وضعیت تسک '{task.title}' به '{status}' تغییر یافت.")

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")

    def delete_task(self):
        """Handle task deletion"""
        try:
            print("\n--- حذف تسک ---")
            task_id = int(input("شناسه تسک برای حذف: "))

            success = self.task_service.delete_task(task_id)
            if success:
                print("✅ تسک با موفقیت حذف شد.")
            else:
                print("❌ تسک یافت نشد.")

        except ValueError as e:
            print(f"❌ خطا: {e}")

    def show_project_stats(self):
        """Display project statistics"""
        try:
            print("\n--- آمار پروژه ---")
            project_id = int(input("شناسه پروژه: "))

            stats = self.project_service.get_project_stats(project_id)
            project = stats["project"]

            print(f"\nآمار پروژه '{project.name}':")
            print(f"تعداد کل تسک‌ها: {stats['total_tasks']}")
            for status, count in stats["status_count"].items():
                status_fa = {
                    "todo": "در انتظار",
                    "doing": "در حال انجام",
                    "done": "انجام شده",
                }
                print(f"  {status_fa[status]}: {count}")

        except (ValidationError, ValueError) as e:
            print(f"❌ خطا: {e}")


def main():
    """Application entry point"""
    cli = ToDoListCLI()
    cli.run()


if __name__ == "__main__":
    main()
