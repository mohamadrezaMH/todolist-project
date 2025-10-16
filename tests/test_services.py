import pytest
from datetime import datetime, timedelta
from src.todolist.storage.in_memory_storage import ProjectStorage, TaskStorage
from src.todolist.services.project_service import ProjectService
from src.todolist.services.task_service import TaskService
from src.todolist.utils.validators import ValidationError


class TestProjectService:
    def setup_method(self):
        self.project_storage = ProjectStorage()
        self.task_storage = TaskStorage()
        self.project_service = ProjectService(self.project_storage, self.task_storage)

    def test_create_project_success(self):
        """Test successful project creation"""
        project = self.project_service.create_project(
            "Test Project", "Test Description"
        )
        assert project.name == "Test Project"
        assert project.id is not None

    def test_create_project_duplicate_name(self):
        """Test project creation with duplicate name"""
        self.project_service.create_project("Test Project", "Description 1")
        with pytest.raises(ValidationError):
            self.project_service.create_project("Test Project", "Description 2")

    def test_delete_project_cascade(self):
        """Test project deletion with cascade"""
        project = self.project_service.create_project(
            "Test Project", "Test Description"
        )

        # Create task service and add a task
        task_service = TaskService(self.task_storage, self.project_service)
        task = task_service.create_task(project.id, "Test Task", "Task Description")

        # Delete project
        success = self.project_service.delete_project(project.id)
        assert success

        # Verify task is also deleted
        assert task_service.get_task(task.id) is None


class TestTaskService:
    def setup_method(self):
        self.project_storage = ProjectStorage()
        self.task_storage = TaskStorage()
        self.project_service = ProjectService(self.project_storage, self.task_storage)
        self.task_service = TaskService(self.task_storage, self.project_service)

        # Create a project for testing tasks
        self.project = self.project_service.create_project(
            "Test Project", "Test Description"
        )

    def test_create_task_success(self):
        """Test successful task creation"""
        task = self.task_service.create_task(
            self.project.id,
            "Test Task",
            "Test Description",
            datetime.now() + timedelta(days=1),
        )
        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.project_id == self.project.id

    def test_create_task_invalid_project(self):
        """Test task creation with invalid project ID"""
        with pytest.raises(ValidationError):
            self.task_service.create_task(999, "Test Task", "Test Description")

    def test_change_task_status(self):
        """Test task status change"""
        task = self.task_service.create_task(
            self.project.id, "Test Task", "Test Description"
        )
        updated_task = self.task_service.change_task_status(task.id, "doing")
        assert updated_task.status == "doing"
