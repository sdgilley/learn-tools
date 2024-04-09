'''
This script shows the files deleted or modified in a PR in azureml-examples
If any of these files are referenced azure-docs-pr, 
the corresponding file (labeled referenced_from_file) is also shown.

To run this script, first run find_codeowners.py to create the codeowners.csv file.
Then run from command line:

    python pr-report.py <PR number> 


To decide if the PR is safe to merge:
* If any deleted cell in a MODIFIED file is referenced in azure-docs-pr, PR is not ready to merge
* If any DELETED file is referenced, PR is not ready to merge.
`
'''

import pandas as pd
import sys
import auth_request as a
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

print(f"\n============================== PR: {pr} ==============================")
print(f"https://github.com/Azure/azureml-examples/pull/{pr}/files\n")

prfiles = a.get_auth_response(url)
repo = h.connect_repo("Azure/azureml-examples")

if 'message' in prfiles:
    print("Error occurred.  Check the PR number and try again.")
    print(prfiles)
    sys.exit()
else:
    deleted_files = [file['filename'] for file in prfiles if file['status'] == 'removed']
    modified_files = [(file['filename'], file['blob_url']) for file in prfiles if file['status'] == 'modified']    
    added_files = [file['filename'] for file in prfiles if file['status'] == 'added']


codeowners = h.read_codeowners() # read the codeowners file
# Process the files:
print(f"ADDED FILES: {len(added_files)}\n") # just for info about the PR
modified = len(modified_files)
deleted = len(deleted_files)
print(f"MODIFIED: {modified}") 

alert = False
if modified > 0:
    for file, blob_url in modified_files:
        if any(file in owner for owner in codeowners):
            # Check if there are deleted nb named cells or code comments
            nb, adds, deletes, blob_url = h.find_changes(file, prfiles, blob_url)
            deleted_cells = [value for value in deletes if value not in adds]
            if deleted_cells:
                print('Modified File: {file} deletes content that may be referenced in azure-docs-pr.')
                alert = True


print(f"DELETED: {deleted}")
if deleted > 0:
    found = 0
    for file in deleted_files:
        if any(file in owner for owner in codeowners):
            print(f"DELETED FILE: {file} is used in docs")
            found = 1
            alert = True
    if found == 0:
        print("None of the deleted files are referenced in azure-docs-pr.\n")


if alert:
    print("Contact mldocs@microsoft.com for further instructions.\n")

print(f"\n============================== PR: {pr} ==============================\n")

