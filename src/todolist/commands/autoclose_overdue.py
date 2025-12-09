"""
Command to auto-close overdue tasks
"""
from datetime import datetime
from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..repositories.task_repository import TaskRepository
from ..services.task_service import TaskService


def auto_close_overdue_tasks(project_id: int = None, dry_run: bool = False):
    """
    Auto-close overdue tasks (deadline passed and not 'done')
    
    Args:
        project_id: Optional project ID to filter tasks
        dry_run: If True, only show what would be closed
    """
    db: Session = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        task_service = TaskService(task_repo)
        
        overdue_tasks = task_service.get_overdue_tasks(project_id)
        
        if not overdue_tasks:
            print(f"{datetime.now()}: No overdue tasks found.")
            return
        
        print(f"{datetime.now()}: Found {len(overdue_tasks)} overdue task(s)")
        
        if dry_run:
            print("Dry run - would close:")
            for task in overdue_tasks:
                print(f"  Task {task.id}: {task.title} (deadline: {task.deadline})")
            return
        
        closed_count = 0
        for task in overdue_tasks:
            try:
                task_service.change_task_status(task.id, "done")
                closed_count += 1
                print(f"  Closed task {task.id}: {task.title}")
            except Exception as e:
                print(f"  Failed to close task {task.id}: {e}")
        
        db.commit()
        print(f"Successfully closed {closed_count} overdue task(s)")
        
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-close overdue tasks")
    parser.add_argument("--project-id", type=int, help="Project ID (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    
    args = parser.parse_args()
    auto_close_overdue_tasks(args.project_id, args.dry_run)