# only works locally, not in Codespaces
import pandas as pd
import get_changes as a
import os

# git changes summary
# fix truncation
pd.set_option("display.max_colwidth", 500)

# change these as needed
repo_path = "C:/GitPrivate/azure-docs-pr"
author = ""  # leave blank for all; careful of date range.
since = "01/01/2024"
until = "07/31/2024"
branch = "main"
patterns = ["articles/machine-learning"] # what folders to look at.  Not used if author specified.

print(f"*** {since}-{until} branch: {branch} ***")
# get the changes
output = a.get_changes(repo_path, author, since, until, branch)
# print(output)
# filter out blanks.  If no author, filter on patterns
if author == "":
    # filter results based on patterns
    results = [
        line for line in output.split("\n") if any(pattern in line for pattern in patterns) and line.strip()
    ]
else:
    results = [line for line in output.split("\n") if line.strip()]

# create a dataframe from the results
changes = pd.DataFrame([line.split() for line in results])
# now only want columns 4 and beyond.  When there is a rename, there is a 7th column.
changes = changes.iloc[:, 4:]
# name the columns
if changes.shape[1] == 3:
    changes.columns = ["ChangeType", "Filename", "Rename"]
    extra_col = True
    print("Extra columns found")
elif changes.shape[1] == 2:
    changes.columns = ["ChangeType", "Filename"]
else:
    print("Unexpected number of columns found")
    print(changes.shape)
    exit(1)

# show counts for unique files
if author == "":
    print(f"*** Changes in {repo_path} from {since} to {until} (all authors) *** ")
else:
    print(f"*** Changes in {repo_path} by {author} from {since} to {until} ***")

print(pd.crosstab(index=unique["ChangeType"], columns=unique["FileType"]))

# show the added files
print("Added:")
print(unique[(unique["FileType"] == ".md") & (unique["ChangeType"] == "A")]["Filename"])

# show the deleted files
print("Deleted:")
print(unique[(unique["FileType"] == ".md") & (unique["ChangeType"] == "D")]["Filename"])
