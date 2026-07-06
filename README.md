## Project Status

🚧 Currently under active development.

This personal project is part of my Cloud & AI Engineering learning journey to put into practice my Cloud Development learnings.

Upcoming work includes:

- Docker support
- AWS deployment
- CI/CD
- AI-powered cocktail recommendations

# Running the Application

## 1. Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

---

## 2. Ensure You Are in the Project Root Directory

Example:

```text
cocktail-ai-app/
│
├── src/
├── requirements.txt
├── README.md
└── ...
```

---

## 3. Start the Application

### FastAPI Web Application

```powershell
uvicorn src.main:app --reload
```

> **Note:** `python src/main.py` can be useful for simple testing, but the application is intended to be run using Uvicorn.

---

## 4. Open the Application

Application Home Page:

```text
http://localhost:8000
```

Interactive API Documentation (Swagger UI):

```text
http://localhost:8000/docs
```

---

# Notes

- Ensure the virtual environment is activated before running the application.
- Ensure `app = FastAPI()` exists in `src/main.py`.
- If using a different project structure (for example `app/` instead of `src/`), adjust the Uvicorn command accordingly.

---

# External Dependencies

This application integrates with cloud-hosted AWS services.

## Database

The application stores cocktail data in an AWS DynamoDB table.

A valid AWS configuration must be available before the application can access the database.

Configuration is supplied through environment variables and is **not** stored in this repository.

---

# Configuration

Create a `.env` file in the project root.

Example:

```text
AWS_REGION=ap-southeast-2
TABLE_NAME=Cocktails
LOG_LEVEL=INFO
```

Alternatively, copy the provided template.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

---

# Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_REGION` | AWS region containing the DynamoDB table | `ap-southeast-2` |
| `TABLE_NAME` | DynamoDB table name | `Cocktails` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

# Security

- Never commit API keys, passwords or credentials to Git.
- Never commit your `.env` file.
- Store sensitive configuration in a local `.env` file or a cloud-based secrets manager.
- The repository includes a `.env.example` file documenting the required configuration without exposing sensitive values.

---

# Project Structure

```text
cocktail-ai-app/
│
├── src/
│   ├── main.py
│   ├── database.py
│   ├── logging_config.py
│   ├── models.py
│   └── static/
│       └── main.css
│
├── logs/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```