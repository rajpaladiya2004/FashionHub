# Contributing to FashionHub

Thank you for your interest in contributing to FashionHub! This document provides guidelines and information about our development process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [CI/CD Pipeline](#cicd-pipeline)
- [Coding Standards](#coding-standards)

## Code of Conduct

Please be respectful and constructive in all interactions. We're building an inclusive community where everyone feels welcome to contribute.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/FashionHub.git
   cd FashionHub
   ```

3. **Set up your development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Running the Development Server

```bash
python manage.py runserver
```

### Running Tests

```bash
python manage.py test
```

### Checking Code Quality

Before submitting a PR, ensure your code passes linting:

```bash
# Install linting tools
pip install flake8 pylint

# Run flake8
flake8 . --exclude=venv,migrations,sneat-1.0.0

# Run Django checks
python manage.py check
```

## Pull Request Process

1. **Update your branch** with the latest changes from main:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add: Brief description of what you added"
   git commit -m "Fix: Brief description of what you fixed"
   git commit -m "Update: Brief description of what you updated"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues
   - Ensure all CI checks pass

### What Happens Next?

When you create a PR, our automated workflows will:

1. **Greet you** (if it's your first contribution)
2. **Label the PR** based on size (XS, S, M, L, XL)
3. **Run CI tests** to verify your code
4. **Scan for security issues**
5. **Analyze code quality** with CodeQL

## CI/CD Pipeline

### Automated Workflows

#### CI - Test and Lint (`ci.yml`)
- **Trigger**: Push or PR to `main` or `develop`
- **Actions**:
  - Tests code on Python 3.10 and 3.11
  - Runs flake8 linting
  - Checks Django migrations
  - Runs Django system checks
  - Executes test suite

#### CodeQL Analysis (`codeql.yml`)
- **Trigger**: Push, PR, or weekly schedule
- **Actions**:
  - Scans Python and JavaScript code
  - Identifies security vulnerabilities
  - Checks code quality

#### Security Scan (`security.yml`)
- **Trigger**: Push, PR, schedule, or manual
- **Actions**:
  - Checks dependencies for known vulnerabilities (Safety)
  - Runs Bandit security linter
  - Scans for hardcoded secrets (TruffleHog)

#### Deploy to Render (`deploy.yml`)
- **Trigger**: Push to `main` or manual
- **Actions**:
  - Verifies build integrity
  - Triggers deployment to Render

#### PR Labels (`pr-labels.yml`)
- **Trigger**: PR opened/updated
- **Actions**:
  - Labels PR by size
  - Greets first-time contributors

#### Issue Management (`handle-new-issue.yml`)
- **Trigger**: New issue created
- **Actions**:
  - Greets issue creator
  - Adds triage label

#### Stale Management (`stale.yml`)
- **Trigger**: Daily schedule
- **Actions**:
  - Marks inactive issues/PRs as stale
  - Closes long-stale items

### CI Requirements

For your PR to be merged:
- ✅ All tests must pass
- ✅ Code must pass linting checks
- ✅ No critical security issues
- ✅ Django migrations check must succeed
- ✅ Code review approval required

## Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Maximum line length: 127 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Django Best Practices

- Use Django's built-in features when possible
- Follow the DRY (Don't Repeat Yourself) principle
- Properly handle migrations
- Use Django's ORM instead of raw SQL
- Secure user inputs and prevent SQL injection

### JavaScript Code Style

- Use modern ES6+ syntax
- Keep functions small and focused
- Comment complex logic

### Commit Messages

Follow the conventional commits format:

```
Type: Brief description

Detailed explanation if needed

Types:
- Add: New features
- Fix: Bug fixes
- Update: Changes to existing features
- Remove: Removing features or code
- Docs: Documentation changes
- Style: Formatting changes
- Refactor: Code restructuring
- Test: Adding or updating tests
- Chore: Maintenance tasks
```

## Need Help?

- Check existing issues and PRs
- Create a new issue for bugs or feature requests
- Reach out to maintainers for guidance

Thank you for contributing to FashionHub! 🛍️
