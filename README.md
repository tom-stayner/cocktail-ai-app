# 🍸 Cocktail AI App

A cloud-native cocktail recipe application built with **Python**, **FastAPI**, and **AWS DynamoDB**.

This project forms part of my **Cloud & AI Engineering** learning journey and is designed to put cloud development concepts into practice while building a real-world application.

Current features include:

- REST API built with FastAPI
- HTML web interface
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

```text
            Browser
               │
               ▼
      FastAPI (Uvicorn)
               │
               ▼
      AWS DynamoDB Table
```

---

## 🚧 Project Status

This project is under active development as part of my Cloud & AI Engineering learning journey.

### Current Focus

- REST API development with FastAPI
- AWS DynamoDB integration
- Structured logging
- HTML web interface
- Project modularisation and code refactoring

## Planned Enhancements

### Architecture & Quality

- Service layer architecture
- Environment-based configuration
- Improved exception and error handling
- Automated testing with pytest

### Deployment

- Docker support
- AWS cloud deployment
- CI/CD pipeline

### Media Management

- Store cocktail images in Amazon S3
- Upload images from the web interface
- Display images on cocktail pages
- Generate image thumbnails
- Validate uploaded image types and sizes

### AI Features

- AI-powered cocktail recommendations

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

Create a `.env` file in the project root.

Example:

```text
AWS_REGION=ap-southeast-2
TABLE_NAME=Cocktails
LOG_LEVEL=INFO
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

> `python src/main.py` can be useful for simple testing, however the application is intended to be run using Uvicorn.

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
- AWS credentials configured locally
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
| `LOG_LEVEL` | Application logging level | `INFO` |

---

## Security

- Never commit API keys or passwords.
- Never commit your `.env` file.
- Store secrets in a local `.env` file or a cloud secrets manager.
- `.env.example` documents the required configuration without exposing sensitive information.

---

## Repository Structure

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