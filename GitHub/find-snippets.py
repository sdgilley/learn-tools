import find_snippets as f
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Find snippets in docs.')

# Add the arguments
parser.add_argument("repo", type=str, nargs='?', default="ml", 
                    choices=["ai", "ml","all"], help="Which repo: 'ai', 'ml' or 'all'")
# Parse the arguments
args = parser.parse_args()

# Use the argument
repo_arg = args.repo.lower()
if repo_arg == "all":
    print ("Finding all snippets in AI and ML docs")
    print ("AI snippets")
    f.find_snippets("ai")
    print ("ML snippets")
    f. find_snippets("ml")
elif repo_arg == "ai":
    print ("Finding snippets in AI docs")
    f.find_snippets("ai")
elif repo_arg == "ml":
    print ("Finding snippets in ML docs")
    f.find_snippets("ml")
else:
    print("Invalid argument.  Must be 'ai', 'ml' or 'all'")
