# list old articles
from get_filelist import get_filelist
import pandas as pd

# inputs here
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/ai-foundry"
me = 'sgilley'
ago = 180
csvfile = "ai-foundry.csv"
pull = False # change to True first time you run, then to False to save time
# end of inputs

articles = get_filelist(repo_path, "ms.author", "main", pull=False)
print(f" Total articles: {articles.shape[0]}")

articles.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")
