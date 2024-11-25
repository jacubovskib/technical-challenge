# Technical Backend Challenge

## Overview
Backend application developed for the technical challenge, implementing a simplified users api.

## Project Structure
This structure follows clean architecture principles with clear separation of concerns between layers.
<pre>
project/
├── api-schema/             # API Schema definitions
├── src/
│   ├── application/        # Use cases
│   │                       # Core business logic, independent of external frameworks
│   │
│   ├── domain/            # Business rules and entities
│   │                      # Core business logic, independent of external frameworks
│   │
│   ├── infra/             # External interfaces and frameworks
│   │                      # Database, HTTP clients, external services
│   │
│   └── main.py            # Application bootstrap and configuration
│
├── test/                  # Mirrors the src structure for tests
│   ├── application/       # Tests for use cases and application services
│   ├── domain/            # Tests for business rules and entities
│   └── infra/             # Tests for external interfaces
</pre>


## Technologies
- Python 3.11+
- Poetry (Dependency Management)
- SQLite3
- Docker & Docker Compose

## Requirements
- Python 3.11 or higher
- Poetry
- Docker (optional)
- Make

## Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/technical-challenge.git
cd technical-challenge
```
2. Verify the environment:
```bash
make check-env
```
2. Configure the environment:
```bash
make configure
```

3. Copy .env.example to .env:
```bash
cp .env.example .env

```

## Development
### Available Commands
```bash
"╔═══════════════════════════════════════════════════════════════╗"
"║                     Available Commands                        ║"
"╠═══════════════════════════════════════════════════════════════╣"
"║ Development:                                                  ║"
"║   make config        - Install Poetry and dependencies        ║"
"║   make check-env     - Verify development environment         ║"
"║                                                               ║"
"║ Testing:                                                      ║"
"║   make test          - Run all tests                          ║"
"║   make test-domain   - Run domain tests                       ║"
"║   make test-infra    - Run infrastructure tests               ║"
"║   make test-app      - Run application tests                  ║"
"║                                                               ║"
"║ Docker:                                                       ║"
"║   make docker-build  - Build Docker image                     ║"
"║   make docker-up     - Start Docker containers                ║"
"║   make docker-down   - Stop Docker containers                 ║"
"║                                                               ║"
"║ Utilities:                                                    ║"
"║   make clean         - Remove cache files and directories     ║"
"║   make help          - Show this help message                 ║"
"╚═══════════════════════════════════════════════════════════════╝"
```

### Running Locally
```bash
make build
or
poetry run python -m src.main

```
### Running with Docker
```bash
make docker-build
make docker-up

```
### Running Tests
```bash
make test                # Run all tests
make test-domain        # Run domain tests
make test-infra         # Run infrastructure tests
make test-application   # Run application tests
```


### Environment Variables
```bash
# Application Settings
APP_NAME=
APP_ENV=
APP_DEBUG=
APP_PORT=
APP_HOST=
# Database Settings
DATABASE_URL=
# API Settings
API_VERSION=
API_PREFIX=
# Security Settings
SECRET_KEY=
JWT_EXPIRATION_MINUTES=
```
