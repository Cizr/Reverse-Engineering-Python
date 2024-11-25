import os
import json
from radon.metrics import mi_visit, h_visit
from radon.complexity import cc_visit


def analyze_file(file_path):
    """Analyze a single Python file and calculate code metrics."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Calculate metrics
    loc = len(content.splitlines())  # Lines of code
    cc_scores = cc_visit(content)    # Cyclomatic complexity scores
    avg_cc = sum(x.complexity for x in cc_scores) / len(cc_scores) if cc_scores else 0
    mi = mi_visit(content, True)     # Maintainability Index
    halstead = h_visit(content)      # Halstead metrics

    return {
        "LOC": loc,
        "Cyclomatic Complexity": avg_cc,
        "Maintainability Index": mi,
        "Halstead Volume": halstead.total if halstead else 0,
    }


def analyze_codebase(path):
    """Analyze a codebase (single file or directory) and return the results."""
    results = {}
    if os.path.isfile(path):  # Check if the path is a file
        results[os.path.basename(path)] = analyze_file(path)
    return results


def save_results(results, output_file):
    """Save analysis results to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    # File path to analyze
    path = "pyreverseUML.py"  # Replace with your Python file path
    output_file = "code_metrics.json"

    # Analyze the codebase and save results
    results = analyze_codebase(path)
    save_results(results, output_file)

    print(f"Code metrics saved to {output_file}")
