
import pandas as pd
import os
import helpers as h

# Function to recursively extract href and name pairs


# Get script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
repo_path = "C:/GitPrivate/azure-ai-docs-pr"
# point to the toc.yml file in the repo path: "articles/ai-studio/toc.yml"
toc_path = os.path.join(repo_path, "articles/ai-studio/toc.yml")
# read the TOC and convert it to a DataFrame
# first read from main - make sure the branch you use is up to date with upstream
h.change_branch(repo_path, "main")
current = h.read_toc(toc_path)

# now from the release branch - again make sure it's up to date first.
h.change_branch(repo_path, "sdg-release-foundry-toc")
release = h.read_toc(toc_path)

# merge the two dataframes show the differences
df = pd.merge(current, release, on='href', how='outer', suffixes=('_current', '_release'), indicator=True)
# Save the DataFrame to a CSV file
current_only = df[df['_merge'] == '_left_only']
release_only = df[df['_merge'] == '_right_only']
current_only.to_csv(os.path.join(script_dir, "current_only.csv"), index=False)
release_only.to_csv(os.path.join(script_dir, "release_only.csv"), index=False)

diffs = df[df['_merge'] != 'both']
diffs.to_csv(os.path.join(script_dir, "diffs.csv"), index=False)