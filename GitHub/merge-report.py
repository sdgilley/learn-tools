import requests
import pandas as pd
import sys
import auth_request as a
from datetime import datetime, timedelta
import argparse
import utilities as h

# Create the parser
parser = argparse.ArgumentParser(description='Find number of days.')
parser.add_argument('days', type=int, default=7, nargs='?', help='For how many days?') # Add optional arguments
args = parser.parse_args() # Parse the arguments

snippets = h.read_snippets() # read the snippets file

# Calculate the date to filter by
if args.days < 100:
    days_ago = (datetime.now() - timedelta(days=args.days)).isoformat()
else:
    print("ERROR: The maximum number of days is 100.")
    sys.exit()

# Define the URL for the GitHub API
url = "https://api.github.com/repos/Azure/azureml-examples/pulls?state=closed&sort=updated&direction=desc"

# Send a GET request to the GitHub API
response = requests.get(url)

# Convert the response to JSON
data = response.json()

print(f"\n============================== MERGED IN LAST {args.days} DAYS ==============================\n")
# Filter the PRs that were merged in the last 7 days
merged_prs = [pr['number'] for pr in data if pr['merged_at'] and pr['merged_at'] > days_ago]
print (f"Total PRs merged: {len(merged_prs)}")

data = [] # create an empty list to hold data for modified files that are referenced
# loop through the PRs 
for pr in merged_prs:  
    # now get file info for each PR
    url = f"https://api.github.com/repos/Azure/azureml-examples/pulls/{pr}/files?per_page=100"
    prfiles = a.get_auth_response(url)  
    modified_files = [file['filename'] for file in prfiles if file['status'] == 'modified']

    # See if any of the file changes are reference problems
    if len(modified_files) > 0:

        for file in modified_files:
            if (snippets['ref_file'] == file).any():
                snippet_match = snippets.loc[snippets['ref_file'] == file, 'from_file']
                # Append the data to the list
                data.append({'PR': pr, 'Modified File': file, 'Referenced In': snippet_match.to_string(index=False)})

# done with all the PRs.  Now process the data 

df = pd.DataFrame(data) # Convert the list to a DataFrame
if df.empty:
    print("\nNothing to do here :-)  There are no PRs that impacted references.\n")
    sys.exit()
else:
    print("\nCheck the following PRs to see if any referenced docs need to be updated:\n")
    # Group the DataFrame by PR
    grouped_by_pr = df.groupby('PR')

    # Loop through the PR groups
    for pr, pr_group in grouped_by_pr:
        print(f"* PR {pr} (https://github.com/Azure/azureml-examples/pull/{pr}/files)")

        # Group the PR group by Modified File
        grouped_by_file = pr_group.groupby('Modified File')

        # Loop through the Modified File groups
        for modified_file, file_group in grouped_by_file:
            print(f"     Modified: {modified_file}")
            print(f"     Referenced in: ")

            for index, row in file_group.iterrows():
                refs = row['Referenced In'].split('\n')
                for ref in refs:
                    print(f"       https://github.com/MicrosoftDocs/azure-docs-pr/edit/main/articles/machine-learning/{ref.strip()}")
                # print(f"  {row['Referenced In']}")
        print()

print(f"\n============================== /MERGED IN LAST {args.days} DAYS ==============================\n")