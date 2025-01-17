# find metadata from file in a local repo

def get_filelist(repo_path, fstr, branch="main", pull=False, cdonly=False):
    import pandas as pd
    import subprocess
    # cd to the repo, checkout main, and pull to get latest version
    if cdonly:
        command1 = f"cd {repo_path}"
    elif pull:
        command1 = f"cd {repo_path} && git checkout {branch} && git pull upstream {branch}"
    else:
        command1 = f"cd {repo_path} && git checkout {branch}"
    subprocess.check_output(command1, shell=True, text=True)

    # find the metadata in the md files

    command1 = f'findstr /S "{fstr}" *.md'
    print(f"Running command: {command1}")
    output = subprocess.check_output(command1, shell=True, text=True, cwd=repo_path)
    lines = output.strip().split('\n')
    data = [line.split(f':{fstr}: ') for line in lines]
    df = pd.DataFrame(data, columns=['filename', f'{fstr}'])

    return df

if __name__ == "__main__":
    repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/ai-studio"
    articles = get_filelist(repo_path, "ms.author", "main", pull=False)
    
    print(f" Total articles: {articles.shape[0]}")
    print(articles.head())



