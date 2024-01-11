'''
This script reads through the files in azure-docs (main) and finds code snippets from azureml-examples
It creates two files:

* refs-found.csv - needed for the merge-report and pr-report scripts
* CODEOWNERS.txt - use the contents to populate the CODEOWNERS file in azureml-examples

Run this script periodically to stay up to date with the latest references.
'''

import os
import re
import sys
import utilities as h
from github import Github
import pandas as pd
import time

###################### INPUT HERE ############################
# Name the path to your repo. If trying to use a private repo, you'll need a token that has access to it.
repo_name = "MicrosoftDocs/azure-docs"
repo_branch = "main"
path_in_repo = 'articles/machine-learning' 
############################ DONE ############################

# Name the file to write the results to. Don't change this, report-pr.py needs this file to work.
script_dir = os.path.dirname(os.path.realpath(__file__))
result_fn = os.path.join(script_dir,"refs-found.csv")
az_ml_branch = "azureml-examples-main"

found = pd.DataFrame(columns=['ref_file', 'from_file'])
dict_list = []
branches = []
# Record the start time
start_time = time.time()
# Read files from GitHub  
repo = h.connect_repo(repo_name)
contents = repo.get_contents(path_in_repo, ref=repo_branch)

print(f"Starting search at {start_time}")
# look through the markdown files in the repo
for content_file in contents:
    # Check if the file is a markdown file
    if content_file.path.endswith(".md"):
        file = os.path.basename(content_file.path)
        # Get the file content
        file_content = content_file.decoded_content
        lines = file_content.decode().splitlines()

        for line in lines:
            # snippets have ~\azureml-examples in them.  Find all snippets in this file.
            match_snippet = re.findall(r'\(~\/azureml-examples[^)]*\)|source="~\/azureml-examples[^"]*"', line)
            if match_snippet:
                for match in match_snippet:
                    path, ref_file, branch, match, name = h.cleanup_matches(match)
                    branches.append(branch)
                    if branch == az_ml_branch: #PRs are merged into main, so only these files are relevant
                        row_dict = {'ref_file': ref_file, 'from_file': file}
                        dict_list.append(row_dict)

found = pd.DataFrame.from_dict(dict_list)
branches = pd.DataFrame(branches)
# get rid of duplicates
found = found.drop_duplicates()
branches = branches.drop_duplicates()
# sort the file
if not found.empty:
    found = found.sort_values(by=['ref_file'])
else:
    print("No references found")
    sys.exit()
# write the snippets file
found.to_csv(result_fn, index=False)

# now create codeowners file
refs = found['ref_file'].drop_duplicates().replace(" ", "\ ", regex=True)
f = open(os.path.join(script_dir,'CODEOWNERS.txt'), 'w+')
for ref in refs:
    f.write(f"/{ref} @sdgilley @msakande @Blackmist @ssalgadodev @lgayhardt @fbsolo-ms1  \n")
f.close()

# report the branches in use
print(f"References found in {repo_name} {repo_branch}:")
print (branches.to_string(index=False, header=False, justify='left'))

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"\nTime elapsed: {elapsed_time/60} minutes")