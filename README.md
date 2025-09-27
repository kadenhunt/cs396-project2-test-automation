# CS 396 Project 2 – Test Automation Framework

## Team

- **Kaden Hunt**
- **Nate Barner**

## Overview

This project delivers a test automation framework for a distributed disaster response coordination system. It supports unit, integration, and system testing, integrates with CI/CD pipelines for immediate feedback, and generates detailed reports with historical trends to track software quality over time.

### Key Goals of the Framework

- Improve reliability by catching defects early.
- Provide fast, automated test execution (<5 minutes).
- Scale to support additional test cases and workflows.
- Protect test data while keeping historical reports version-controlled.

## Features

- **Unit tests** – Verify isolated functions (`tests/test_disaster_unit.py`).
- **Integration tests** – Validate interactions between components (`tests/test_disaster_integration.py`).
- **System tests** – Simulate end-to-end workflows (`tests/test_disaster_system.py`).
- **Test case management** – JSON case files stored in `tests/cases/`, organized and run through a CLI.
- **Runner (`runner.py`)** – List or run tests by type or ID:
    ```bash
    python runner.py --list        # list all cases  
    python runner.py --type unit   # run all unit tests  
    python runner.py --case TC001  # run a specific case  
    ```
- **Reporting (`make_report.py`)** – Combines test results and coverage into `reports/final_report.json`, appends results to `reports/history.json`, computes deltas, and prints trend summaries to the console.
- **Logging & error handling** – All report generation wrapped with robust logging (`reports/report.log`, generated locally and ignored by git).
- **CI/CD integration** – GitHub Actions workflow runs on each push/PR, executes the full test suite, manages historical results, and uploads artifacts (`results.xml`, `coverage.xml`, `reports/final_report.json`, `reports/history.json`).

## Repository Structure

```
cs396-project2-test-automation/
│── disaster_app.py          # disaster response app functions
│── make_report.py           # combines test results, coverage, history
│── runner.py                # CLI runner for test cases
│── requirements.txt         # dependencies (pytest, pytest-cov)
│── .gitignore               # excludes build artifacts (keeps versioned reports)
│── .github/workflows/ci.yml # CI/CD pipeline config
│── tests/
│   ├── test_disaster_unit.py
│   ├── test_disaster_integration.py
│   ├── test_disaster_system.py
│   └── cases/               # JSON test case definitions
│── reports/
        ├── final_report.json     # latest combined results (committed for reference)
        ├── history.json          # historical trends tracked in git
        └── report.log            # error/info logs (ignored from version control)
```

## Setup

1. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. Run all tests locally with coverage and export the artifacts expected by the report generator:
     ```bash
     PYTHONPATH=. pytest tests/ --junitxml=results.xml --cov=disaster_app --cov-report=xml --cov-report=term
     ```

3. Generate a combined report manually:
     ```bash
     python make_report.py results.xml coverage.xml reports/final_report.json
     ```

## CI/CD Workflow

On each push or pull request to `main`:

1. GitHub Actions sets up Python and installs dependencies.
2. `runner.py` can be used to list or run test cases.
3. `pytest` executes all unit, integration, and system tests with coverage.
4. `make_report.py` produces a final combined report, appends history, and prints a trend summary in the console.
5. Updated `reports/history.json` and `reports/final_report.json` are committed back to `main`, and artifacts remain available for download from the Actions tab.


## Closing Note

A lightweight, extensible framework that automates testing, integrates with CI/CD, and provides historical insight into code quality.

**Go Tops!**
