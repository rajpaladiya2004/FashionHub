# GitHub Actions Setup Guide

This guide explains how the GitHub Actions workflows are configured for FashionHub and what you need to know as a contributor or maintainer.

## Overview

FashionHub uses GitHub Actions for:
- Continuous Integration (CI)
- Security scanning
- Code quality analysis
- Automated deployment
- Issue and PR management

## Authentication and Permissions

### Built-in Authentication

Most workflows use the built-in `GITHUB_TOKEN` which is automatically provided by GitHub Actions. This token has the necessary permissions to:
- Read repository contents
- Comment on issues and PRs
- Add labels
- Create check runs

**No additional setup required** for these workflows.

### Workflows Using GITHUB_TOKEN

1. **CI (`ci.yml`)** - Uses default permissions
2. **CodeQL (`codeql.yml`)** - Requires `security-events: write`
3. **Security Scan (`security.yml`)** - Requires `security-events: write`
4. **Handle New Issue (`handle-new-issue.yml`)** - Requires `issues: write`
5. **PR Labels (`pr-labels.yml`)** - Requires `pull-requests: write`
6. **Stale Management (`stale.yml`)** - Requires `issues: write`, `pull-requests: write`

## Workflow Details

### 1. CI - Test and Lint

**File**: `.github/workflows/ci.yml`

**Purpose**: Ensures code quality and functionality

**Runs on**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does**:
1. Sets up Python environment (3.10 and 3.11)
2. Installs dependencies
3. Runs flake8 linting
4. Checks Django migrations
5. Runs Django system checks
6. Executes test suite

**Configuration**:
```yaml
env:
  SECRET_KEY: 'test-secret-key-for-ci'
  DEBUG: 'True'
```

### 2. CodeQL Analysis

**File**: `.github/workflows/codeql.yml`

**Purpose**: Security and code quality analysis

**Runs on**:
- Push to `main` or `develop`
- Pull requests
- Weekly schedule (Mondays at 6 AM UTC)

**Languages analyzed**:
- Python
- JavaScript

**No manual setup required** - GitHub CodeQL is free for public repositories.

### 3. Security Scan

**File**: `.github/workflows/security.yml`

**Purpose**: Vulnerability detection

**Runs on**:
- Push to `main` or `develop`
- Pull requests
- Weekly schedule (Mondays at 9 AM UTC)
- Manual trigger

**Tools used**:
- **Safety**: Checks Python dependencies for known vulnerabilities
- **Bandit**: Python security linter
- **TruffleHog**: Scans for hardcoded secrets

**Artifacts**: Security reports are uploaded and retained for 30 days

### 4. Deploy to Render

**File**: `.github/workflows/deploy.yml`

**Purpose**: Automated deployment

**Runs on**:
- Push to `main` branch
- Manual trigger

**Note**: This workflow triggers Render's auto-deployment feature. Ensure your Render service is configured to auto-deploy from the GitHub repository.

**Render Setup**:
1. Connect your GitHub repository to Render
2. Enable auto-deploy for the `main` branch
3. No additional secrets needed

### 5. PR Labels

**File**: `.github/workflows/pr-labels.yml`

**Purpose**: Automated PR management

**Runs on**:
- PR opened, synchronized, or reopened
- PR review submitted

**Features**:
- Auto-labels PRs by size (XS, S, M, L, XL)
- Greets first-time contributors
- No configuration needed

### 6. Handle New Issue

**File**: `.github/workflows/handle-new-issue.yml`

**Purpose**: Welcome new issue creators

**Runs on**:
- New issue created

**Actions**:
- Posts a welcoming comment
- Adds `triage` label

### 7. Stale Management

**File**: `.github/workflows/stale.yml`

**Purpose**: Cleanup inactive issues and PRs

**Runs on**:
- Daily at 1:30 AM UTC
- Manual trigger

**Configuration**:
- Issues: Stale after 30 days, close after 7 more days
- PRs: Stale after 45 days, close after 7 more days
- Exempt labels: `pinned`, `security`, `enhancement` (for issues)

## Repository Settings

### Required Permissions

Ensure the following permissions are enabled in repository settings:

**Settings > Actions > General > Workflow permissions**:
- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

**Settings > Code security and analysis**:
- ✅ CodeQL analysis (automatically enabled)
- ✅ Dependabot alerts
- ✅ Secret scanning

### Branch Protection (Recommended)

For the `main` branch, enable:
- ✅ Require status checks to pass before merging
  - Required checks: `test`, `Analyze (python)`, `security-scan`
- ✅ Require branches to be up to date before merging
- ✅ Require review from code owners

## Secrets Configuration

### No Secrets Required for Basic Workflows

The following workflows work out of the box:
- CI
- CodeQL
- Issue management
- PR labels
- Stale management

### Optional: Enhanced Deployment

If you want to add deployment notifications or advanced features:

**Settings > Secrets and variables > Actions > New repository secret**:

```
RENDER_API_KEY=your_render_api_key  # Optional for enhanced deployment
SLACK_WEBHOOK=your_slack_webhook    # Optional for notifications
```

## Manual Workflow Triggers

Some workflows can be triggered manually:

1. Go to **Actions** tab
2. Select the workflow (e.g., "Security Scan")
3. Click **Run workflow**
4. Choose the branch
5. Click **Run workflow**

## Monitoring Workflows

### View Workflow Runs

1. Navigate to the **Actions** tab
2. Select a workflow from the left sidebar
3. View run history and status

### Debugging Failed Workflows

1. Click on a failed workflow run
2. Click on the failed job
3. Expand failed steps to see error logs
4. Check the "Annotations" section for specific issues

## Workflow Badges

Add status badges to your README:

```markdown
[![CI - Test and Lint](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/ci.yml/badge.svg)](https://github.com/rajpaladiya2004/FashionHub/actions/workflows/ci.yml)
```

## Cost Considerations

### Free Tier (Public Repository)

All workflows are **free** for public repositories:
- ✅ Unlimited workflow minutes
- ✅ Concurrent jobs
- ✅ CodeQL analysis included
- ✅ Artifact storage (limited)

### Private Repository

If the repository becomes private:
- Limited free minutes per month
- Consider optimizing workflow frequency
- Cache dependencies to save time

## Best Practices

1. **Keep workflows fast**: Use caching for dependencies
2. **Run expensive workflows conditionally**: Use `if` conditions
3. **Monitor workflow usage**: Check Actions tab regularly
4. **Update actions versions**: Keep actions up to date
5. **Test workflows locally**: Use tools like `act` for local testing

## Troubleshooting

### Common Issues

**Issue**: Workflow permissions error
**Solution**: Check repository settings > Actions > Workflow permissions

**Issue**: CodeQL times out
**Solution**: Increase timeout or optimize code analysis scope

**Issue**: Security scan finds vulnerabilities
**Solution**: Update dependencies in `requirements.txt`

**Issue**: Deployment workflow fails
**Solution**: Verify Render configuration and auto-deploy settings

## Getting Help

- Check [GitHub Actions documentation](https://docs.github.com/en/actions)
- Review workflow logs for error details
- Open an issue for FashionHub-specific problems
- Check the Actions tab for workflow status

## Summary

The GitHub Actions setup for FashionHub is designed to be:
- **Zero-configuration**: Works out of the box
- **Comprehensive**: Covers CI, security, and automation
- **Maintainable**: Easy to update and extend
- **Free**: No additional costs for public repos

All workflows use the built-in `GITHUB_TOKEN` and require no manual authentication setup. Simply push your code and the workflows will run automatically! 🚀
