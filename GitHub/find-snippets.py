'''
This script reads through the files in azure-docs (main) and finds code snippets from azureml-examples
It creates two files:

* refs-found.csv - needed for the merge-report and pr-report scripts
* CODEOWNERS.txt - use the contents to populate the CODEOWNERS file in azureml-examples

Run this script periodically to stay up to date with the latest references.
'''

import os
import re
import utilities as h
from github import Github
import pandas as pd

###################### INPUT HERE ############################
# Name the path to your repo.
repo_name = "MicrosoftDocs/azure-docs"
path_in_repo = 'articles/machine-learning' 
############################ DONE ############################

# Name the file to write the results to. Don't change this, report-pr.py needs this file to work.
result_fn = "refs-found.csv"
main_branch = "azureml-examples-main"
found = pd.DataFrame(columns=['ref_file', 'from_file'])
dict_list = []

# Read files from GitHub  
try:
    token = os.environ['GH_ACCESS_TOKEN']   
except:
    print("Please set GH_ACCESS_TOKEN environment variable")
    sys.exit()  

g = Github(token)
repo = g.get_repo(repo_name)

contents = repo.get_contents(path_in_repo)

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
                    if branch == main_branch: #PRs are merged into main, so only these files are relevant
                        row_dict = {'ref_file': ref_file, 'from_file': file}
                        dict_list.append(row_dict)

found = pd.DataFrame.from_dict(dict_list)
# get rid of duplicates
found = found.drop_duplicates()
# sort the file
found = found.sort_values(by=['ref_file'])

# write the snippets file
found.to_csv(result_fn, index=False)

# now create codeowners file
refs = found['ref_file'].drop_duplicates().replace(" ", "\ ", regex=True)
f = open('CODEOWNERS.txt', 'w+')
for ref in refs:
    f.write(f"/{ref} @ML \n")
f.close()

