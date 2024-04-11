def get_changes(repo_path, author, since, until):
    print("Getting changes")
    import subprocess


    # git  whatchanged --author='Sheri Gilley' --since '04/01/2023' --until '03/31/2024' --oneline --pretty=format: | sort | uniq >> ../MonthlyReport/sherichanges.csv
    command1 = f"cd {repo_path} && git checkout main && git pull"
    subprocess.check_output(command1, shell=True, text=True)
    if author:
        command2 = f'git whatchanged --author="{author}" --since {since} --until {until} --oneline --pretty=format:'
    else:
        command2 = f'git whatchanged --since {since} --until {until} --oneline --pretty=format:'

    results = subprocess.check_output(command2, shell=True, text=True, cwd=repo_path)
    return results

if __name__ == "__main__":
    import pandas as pd

    # change these as needed
    repo_path = "C:/GitPrivate/azure-docs-pr"
    author = 'Sheri Gilley'
    since = '03/01/2023'
    until = '04/01/2024'

    # other code...

    output = get_changes(repo_path, author, since, until)
    if author == '':
        results = [line for line in output.split('\n') if "machine-learning" in line and line.strip()]
    else:
        results = [line for line in output.split('\n') if line.strip()]
    changes = pd.DataFrame([line.split() for line in results])

    # print first few lines
    print(changes.head())
    print(changes.shape)
