# 🚀 **ToDoList Project**

A comprehensive ToDoList application built with Python OOP, PostgreSQL/SQLite, FastAPI, and modern software engineering practices across 4 development phases.

## 📊 **Project Phases Overview**

### **Phase 1: OOP & In-Memory Storage**
- ✅ Object-Oriented Design with clean architecture
- ✅ Project and Task management with validation
- ✅ In-memory data storage
- ✅ CLI interface with English/Persian support
- ✅ Comprehensive unit testing (12/12 tests)

### **Phase 2: Database & Repository Pattern**
- ✅ PostgreSQL/SQLite integration with SQLAlchemy ORM
- ✅ Repository Pattern implementation
- ✅ Database migrations with Alembic
- ✅ Scheduled tasks for auto-closing overdue items
- ✅ Dependency injection and layered architecture

### **Phase 3: REST API with FastAPI**
- ✅ Full RESTful API implementation
- ✅ Automatic Swagger/OpenAPI documentation
- ✅ Pydantic models for validation
- ✅ Async endpoint support
- ✅ CLI deprecation with migration path

### **Phase 4: API Testing with Postman**
- ✅ Postman workspace and collection setup
- ✅ Environment variable management
- ✅ Complete endpoint testing suite
- ✅ Automated test runs

## 🏗️ **Project Structure**

```
src/todolist/
├── api/                    # FastAPI application
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic models
│   └── dependencies/      # Dependency injection
├── models/                # SQLAlchemy ORM models
├── repositories/          # Data access layer
├── services/              # Business logic
├── commands/              # CLI commands & scheduled tasks
├── db/                    # Database configuration
├── exceptions/            # Custom exceptions
├── utils/                 # Utilities & config
└── main.py               # Legacy CLI entry point

alembic/                   # Database migrations
tests/                     # Unit tests
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Poetry (dependency management)
- Git
- (Optional) Docker & Docker Compose for PostgreSQL

### **Installation**

```bash
# 1. Clone repository
git clone <https://github.com/mohamadrezaMH/todolist-project>
cd todolist-project

# 2. Install dependencies
poetry install

# 3. Setup environment
cp .env.example .env
# Edit .env with your preferences

# 4. Initialize database
poetry run python -m src.todolist.db.init_db

# 5. Run the application
```

### **Running the Application**

#### **Option A: FastAPI (Recommended)**
```bash
# Start the API server
poetry run uvicorn src.todolist.api.main:app --reload --port 8000

# Access at:
# API: http://localhost:8000/api/v1/
# Docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

#### **Option B: Legacy CLI (Deprecated)**
```bash
# CLI interface (deprecated - use API instead)
poetry run python run_api.py
```

#### **Option C: Scheduled Tasks**
```bash
# Auto-close overdue tasks
poetry run todolist-autoclose

# Run task scheduler
poetry run todolist-scheduler --interval 15
```

## 📡 **API Endpoints**

### **Projects**
- `GET /api/v1/projects/` - List all projects
- `POST /api/v1/projects/` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project
- `GET /api/v1/projects/{id}/stats` - Get project statistics
- `GET /api/v1/projects/{id}/tasks` - Get project tasks

### **Tasks**
- `GET /api/v1/tasks/` - List all tasks (with filters)
- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}/status` - Update task status
- `DELETE /api/v1/tasks/{id}` - Delete task
- `GET /api/v1/tasks/overdue/` - Get overdue tasks

## 🧪 **Testing**

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_models.py

# Test API endpoints
poetry run pytest tests/test_api.py
```

## 🛠️ **Development Commands**

```bash
# Code formatting
poetry run black src/ tests/

# Code linting
poetry run flake8 src/

# Database migrations
poetry run alembic revision --autogenerate -m "description"
poetry run alembic upgrade head

# Package management
poetry add <package>        # Add dependency
poetry remove <package>     # Remove dependency
poetry update              # Update dependencies
```

## 📋 **Postman Setup**

1. **Import Collection**: `ToDoList API v1.postman_collection.json`
2. **Environment Variables**:
   - `base_url`: `http://localhost:8000/api/v1`
   - `base_url_swagger`: `http://localhost:8000`
3. **Test All Endpoints**: Use the collection runner

## 🗄️ **Database Configuration**

### **SQLite (Default)**
```env
DATABASE_URL=sqlite:///todolist.db
```

### **PostgreSQL (Docker)**
```bash
# Start PostgreSQL
docker-compose up -d

# Environment
DATABASE_URL=postgresql://todolist_user:todolist_password@localhost:5432/todolist
```

## 📁 **Key Features**

- ✅ **Layered Architecture**: Clear separation of concerns
- ✅ **Repository Pattern**: Database-agnostic data access
- ✅ **RESTful API**: Full CRUD operations with validation
- ✅ **Automated Testing**: Comprehensive test suite
- ✅ **Database Migrations**: Version-controlled schema changes
- ✅ **Scheduled Tasks**: Automated background processing
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Environment Configuration**: 12-factor app compliant
- ✅ **Type Hints**: Full Python type annotation support

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### **Commit Convention**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation
- `test`: Tests
- `chore`: Maintenance

## 📚 **Learning Outcomes**

This project demonstrates:
- Modern Python OOP principles
- Database design with ORM
- REST API development
- Software architecture patterns
- CI/CD and testing practices
- Professional Git workflow

---

**Built with ❤️ for Software Engineering Course at AUT**

*Azar 1404 - Complete 4-Phase Implementation*
