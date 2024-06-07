"""
This script reads through the files in azure-docs (main) and finds code snippets from azureml-examples
It creates two files:

* refs-found.csv - needed for the merge-report and pr-report scripts
* CODEOWNERS.txt - use the contents to populate the CODEOWNERS file in azureml-examples

Run this script periodically to stay up to date with the latest references.
"""

import os
import re
import sys
import utilities as h
import gh_auth as a
import pandas as pd
from datetime import datetime


# read command line arguments
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process some integers.')

# Add the arguments
parser.add_argument("repo", type=str, nargs='?', default="ml", 
                    choices=["ai", "ml"], help="type of learning: 'ai' or 'ml'")
# Parse the arguments
args = parser.parse_args()

# Use the argument
repo_arg = args.repo.lower()

###################### INPUT HERE ############################
# Name the path to your repo. If trying to use a private repo, you'll need a token that has access to it.
repo_name = "MicrosoftDocs/azure-docs"
repo_branch = "main"
if repo_arg == "ai":
    path_in_repo = "articles/ai-studio"
    repo_token = "azureai-samples"
elif repo_arg == "ml":
    path_in_repo = "articles/machine-learning"
    repo_token = "azureml-examples"
else:
    print("Invalid repo value")
    sys.exit()
az_branch = f"{repo_token}-main"
############################ DONE ############################

# Name the file to write the results to. Don't change this, report-pr.py needs this file to work.
script_dir = os.path.dirname(os.path.realpath(__file__))
result_fn = os.path.join(script_dir, f"refs-found-{repo_arg}.csv")
tutorials_fn = os.path.join(script_dir, f"tutorials-{repo_arg}.csv")


found = pd.DataFrame(columns=["ref_file", "from_file"])
dict_list = []
dict_list2 = []
tutorials_list = []
branches = []

# Record the start time
start_time = datetime.now()
# Read files from GitHub
repo = a.connect_repo(repo_name)
# contents = repo.get_contents(path_in_repo, ref=repo_branch)
if repo_arg == "ai": # content here is in sub-directories
    contents = h.get_all_contents(repo, path_in_repo, repo_branch)
else: # ml content only in the given path (is this still correct?)
    contents = repo.get_contents(path_in_repo, ref=repo_branch)

# Now contents contains the list of files to search
print(f"Starting search of {path_in_repo} at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
for content_file in contents:
    # Check if the file is a markdown file
    if content_file.path.endswith(".md"):
        file = os.path.basename(content_file.path)
        # Get the file content
        file_content = content_file.decoded_content
        lines = file_content.decode().splitlines()

        blocks = []
        count = 0
        code_type = None
        inside_code_block = False
        for line in lines:
            # count hard-coded code blocks
            blocks, inside_code_block, count, code_type = h.count_code_lines(
                line, blocks, inside_code_block, count, code_type
            )
            # snippets have ~\azureml-examples in them.  Find all snippets in this file.
            match_snippet = re.findall(
                f'r\(~\/{repo_token}[^)]*\)|source="~\/{repo_token}[^"]*"', line
            )
            if match_snippet:
                for match in match_snippet:
                    path, ref_file, branch, m, name = h.cleanup_matches(match)
                    if "(" in ref_file:  # this might be a mistake
                        print(
                            f"{file}: Warning: Found a snippet with a ( in it: {match}"
                        )
                        print(f" cleaned up match is {m}")
                        print(
                            f"  The snippet was split into {path}\n {ref_file}\n {branch}"
                        )
                    branches.append(branch)
                    if (
                        branch == az_branch
                    ):  # PRs are merged into main, so only these files are relevant
                        row_dict = {"ref_file": ref_file, "from_file": file}
                        dict_list.append(row_dict)
            # count lines in code snippets

            # now look for tutorials that use a whole file
            match_tutorial = re.search(r"nbstart\s+(.*?)\s+-->", line)
            if match_tutorial:
                file_name = match_tutorial.group(1)
                tutorials_list.append({"tutorial": file_name, "from_file": file})
        # done looking through lines of this file
        if inside_code_block:
            print(f"{file}: Warning: A code block started but did not end.")
            print(f"  The last code block type was {code_type} and had {count} lines.")
        if blocks:
            # this file  has code blocks.  add info to the dictionary
            for block in blocks:
                # print(f"{file}: {block[0]} block has {block[1]} lines")
                dict_list2.append({"file": file, "type": block[0], "lines": block[1]})

code_counts = pd.DataFrame.from_dict(dict_list2)
code_counts.to_csv(f"code-counts-{repo_arg}.csv", index=False)

found = pd.DataFrame.from_dict(dict_list)
branches = pd.DataFrame(branches)
tutorials = pd.DataFrame(tutorials_list)
# get rid of duplicates
found = found.drop_duplicates()
branches = branches.drop_duplicates()
# sort the file
if not found.empty:
    found = found.sort_values(by=["ref_file"])
else:
    print("No references found")
    sys.exit()
# write the snippets file
found.to_csv(result_fn, index=False)
# write the tutorials file
# these files won't break the build, so don't need to be in the CODEOWNERS file
# but we do want to track them in the dashboards
tutorials.to_csv(tutorials_fn, index=False)

# now create codeowners file
refs = found["ref_file"].drop_duplicates().replace(" ", "\ ", regex=True)
f = open(os.path.join(script_dir, f"CODEOWNERS-{repo_arg}.txt"), "w+")
for ref in refs:
    f.write(
        f"/{ref} @sdgilley @msakande @Blackmist @ssalgadodev @lgayhardt @fbsolo-ms1  \n"
    )
f.close()

# report the branches in use
print(f"References found in {repo_name} {repo_branch}:")
print(branches.to_string(index=False, header=False, justify="left"))
if "temp-fix" not in branches.values:
    print(
        "Since the 'temp-fix' branch is not in use, update the branch from main.\n See https://github.com/sdgilley/learn-tools/blob/main/fix-the-problem.md#temp-fix-is-not-an-active-branch"
    )

# Record the end time
end_time = datetime.now()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"\nTime elapsed: {elapsed_time/60} minutes")
