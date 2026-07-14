# 🍸 Cocktail AI App

A cocktail recipe application built with **Python**, **FastAPI**, and **AWS DynamoDB**. It currently runs locally and connects to a configured DynamoDB table.

This project forms part of my **Cloud & AI Engineering** learning journey and is designed to put cloud development concepts into practice while building a real-world application.

Current features include:

- REST API built with FastAPI
- HTML web interface
- Service-layer cocktail CRUD logic
- Health endpoint for monitoring
- AWS DynamoDB backend
- Structured application logging
- Interactive Swagger API documentation

---

## Technologies

- Python 3.14
- FastAPI
- AWS DynamoDB
- Boto3
- Uvicorn
- HTML / CSS
- Git & GitHub

---

## Architecture

The current implementation is a FastAPI application with a service layer and a DynamoDB-backed data store.

For a concise architecture overview, see [docs/architecture/overview.md](docs/architecture/overview.md).

---

## 🚧 Project Status

This project is under active development as part of my Cloud & AI Engineering learning journey.

The current focus is strengthening the maintainable backend foundation. See the [roadmap](docs/architecture/roadmap.md) for planned work.

---

# Getting Started

## 1. Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

## 2. Navigate to the Project Root

```text
cocktail-ai-app/
│
├── src/
├── requirements.txt
├── README.md
└── ...
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure the Application

Create a `.env` file in the project root with the AWS Region and DynamoDB table name.

Example:

```text
AWS_REGION=ap-southeast-2
TABLE_NAME=Cocktails
```

Or copy the provided template.

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

## 5. Run the Application

```powershell
uvicorn src.main:app --reload
```

> The application is intended to be run using Uvicorn. For detailed local setup and AWS credential requirements, see [docs/setup.md](docs/setup.md).

## 6. Open Your Browser

Application

```text
http://localhost:8000
```

Swagger Documentation

```text
http://localhost:8000/docs
```

---

## Requirements

- Python 3.14+
- Activated virtual environment
- AWS credentials available through the standard AWS credential provider chain
- Access to the DynamoDB table
- `app = FastAPI()` defined in `src/main.py`

If your project structure differs (for example `app/` instead of `src/`), adjust the Uvicorn command accordingly.

---

## External Dependencies

This application integrates with AWS cloud services.

### DynamoDB

Cocktail data is stored in an AWS DynamoDB table.

Connection information is supplied through environment variables and is **not** stored in this repository.

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_REGION` | AWS region containing the DynamoDB table | `ap-southeast-2` |
| `TABLE_NAME` | DynamoDB table name | `Cocktails` |
| `LOG_LEVEL` | Reserved for future configurable logging; not read by the current application | `INFO` |

---

## Security

- Never commit API keys or passwords.
- Never commit your `.env` file.
- Store secrets in a local `.env` file or a cloud secrets manager.
- `.env.example` documents the required configuration without exposing sensitive information.

---

## Documentation

- [docs/setup.md](docs/setup.md) for detailed local setup
- [docs/project-standards.md](docs/project-standards.md) for the project delivery checklist
- [docs/architecture/overview.md](docs/architecture/overview.md) for the current architecture
- [docs/architecture/aws.md](docs/architecture/aws.md) for AWS-related notes
- [docs/architecture/deployment.md](docs/architecture/deployment.md) for deployment status
- [docs/architecture/data-model.md](docs/architecture/data-model.md) for the current data model
- [docs/architecture/roadmap.md](docs/architecture/roadmap.md) for planned work
- [docs/architecture/engineering-log.md](docs/architecture/engineering-log.md) for implementation notes
- [docs/architecture/chatgpt-integration.md](docs/architecture/chatgpt-integration.md) for the AI-assisted engineering workflow
