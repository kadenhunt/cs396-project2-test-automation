import sys
import xml.etree.ElementTree as ET
import json
import os
import logging
from datetime import datetime


os.makedirs("reports", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="reports/report.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def parse_junit(junit_file):
    """Parse JUnit XML (pytest results) and return summary + failure details."""
    try:
        tree = ET.parse(junit_file)
        root = tree.getroot()
        suite = root.find("testsuite") if root.tag == "testsuites" else root

        total = int(suite.attrib.get("tests", 0))
        failures = int(suite.attrib.get("failures", 0))
        errors = int(suite.attrib.get("errors", 0))
        skipped = int(suite.attrib.get("skipped", 0))
        passed = total - failures - errors - skipped

        failure_details = []
        for testcase in suite.iter("testcase"):
            for failure in testcase.iter("failure"):
                failure_details.append({
                    "test": testcase.attrib.get("name"),
                    "classname": testcase.attrib.get("classname"),
                    "error": failure.attrib.get("message", "").strip(),
                    "details": failure.text.strip() if failure.text else ""
                })

        return {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failures,
                "errors": errors,
                "skipped": skipped
            },
            "failures": failure_details
        }
    except Exception as e:
        logging.error(f"Failed to parse JUnit file {junit_file}: {e}")
        return {"summary": {}, "failures": []}


def parse_coverage(cov_file):
    """Parse coverage XML and return overall + per-function stats."""
    try:
        tree = ET.parse(cov_file)
        root = tree.getroot()

        overall = float(root.attrib.get("line-rate", 0)) * 100
        coverage_details = []

        for package in root.iter("package"):
            for cls in package.iter("class"):
                name = cls.attrib.get("name")
                filename = cls.attrib.get("filename")
                line_rate = float(cls.attrib.get("line-rate", 0)) * 100

                statements = 0
                missing = 0
                for line in cls.iter("line"):
                    statements += 1
                    if int(line.attrib.get("hits", 0)) == 0:
                        missing += 1

                coverage_details.append({
                    "file": filename,
                    "function": name,
                    "statements": statements,
                    "missing": missing,
                    "coverage": f"{line_rate:.0f}%"
                })

        return {
            "overall_coverage": f"{overall:.0f}%",
            "details": coverage_details
        }
    except Exception as e:
        logging.error(f"Failed to parse coverage file {cov_file}: {e}")
        return {"overall_coverage": "0%", "details": []}


def load_history(history_file="reports/history.json"):
    """Load previous test run history."""
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []


def save_history(history, history_file="reports/history.json"):
    os.makedirs("reports", exist_ok=True)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


def make_report(junit_file, cov_file, output_file="final_report.json"):
    results = parse_junit(junit_file)
    coverage = parse_coverage(cov_file)

    final_report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": results["summary"],
        "failures": results["failures"],
        "coverage": coverage
    }

    # Load history and compute deltas
    history = load_history()
    if history:
        last = history[-1]
        final_report["delta"] = {
            "coverage_change": f"{float(coverage['overall_coverage'].strip('%')) - float(last['coverage']['overall_coverage'].strip('%')):.1f}%",
            "passed_change": results["summary"].get("passed", 0) - last["summary"].get("passed", 0),
            "failed_change": results["summary"].get("failed", 0) - last["summary"].get("failed", 0),
        }
    else:
        final_report["delta"] = {"coverage_change": "N/A", "passed_change": "N/A", "failed_change": "N/A"}

    # Save the current report
    out_dir = os.path.dirname(output_file) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(final_report, f, indent=2)


    # Update history
    history.append(final_report)
    save_history(history)

    logging.info(f"Final report written to {output_file}")
    print(f"[INFO] Final report written to {output_file}")

    # Show a quick trend summary in console
    print("\n=== Test Trend (last 5 runs) ===")
    for run in history[-5:]:
        ts = run["timestamp"]
        passed = run["summary"].get("passed", 0)
        failed = run["summary"].get("failed", 0)
        cov = run["coverage"]["overall_coverage"]
        print(f"{ts} | Passed: {passed} | Failed: {failed} | Coverage: {cov}")
    print("================================\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python make_report.py results.xml coverage.xml [output.json]")
        sys.exit(1)

    junit_file = sys.argv[1]
    cov_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "final_report.json"

    make_report(junit_file, cov_file, output_file)
