# ToDoList Project - Phase 1

A modern Python-based ToDoList application built with Object-Oriented Programming principles and clean architecture.

## 🚀 Features

### Project Management
- ✅ Create new projects with unique names
- ✅ Read and list all projects
- ✅ Update project names and descriptions
- ✅ Delete projects with cascade task deletion
- ✅ Configurable project limits via environment variables

### Task Management  
- ✅ Create tasks with titles, descriptions, and deadlines
- ✅ Update task information and status
- ✅ Change task status (todo → doing → done)
- ✅ Delete individual tasks
- ✅ Task validation and constraints

### Technical Features
- 🏗️ Clean layered architecture (Models → Services → Storage → CLI)
- 📝 Comprehensive input validation
- 🧪 Full test coverage (12 unit tests)
- ⚙️ Environment-based configuration
- 🎯 Type hints throughout the codebase
- 🔧 Poetry for dependency management

## 📋 Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <https://github.com/mohamadrezaMH/todolist-project>
   cd todolist-project
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred limits
   ```

4. **Run the application**
   ```bash
   poetry run python -m src.todolist.main
   ```

## 🎮 Usage Examples

### Creating a Project
```
--- Main Menu ---
1. Create New Project
> 1
Project name: Work Tasks
Project description: Tasks related to work projects
✅ Project 'Work Tasks' created successfully. ID: 1
```

### Adding a Task
```
5. Create New Task
> 5
Project ID: 1
Task title: Complete Phase 1
Task description: Finish the first phase of ToDoList project
Deadline (YYYY-MM-DD HH:MM or empty): 2024-12-31 18:00
✅ Task 'Complete Phase 1' created successfully. ID: 1
```

### Changing Task Status
```
8. Change Task Status
> 8
Task ID: 1
New status (todo/doing/done): doing
✅ Task 'Complete Phase 1' status changed to 'doing'.
```

## 🏗️ Project Architecture

```
src/todolist/
├── models/           # Data models (Project, Task)
├── services/         # Business logic layer
├── storage/          # Data storage (In-memory)
├── utils/            # Utilities & configuration
└── main.py           # CLI interface
```

## 🧪 Testing

Run the test suite:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=src
```

## 🔧 Development

### Code Formatting
```bash
poetry run black src/ tests/
```

### Code Quality
```bash
poetry run flake8 src/
```

### Running Tests
```bash
poetry run pytest
```

## ⚙️ Configuration

Environment variables in `.env`:
```env
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS=100
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Python and Clean Architecture**
