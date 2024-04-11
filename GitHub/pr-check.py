'''
This script checks a PR for deleted files, cells or code snippets in files used in docs.

    python pr-report2.py <PR number> 

If the PR has problems, it prints a message to check with the docs team.

'''

import pandas as pd
import sys
import gh_auth as a
import utilities as h

# read arguments from command line - pr and optionally, whether to authenticate
import argparse
parser = argparse.ArgumentParser(description='Process a PR number.') # Create the parser
# Add the arguments
parser.add_argument('pr', type=int, help='The PR number you are interested in.')
args = parser.parse_args() # Parse the arguments
pr = args.pr

# form the URL for the GitHub API
url = f"https://api.github.com/repos/Azure/azureml-examples/pulls/{pr}/files?per_page=100"

# print(f"\n============================== PR: {pr} ==============================")
# print(f"https://github.com/Azure/azureml-examples/pull/{pr}/files\n")

prfiles = a.get_auth_response(url)
repo = a.connect_repo("Azure/azureml-examples")

if 'message' in prfiles:
    print("Error occurred.  Check the PR number and try again.")
    print(prfiles)
    sys.exit()
else:
    deleted_files = [file['filename'] for file in prfiles if file['status'] == 'removed']
    modified_files = [(file['filename'], file['blob_url']) for file in prfiles if file['status'] == 'modified']    
    added_files = [file['filename'] for file in prfiles if file['status'] == 'added']

alert = False
# read the codeowners file to see which files we care about
codeowners = h.read_codeowners() # read the codeowners file

# files modified in the PR
if modified_files:
    for file, blob_url in modified_files:
        if any(file in owner for owner in codeowners):
            # Check if there are deleted nb named cells or code comments
            nb, adds, deletes, blob_url = h.find_changes(file, prfiles, blob_url)

            # if deleted but added back somewhere, not a problem.  
            # Only alert if the name is truly gone.
            deleted_cells = [value for value in deletes if value not in adds]
            if deleted_cells:
                print(f'{file} deletes content that may be referenced in azure-docs-pr.')
                alert = True

# files deleted in the PR
if deleted_files:
    for file in deleted_files:
        if any(file in owner for owner in codeowners):
            print(f"DELETED FILE: {file} is used in docs")
            alert = True


if alert:
    print("** Contact mldocs@microsoft.com for further instructions. **\n")
else:
    print("No docs problems found in this PR.\n")
## test PRs:
# 3081 - no problems
# 2890 - deletes files 
# 2888 - deletes ids in a file 
# 3113 - deletes a cell in a notebook 