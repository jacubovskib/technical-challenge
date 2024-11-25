.PHONY: configure unit-test clean help check-env

PYTHON_VERSION_MIN = 3.11
PYTHON_VERSION_CURRENT := $(shell python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

help:
help:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║                     Available Commands                        ║"
	@echo "╠══════════════════════════════════════════════════════════════╣"
	@echo "║ Development:                                                  ║"
	@echo "║   make config        - Install Poetry and dependencies        ║"
	@echo "║   make check-env     - Verify development environment         ║"
	@echo "║   make build         - Build package                         ║"
	@echo "║   make run          - Run the application                    ║"
	@echo "║                                                              ║"
	@echo "║ Testing:                                                     ║"
	@echo "║   make test          - Run all tests                         ║"
	@echo "║   make test-domain   - Run domain tests                      ║"
	@echo "║   make test-infra    - Run infrastructure tests              ║"
	@echo "║   make test-application - Run application tests              ║"
	@echo "║                                                              ║"
	@echo "║ Docker:                                                      ║"
	@echo "║   make docker-build  - Build Docker image                    ║"
	@echo "║   make docker-up     - Start Docker containers               ║"
	@echo "║   make docker-down   - Stop Docker containers                ║"
	@echo "║                                                              ║"
	@echo "║ Utilities:                                                   ║"
	@echo "║   make clean         - Remove cache files and directories    ║"
	@echo "║   make help          - Show this help message                ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"

check-env:
	@echo "Checking development environment..."
	@echo "\nPython:"
	@if command -v python3 &> /dev/null; then \
		python3 --version; \
	else \
		echo "Python 3 not found"; \
	fi

	@echo "\nPoetry:"
	@if command -v poetry &> /dev/null; then \
		poetry --version; \
	else \
		echo "Poetry not found"; \
	fi

	@echo "\nDocker:"
	@if command -v docker &> /dev/null; then \
		docker --version; \
	else \
		echo "Docker not found"; \
	fi

	@echo "\nDocker Compose:"
	@if command -v docker-compose &> /dev/null; then \
		docker-compose --version; \
	else \
		echo "Docker Compose not found"; \
	fi

	@echo "\nMake:"
	@if command -v make &> /dev/null; then \
		make --version | head -n 1; \
	else \
		echo "Make not found"; \
	fi

config:
		@echo "Checking Python version..."
	@if [ $(shell python3 -c 'from packaging import version; print(1 if version.parse("$(PYTHON_VERSION_CURRENT)") >= version.parse("$(PYTHON_VERSION_MIN)") else 0)') -eq 1 ]; then \
		echo "\033[32mPython version $(PYTHON_VERSION_CURRENT) OK\033[0m"; \
	else \
		echo "\033[31mPython version $(PYTHON_VERSION_CURRENT) is not supported. Please install Python $(PYTHON_VERSION_MIN) or higher\033[0m"; \
		exit 1; \
	fi
	@if command -v poetry &> /dev/null; then \
		echo "\033[32mPoetry is already installed\033[0m"; \
	else \
		echo "Installing Poetry..."; \
		curl -sSL https://install.python-poetry.org | python3 -; \
	fi
	@echo "\033[34mActivating Ambient Poetry......\033[0m"
	poetry shell
	@echo "\033[34mInstalling dependencies...\033[0m"
	poetry install


build:
	@echo "Building package..."
	poetry build

run:
	poetry run python main.py

test-application:
	@echo "Running application tests..."
	poetry run python -m unittest discover -s test/application -p "*_test.py" -v

test-domain:
	@echo "Running domain tests..."
	poetry run python -m unittest discover -s test/domain -p "*_test.py" -v

test-infra:
	@echo "Running infrastructure tests..."
	poetry run python -m unittest discover -s test/infra -p "*_test.py" -v

test: test-application test-domain test-infra

clean:
	@echo "Cleaning __pycache__ directories..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean completed!"

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

.DEFAULT_GOAL := help