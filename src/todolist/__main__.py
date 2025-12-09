import sys

def main():
    """Main entry point for the package"""
    print("ToDoList Application")
    print("Available commands:")
    print("  python -m todolist.api.main    # Run FastAPI server")
    print("  python -m todolist.main        # Run CLI (deprecated)")
    sys.exit(1)

if __name__ == "__main__":
    main()