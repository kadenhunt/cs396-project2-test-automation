# CS 396 Project 2 – Test Automation Framework

## Team
- Kaden Hunt  
- Nate Barner

Overview

This project delivers a test automation framework designed to improve code quality in a distributed disaster response coordination system.
It supports unit, integration, and system testing to catch defects early, while integrating with CI/CD pipelines for automated execution and immediate feedback.

The framework emphasizes scalability, speed, and security, ensuring reliable test runs in under five minutes, with robust error handling and secure configuration management.
A small dummy application (in /app) is included as the demonstration target system.

Features

- Unit tests for isolated components

- Integration tests for application + database interactions

- System tests for end-to-end workflows

- Test case management using structured YAML/JSON files (tests/cases/) with easy creation, modification, and organization

- Runner script (runner.py) to launch tests by type or case ID via a simple CLI

- Reporting with pass/fail summaries, error logs, coverage metrics, and historical tracking

- Error handling & logging to capture failures and exceptions with actionable detail

- CI/CD integration via GitHub Actions for automated runs on every push or pull request

- Fast execution optimized to complete test suites within minutes for rapid feedback

- Scalability to support growth in both number and complexity of test cases without performance loss

- Security practices to protect test data and configuration details

- Usability through clear folder structure, documentation, and onboarding guidance for new developers

## Requirements
- Python 
- Install dependencies:

```bash
pip install -r requirements.txt
````

## Repository Structure

```
app/            # Dummy application
tests/          # Test files + case descriptions
runner.py       # CLI runner for test cases
requirements.txt
.github/        # CI/CD pipeline config
docs/           # Technical & organizational documentation
```

## Demo

A demo video, presentation slides, and documentation will be added before submission.
