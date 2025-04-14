# Functions
import subprocess
import os
import pandas as pd
import yaml

def change_branch(repo_path, branch):
    print(f"Switching to branch {branch} in {repo_path}")
    import subprocess

    command1 = f"cd {repo_path} && git checkout {branch}"
    # modify the command if there is a need to pull
        # cd to the repo, checkout main, and pull to get latest version
    subprocess.check_output(command1, shell=True, text=True)

def extract_pairs(items, pairs):
    for item in items:
        if 'href' in item and 'name' in item:
            pairs.append({'href': item['href'], 'name': item['name']})
        if 'items' in item and isinstance(item['items'], list) and item['items']:
            # Check if 'items' key exists, is a list, and is non-empty
            extract_pairs(item['items'], pairs)


def read_toc(toc_path):
    with open(toc_path, 'r') as file:
        toc = yaml.safe_load(file)

    # Initialize an empty list to store the pairs
    pairs = []

    # Extract pairs from the top-level items
    extract_pairs(toc['items'], pairs)
    # Convert the list of pairs to a DataFrame
    df = pd.DataFrame(pairs)
    return df

# test the functions

if __name__ == "__main__":
    repo_path = "C:/GitPrivate/azure-ai-docs-pr"
    # point to the toc.yml file in the repo path: "articles/ai-foundry/toc.yml"
    toc_path = os.path.join(repo_path, "articles/ai-foundry/toc.yml")
    read_toc(toc_path)