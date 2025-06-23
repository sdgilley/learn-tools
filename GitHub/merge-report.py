"""
Run merge-report for ml, ai, or both.
"""
import GitHub.utilities.merge_report as m
import argparse
# Create the parser
parser = argparse.ArgumentParser(description="Find number of days and which service.")
parser.add_argument(
    "input", type=str, nargs="*", help="For how many days and/or which service: 'ai', 'ml', or 'all'"
)

args = parser.parse_args()  # Parse the arguments

service = "all"  # Default service
days = 8

for arg in args.input:
    if arg.isdigit():
        days = int(arg)
    elif arg.lower() in ["ai", "ml", "all"]:
        service = arg.lower()

if service == "all":
    m.merge_report(days, "ai")
    m.merge_report(days, "ml")
    m

else:
    m.merge_report(days, service)