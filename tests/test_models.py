import pytest
from datetime import datetime, timedelta
from src.todolist.models.project import Project
from src.todolist.models.task import Task


class TestProjectModel:
    def test_project_creation(self):
        """Test basic project creation (SQLAlchemy model)"""
        project = Project(name="Test Project", description="Test Description")
        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.created_at is not None
    
    def test_project_update(self):
        """Test project update functionality"""
        project = Project(name="Old Name", description="Old Description")
        project.update("New Name", "New Description")
        
        assert project.name == "New Name"
        assert project.description == "New Description"
        assert project.updated_at is not None


class TestTaskModel:
    def test_task_creation(self):
        """Test basic task creation"""
        task = Task(title="Test Task", description="Test Description")
        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.created_at is not None
    
    def test_task_status_change(self):
        """Test task status change"""
        task = Task(title="Test Task", description="Test Description")
        task.change_status("doing")
        assert task.status == "doing"
        assert task.updated_at is not None
    
    def test_task_update(self):
        """Test task update"""
        task = Task(title="Old Title", description="Old Description")
        new_deadline = datetime.now() + timedelta(days=1)
        task.update("New Title", "New Description", "done", new_deadline)
        
        assert task.title == "New Title"
        assert task.status == "done"
        assert task.deadline == new_deadline