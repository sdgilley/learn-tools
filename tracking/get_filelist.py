# find ms.dates & authors for all files
import pandas as pd
import subprocess

def get_filelist(repo_path, branch="main", pull=False):
    # cd to the repo, checkout main, and pull to get latest version
    if pull:
        command1 = f"cd {repo_path} && git checkout {branch} && git pull upstream {branch}"
    else:
        command1 = f"cd {repo_path} && git checkout {branch}"
    subprocess.check_output(command1, shell=True, text=True)

    # get the dates
    command1 = 'findstr /S "ms.date" *.md'
    print(f"Running command: {command1}")
    dates_output = subprocess.check_output(command1, shell=True, text=True, cwd=repo_path)
    # Parse the dates output
    dates_lines = dates_output.strip().split('\n')
    dates_data = [line.split(':ms.date: ') for line in dates_lines]
    dates_df = pd.DataFrame(dates_data, columns=['filename', 'date'])

    # get the authors
    command1 = 'findstr /S "ms.author" *.md'
    print(f"Running command: {command1}")
    authors_output = subprocess.check_output(command1, shell=True, text=True, cwd=repo_path)
    authors_lines = authors_output.strip().split('\n')
    authors_data = [line.split(':ms.author: ') for line in authors_lines]
    authors_df = pd.DataFrame(authors_data, columns=['filename', 'author'])
    merged = pd.merge(dates_df, authors_df, on='filename')

    # get the titles
    command1 = 'findstr /S "title" *.md'
    print(f"Running command: {command1}")
    titles_output = subprocess.check_output(command1, shell=True, text=True, cwd=repo_path)
    titles_lines = titles_output.strip().split('\n')
    titles_data = [line.split(':title: ') for line in titles_lines]
    titles_df = pd.DataFrame(titles_data, columns=['filename', 'title'])
    # drop the quotes
    titles_df['title'] = titles_df['title'].str.replace(r'"', '')
    titles_df['title'] = titles_df['title'].str.replace(r"'", '')

    merged = pd.merge(dates_df, authors_df, on='filename')
    merged = pd.merge(merged, titles_df, on='filename')
    # Clean the date strings
    merged['date'] = merged['date'].str.strip()
    # Convert the date column to datetime
    merged['date'] = pd.to_datetime(merged['date'], errors='coerce')
    # Clean the author & title strings
    merged['author'] = merged['author'].str.strip()
    merged['title'] = merged['title'].str.strip()
    # filter out component-reference files
    merged = merged[~merged['filename'].str.contains(r'component-reference\\')]
    merged = merged[~merged['filename'].str.contains(r'component-reference-v2\\')]
    # filter out includes
    merged = merged[~merged['filename'].str.contains(r'includes\\')]
    return merged

if __name__ == "__main__":
    repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/machine-learning"
    articles = get_filelist(repo_path, "main", pull=False)
    
    print(f" Total articles: {articles.shape[0]}")
    print(articles.head())



