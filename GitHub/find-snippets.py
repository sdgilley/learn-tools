import find_snippets as f
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Find snippets in docs.')

# Add the arguments
parser.add_argument("repo", type=str, nargs='?', default="ml", 
                    choices=["ai", "ml", "all" ], help="Which repo: 'ai', 'ml', 'fabric', or 'all'")
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

else:
    print (f"Finding snippets in {repo_arg.upper()} docs")
    f.find_snippets(repo_arg)

