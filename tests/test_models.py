import pytest
from datetime import datetime, timedelta
from src.todolist.models.project import Project
from src.todolist.models.task import Task
from src.todolist.exceptions.service_exceptions import ValidationError


class TestProjectModel:
    def test_project_creation(self):
        """Test basic project creation"""
        project = Project("Test Project", "Test Description")
        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.id is None
    
    def test_project_update(self):
        """Test project update functionality"""
        project = Project("Old Name", "Old Description")
        project.update("New Name", "New Description")
        
        assert project.name == "New Name"
        assert project.description == "New Description"


class TestTaskModel:
    def test_task_creation(self):
        """Test basic task creation"""
        task = Task("Test Task", "Test Description")
        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.project_id is None
    
    def test_task_status_change(self):
        """Test task status change"""
        task = Task("Test Task", "Test Description")
        task.change_status("doing")
        assert task.status == "doing"
    
    def test_task_update(self):
        """Test task update"""
        task = Task("Old Title", "Old Description")
        task.update("New Title", "New Description", "done", datetime.now() + timedelta(days=1))
        
        assert task.title == "New Title"
        assert task.status == "done"