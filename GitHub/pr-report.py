'''
This script shows the files deleted or modified in a PR in azureml-examples
If any of these files are referenced azure-docs-pr, 
the corresponding file (labeled referenced_from_file) is also shown.

To run this script, first run find_snippets.py to create the snippets.csv file.
Then run from command line:

    python pr-report.py <PR number> 

If you get a warning that only first 100 are shown, add "True" to the end of the command line:

    python pr-report.py <PR number> True

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
# fix truncation?
pd.set_option('display.max_colwidth', 500)

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
    modified_files = [file['filename'] for file in prfiles if file['status'] == 'modified']
    added_files = [file['filename'] for file in prfiles if file['status'] == 'added']


snippets = h.read_snippets() # read the snippets file

# Process the files:
print(f"ADDED FILES: {len(added_files)}\n") # just for info about the PR
modified = len(modified_files)
deleted = len(deleted_files)
print(f"MODIFIED: {modified}") 

data =[] # create an empty list to hold data for modified files that are referenced
if modified > 0:
    for file in modified_files:
        if (snippets['ref_file'] == file).any():
            snippet_match = snippets.loc[snippets['ref_file'] == file, 'from_file']
            # Check if there are deleted nb named cells or code comments
            nb, adds, deletes = h.find_changes(file, prfiles)
            deleted_cells = [value for value in deletes if value not in adds]
            if deleted_cells:
                cell_type = "Notebook" if nb else "Code"
                for cell in deleted_cells:
                    # Append the data to the list
                    data.append({'Modified File': file,
                             'Referenced In': snippet_match.to_string(index=False),
                             'Cell Type': cell_type,
                             'Cell': cell})
                   # print(f"*** {cell}")
if data == []:
    print("None of the modified files have deleted cells or code snippets.\n")
else:
    # Group the data by 'Modified File' and 'Referenced In'
    grouped_data = {}
    for item in data:
        key = (item['Modified File'], item['Referenced In'])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item['Cell'])

    # Print the grouped data
    for (modified_file, referenced_in), cells in grouped_data.items():
        print(f"Modified File: {modified_file} \n  Referenced in:")
        refs = referenced_in.split('\n')
        for ref in refs:
            print(f"   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/{ref.strip()}")
        print(f"   {cell_type} cells deleted: {len(cells)}")
        for cell in cells:
            print(f"   * {cell}")
        # compare the sha to this same file in branch "temp-fix"
        h.compare_branches(repo, file, "main", "temp-fix")
        print()
print(f"DELETED: {deleted}")
if deleted > 0:
    found = 0
    for file in deleted_files:
        if (snippets['ref_file'] == file).any():
            snippet_match = snippets.loc[snippets['ref_file'] == file, 'from_file']

            print(f"DELETED FILE: {file} \n  Referenced in:")
            refs = snippet_match.to_string(index=False).split('\n')
            for ref in refs:
                print(f"   https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/{ref.strip()}")
           # print(snippet_match.to_string(index=False))
            h.compare_branches(repo, file, "main", "temp-fix")
            found = +1
    if found == 0:
        print("None of the deleted files are referenced in azure-docs-pr.\n")

print(f"\n============================== PR: {pr} ==============================\n")

