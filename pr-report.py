'''
This script shows the files deleted or modified in a PR in azureml-examples
If any of these files are referenced azure-docs-pr, 
the corresponding file (labeled referenced_from_file) is also shown.

To run this script, first run find_snippets.py to create the snippets.csv file.

* If a MODIFIED file is referenced, make sure that a named cell or snippet comment is not removed
* If a DELETED file is referenced, don't approve the PR until you've resolved the problem,
    either by removing the reference 
    or a temporary fix by moving the file to a different branch and changing the reference.
* If you choose a temporary fix, make sure you create a work item to implement a permanent fix.

'''

### USER INPUT HERE ##############
auth = False # set to True to get all responses from the API (e.g. when there are more than 100 items)
             # you'll need to set the GH_ACCESS_TOKEN environment variable for this to work.
pr = 2752  # supply the PR you are interested in here.
####################################

# TESTING VALUES:
# pr = 2779 # this one will have matches
# pr = 2794 # this one also has matches
# pr = 2748 # has 373 modified files.  you'll get a warning if auth is false
# pr = 2791 # has 11 added files, no modified or deleted files

import requests
import pandas as pd
import os
import sys
import auth_request as a

url = f"https://api.github.com/repos/Azure/azureml-examples/pulls/{pr}/files?per_page=100"

print(f"\n============================== PR: {pr} ==============================\n")

if auth:
    files = a.get_auth_response(url)
else:
    response = requests.get(url)
    # Check if there are more items
    if 'next' in response.links:
        print("WARNING: There are more items. Set auth to true to get all responses. \nShowing only first 100")
    files = response.json()

deleted_files = [file['filename'] for file in files if file['status'] == 'removed']
modified_files = [file['filename'] for file in files if file['status'] == 'modified']
added_files = [file['filename'] for file in files if file['status'] == 'added']

# read the snippets file

# Check if 'snippets.csv' exists
if os.path.exists('snippets.csv'):
    snippets = pd.read_csv('snippets.csv')
    snippets = snippets[['ref_file', 'from_file']].drop_duplicates()
    snippets = snippets.rename(columns={'from_file': 'referenced_from_file'})
else:
    print("'snippets.csv' does not exist.")
    print("Run 'find-snippets.py' to create the file.")
    sys.exit()


# Process the files:

modified = len(modified_files)
print(f"MODIFIED: {modified}") 
if modified > 0:
    found = 0
    for file in modified_files:
        if (snippets['ref_file'] == file).any():
            # Print 'from_file' for the matching row(s)
            print(snippets.loc[snippets['ref_file'] == file].rename(columns={'ref_file': 'MODIFIED'})[['MODIFIED']].drop_duplicates().to_string(index=False, justify='left'))
            print(snippets.loc[snippets['ref_file'] == file].rename(columns={'referenced_from_file': 'REFERENCED IN'})[['REFERENCED IN']].to_string(index=False, justify='left'))

            print("\n")
            found = +1
    if found == 0:
        print("None of these files are referenced in azure-docs-pr.\n")

deleted = len(deleted_files)
print(f"DELETED: {deleted}")
if deleted > 0:
    found = 0
    for file in deleted_files:
        if (snippets['ref_file'] == file).any():
            # Print 'from_file' for the matching row(s)
            print(snippets.loc[snippets['ref_file'] == file].rename(columns={'ref_file': 'DELETED'})[['DELETED']].drop_duplicates().to_string(index=False, justify='left'))
            print(snippets.loc[snippets['ref_file'] == file].rename(columns={'referenced_from_file': 'REFERENCED IN'})[['REFERENCED IN']].to_string(index=False, justify='left'))
            print("\n")
            found = +1
    if found == 0:
        print("None of these files are referenced in azure-docs-pr.\n")


print(f"ADDED FILES: {len(added_files)}") # just for info about the PR
print(f"\n============================== PR: {pr} ==============================\n")