from src.application.application_manager import ApplicationManager

def main():
    app_manager = ApplicationManager()
    app_manager.initialize()
    app_manager.run()


if __name__ == "__main__":
    main()