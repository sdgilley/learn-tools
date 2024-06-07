"""
Run merge-report for ml, ai, or both.
"""
import merge_report as m
import argparse
# Create the parser
parser = argparse.ArgumentParser(description="Find number of days and which repo.")
parser.add_argument(
    "input", type=str, nargs="*", help="For how many days and/or which repo: 'ai', 'ml', or 'all'"
)

args = parser.parse_args()  # Parse the arguments

repo_arg = "ml"
days = 8

for arg in args.input:
    if arg.isdigit():
        days = int(arg)
    elif arg.lower() in ["ai", "ml", "all"]:
        repo_arg = arg.lower()

if repo_arg == "all":
    m.merge_report(days, "ai")
    m.merge_report(days, "ml")
else:
    m.merge_report(days, repo_arg)