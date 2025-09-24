import argparse
import json
import os
import subprocess
import sys

CASES_DIR = os.path.join("tests", "cases")

def list_cases():
    """List all available test case files."""
    if not os.path.exists(CASES_DIR):
        return []
    return [f for f in os.listdir(CASES_DIR) if f.endswith(".json")]

def load_case(case_id):
    """Load a single case by ID (filename without .json)."""
    case_file = os.path.join(CASES_DIR, f"{case_id}.json")
    if not os.path.exists(case_file):
        raise FileNotFoundError(f"Case file {case_file} not found.")
    with open(case_file, "r") as f:
        return json.load(f)

def run_pytest(test_type=None, case_id=None):
    """Run pytest with filters for test type or case ID."""
    cmd = ["pytest", "tests/", "-q"]

    if test_type:
        # assumes test functions are named test_*_<type>
        cmd += ["-k", test_type]

    if case_id:
        case_data = load_case(case_id)
        print(f"[INFO] Running case {case_id}: {case_data.get('description', '')}")
        

    print(f"[INFO] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr, file=sys.stderr)

    if result.returncode == 0:
        print("[INFO] Tests passed.")
    else:
        print("[ERROR] Tests failed.")

def main():
    parser = argparse.ArgumentParser(description="Test Case Runner")
    parser.add_argument("--list", action="store_true", help="List all available test cases")
    parser.add_argument("--case", type=str, help="Run a specific test case by ID (JSON file name)")
    parser.add_argument("--type", type=str, choices=["unit", "integration", "system"],
                        help="Run all tests of a given type")
    args = parser.parse_args()

    if args.list:
        cases = list_cases()
        print("Available test cases:")
        for c in cases:
            print(" -", c.replace(".json", ""))
        return

    if args.case:
        run_pytest(case_id=args.case)
    elif args.type:
        run_pytest(test_type=args.type)
    else:
        # default: run everything
        run_pytest()

if __name__ == "__main__":
    main()
