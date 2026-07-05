Cocktail AI Application
    How to Run the Application
        Open Visual Studio Code.
        Open the project folder.
        Open a new terminal.

        Activate the virtual environment.
            Windows PowerShell:
                ..venv\Scripts\Activate.ps1

            Windows Command Prompt:
                .venv\Scripts\activate.bat

        Ensure you are in the project root directory.

        Start the application.
            Command Line Application:
            python src/main.py

            FastAPI Web Application:
            uvicorn src.main:app --reload

        Open your browser
            http://localhost:8000

        FastAPI Interactive API Documentation:
            http://localhost:8000/docs

    Notes
        If using FastAPI, ensure app = FastAPI() exists in src/main.py.
        If using a different project structure (for example app/ instead of src/), adjust the Uvicorn command accordingly.
        Ensure the virtual environment is activated before running the application.

    External Dependencies
        This application integrates with external cloud-hosted services.

    Database
        The application uses a cloud-hosted Dynamo database.
        A valid connection string or credentials must be configured before the application can access the database.
        Connection details are supplied through environment variables and are not stored in this repository.
        Example:
        DATABASE_URL=<your database connection string>

    Environment Variables
        The following environment variables may be required:

        Variable	Description
        DATABASE_URL	Database connection string
        OPENAI_API_KEY	OpenAI API key (when AI features are enabled)
        ENVIRONMENT	Current runtime environment (e.g. dev, test, prod)
        
    Security
        API keys, passwords and connection strings must never be committed to Git.
        Sensitive configuration should be stored in a local .env file or a cloud-based secrets manager.
        A .env.example file should be provided to document the required variables without exposing sensitive values.