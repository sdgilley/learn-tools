def get_changes(repo_path, author, since, until, branch):
    print("Getting changes")
    import subprocess

    # git  whatchanged --author='Sheri Gilley' --since '04/01/2023' --until '03/31/2024' --oneline --pretty=format: | sort | uniq >> ../MonthlyReport/sherichanges.csv

    # cd to the repo, checkout main, and pull to get latest version
    command1 = f"cd {repo_path} && git checkout {branch} && git pull upstream {branch}"
    subprocess.check_output(command1, shell=True, text=True)

    # form command to get changes
    if author:
        command2 = f'git whatchanged --author="{author}" --since {since} --until {until} --oneline --pretty=format:'
    else:
        command2 = f"git whatchanged --since {since} --until {until} --oneline --pretty=format:"

    print(f"Running command: {command2}")
    results = subprocess.check_output(command2, shell=True, text=True, cwd=repo_path)
    return results


if __name__ == "__main__":
    import pandas as pd

    # change these as needed
    repo_path = "C:/GitPrivate/azure-docs-pr"
    author = ""
    since = "03/01/2023"
    until = "04/01/2023"

    output = get_changes(repo_path, author, since, until, "main")
    if author == "":
        results = [
            line
            for line in output.split("\n")
            if "machine-learning" in line and line.strip()
        ]
    else:
        results = [line for line in output.split("\n") if line.strip()]
    changes = pd.DataFrame([line.split() for line in results])

    # print first few lines
    print(changes.head())
    print(changes.shape)


# Function to get metadata from GitHub API
def get_file_metadata(file_path):
    import requests
    import sys
    import os

    repo_owner = "MicrosoftDocs"
    repo_name = "azure-docs"
        # *** AUTHENTICATE
    # Get GH access token from environment variables (assumes you've exported this)
    # try to read GH_ACCESS_TOKEN from environment variables
    # if not there, tell user to set it
    try:
        GITHUB_TOKEN = os.environ["GH_ACCESS_TOKEN"]
    except:
        print("Please set GH_ACCESS_TOKEN environment variable")
        sys.exit()
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

    # get the metadata for each file
    metadata = []
    repo_owner = "your_repo_owner"
    repo_name = "your_repo_name"

    for index, row in df.iterrows():
        filename = row["Filename"]
        # get the metadata
        file_metadata = get_file_metadata(repo_owner, repo_name, filename)
        if file_metadata:
            metadata.append(file_metadata)

    return metadata