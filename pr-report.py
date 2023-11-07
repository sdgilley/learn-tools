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

import requests
import pandas as pd

pr = 2779 # supply the PR you are interested in here.
# TESTING VALUES:
# pr = 2779 # this one will have matches
pr = 2794 # this one also has matches
pr = 2791

# get info about files touched in this PR
response = requests.get(f"https://api.github.com/repos/Azure/azureml-examples/pulls/{pr}/files")
files = response.json()

deleted_files = [file['filename'] for file in files if file['status'] == 'removed']
modified_files = [file['filename'] for file in files if file['status'] == 'modified']
added_files = [file['filename'] for file in files if file['status'] == 'added']

# read the snippets file
import os
import sys

# Check if 'snippets.csv' exists
if os.path.exists('snippets.csv'):
    snippets = pd.read_csv('snippets.csv')
    snippets = snippets[['ref_file', 'from_file']].drop_duplicates()
    snippets = snippets.rename(columns={'from_file': 'referenced_from_file'})
else:
    print("'snippets.csv' does not exist.")
    print("Run 'find-snippets.py' to create the file.")
    sys.exit()

print(f"\n================== PR: {pr} ==============================\n")
for file in modified_files:
    print (f"MODIFIED: {file}")
    if (snippets['ref_file'] == file).any():
        # Print 'from_file' for the matching row(s)
        print(snippets.loc[snippets['ref_file'] == file, ['referenced_from_file']].to_string(index=False))
        print("\n")

for file in deleted_files:
    print (f"DELETED: {file}")
    if (snippets['ref_file'] == file).any():
        # Print 'from_file' for the matching row(s)
        print(snippets.loc[snippets['ref_file'] == file, ['referenced_from_file']].to_string(index=False))
        print("\n")

print(f"ADDED FILES: {len(added_files)}") # just for info about the PR
print(f"\n================== PR: {pr} ==============================\n")