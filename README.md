````markdown
# CS 396 Project 2 – Test Automation Framework

## Team
- Kaden Hunt  
- Nate Barner

## Overview
This project implements a **test automation framework** that improves code quality through unit, integration, and system testing.  
It integrates with CI/CD pipelines to provide automated execution, reporting, and code coverage analysis.

A small **dummy application** (in `/app`) is included as the target system for demonstration purposes.

## Features
- **Unit tests** for isolated components  
- **Integration tests** for application + database interactions  
- **System tests** for end-to-end workflows  
- **Test case management** using YAML/JSON (`tests/cases/`)  
- **Runner script** (`runner.py`) to launch tests by type or case ID  
- **Reporting** with pass/fail, error details, and coverage percentage  
- **CI/CD** via GitHub Actions for automated runs on every push  

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
