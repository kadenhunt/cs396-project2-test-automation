# Standard library imports
import sys                   # lets us read command-line arguments (e.g., file names)
import xml.etree.ElementTree as ET  # built-in XML parser
import json                  # for writing the final report as JSON


def parse_junit(junit_file):
    """Parse JUnit XML (pytest results) and return summary + failure details."""
    tree = ET.parse(junit_file)   # load the XML tree from file
    root = tree.getroot()         # get the root element <testsuite>

    # Top-level stats are stored as attributes on the <testsuite>
    total = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
    skipped = int(root.attrib.get("skipped", 0))

    # Calculate passed tests
    passed = total - failures - errors - skipped

    # Collect details for each failed test case
    failure_details = []
    for testcase in root.iter("testcase"):          # loop through <testcase> elements
        for failure in testcase.iter("failure"):    # check if it has a <failure> tag
            failure_details.append({
                "test": testcase.attrib.get("name"),       # test function name
                "classname": testcase.attrib.get("classname"),  # file/class context
                "error": failure.attrib.get("message", "").strip(),  # failure summary
                "details": failure.text.strip() if failure.text else ""  # traceback text
            })

    # Return structured summary + failures
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


def parse_coverage(cov_file):
    """Parse coverage XML and return overall + per-function stats."""
    tree = ET.parse(cov_file)   # load coverage.xml
    root = tree.getroot()       # root <coverage> element

    # Overall project coverage percentage (line-rate is a 0–1 float)
    overall = float(root.attrib.get("line-rate", 0)) * 100

    coverage_details = []
    for package in root.iter("package"):     # loop through all packages (modules)
        for cls in package.iter("class"):   # each <class> is usually a function
            name = cls.attrib.get("name")
            filename = cls.attrib.get("filename")
            line_rate = float(cls.attrib.get("line-rate", 0)) * 100

            # Count how many statements are present/missing
            statements = 0
            missing = 0
            for line in cls.iter("line"):
                statements += 1
                if int(line.attrib.get("hits", 0)) == 0:  # line not covered
                    missing += 1

            coverage_details.append({
                "file": filename,
                "function": name,
                "statements": statements,
                "missing": missing,
                "coverage": f"{line_rate:.0f}%"   # format percentage as whole number
            })

    return {
        "overall_coverage": f"{overall:.0f}%",
        "details": coverage_details
    }


def make_report(junit_file, cov_file, output_file="final_report.json"):
    """Combine test results + coverage into a single JSON report."""
    results = parse_junit(junit_file)
    coverage = parse_coverage(cov_file)

    # Build one consolidated object
    final_report = {
        "summary": results["summary"],
        "failures": results["failures"],
        "coverage": coverage
    }

    # Save it as JSON
    with open(output_file, "w") as f:
        json.dump(final_report, f, indent=2)

    print(f"[INFO] Final report written to {output_file}")


if __name__ == "__main__":
    # Require at least 2 arguments: results.xml + coverage.xml
    if len(sys.argv) < 3:
        print("Usage: python make_report.py results.xml coverage.xml [output.json]")
        sys.exit(1)

    junit_file = sys.argv[1]                   # first arg: path to results.xml
    cov_file = sys.argv[2]                     # second arg: path to coverage.xml
    output_file = sys.argv[3] if len(sys.argv) > 3 else "final_report.json"

    # Generate the combined report
    make_report(junit_file, cov_file, output_file)
