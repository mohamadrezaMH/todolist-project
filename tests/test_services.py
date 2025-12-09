import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.todolist.db.session import SessionLocal
from src.todolist.repositories.project_repository import ProjectRepository
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.services.project_service import ProjectService
from src.todolist.services.task_service import TaskService
from src.todolist.exceptions.service_exceptions import ValidationError
from src.todolist.db.init_db import init_database


# Fixture for database session
@pytest.fixture(scope="module")
def db_session():
    """Create a test database session"""
    init_database()  # Ensure tables exist
    db = SessionLocal()
    yield db
    db.close()


# Fixture for repositories
@pytest.fixture
def project_repo(db_session):
    return ProjectRepository(db_session)


@pytest.fixture
def task_repo(db_session):
    return TaskRepository(db_session)


# Fixture for services
@pytest.fixture
def project_service(project_repo, task_repo):
    return ProjectService(project_repo, task_repo)


@pytest.fixture
def task_service(task_repo):
    return TaskService(task_repo)


class TestProjectService:
    def test_create_project_success(self, project_service):
        """Test successful project creation"""
        project = project_service.create_project("Test Project", "Test Description")
        assert project.name == "Test Project"
        assert project.id is not None
    
    def test_create_project_duplicate_name(self, project_service):
        """Test project creation with duplicate name"""
        project_service.create_project("Test Project", "Description 1")
        with pytest.raises(ValidationError):
            project_service.create_project("Test Project", "Description 2")
    
    def test_delete_project(self, project_service, task_service, project_repo):
        """Test project deletion"""
        project = project_service.create_project("Test Project", "Test Description")
        
        # Create a task
        task_service.create_task(project.id, "Test Task", "Task Description")
        
        # Delete project
        success = project_service.delete_project(project.id)
        assert success
        
        # Verify project is deleted
        assert project_service.get_project(project.id) is None


class TestTaskService:
    @pytest.fixture(autouse=True)
    def setup(self, project_service, task_service):
        """Setup for task tests"""
        self.project = project_service.create_project("Test Project", "Test Description")
        self.project_service = project_service
        self.task_service = task_service
    
    def test_create_task_success(self):
        """Test successful task creation"""
        task = self.task_service.create_task(
            self.project.id, 
            "Test Task", 
            "Test Description",
            datetime.now() + timedelta(days=1)
        )
        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.project_id == self.project.id
    
    def test_change_task_status(self):
        """Test task status change"""
        task = self.task_service.create_task(self.project.id, "Test Task", "Test Description")
        updated_task = self.task_service.change_task_status(task.id, "doing")
        assert updated_task.status == "doing"
    
    def test_get_overdue_tasks(self):
        """Test getting overdue tasks"""
        # Create an overdue task
        task = self.task_service.create_task(
            self.project.id,
            "Overdue Task",
            "Description",
            datetime.now() - timedelta(days=1)  # Past deadline
        )
        
        overdue_tasks = self.task_service.get_overdue_tasks(self.project.id)
        assert len(overdue_tasks) >= 1
        assert overdue_tasks[0].id == task.id