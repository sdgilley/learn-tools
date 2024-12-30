# list old articles
from get_filelist import get_filelist
import pandas as pd

# inputs here
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/ai-studio"
me = 'sgilley'
ago = 180
csvfile = "ai-studio-list.csv"
pull = False # change to True first time you run, then to False to save time
# end of inputs

authors_df = get_filelist(repo_path, "ms.author", "main", cdonly=True)
dates_df = get_filelist(repo_path, "ms.date", "main", cdonly=True)
titles_df = get_filelist(repo_path, "title", "main", cdonly=True)
description_df = get_filelist(repo_path, "description", "main", cdonly=True)
# remove quotes from titles
titles_df['title'] = titles_df['title'].str.replace(r'"', '')
titles_df['title'] = titles_df['title'].str.replace(r"'", '')

merged = pd.merge(dates_df, authors_df, on='filename')
articles = pd.merge(merged, titles_df, on='filename')
articles = pd.merge(articles, description_df, on='filename')


print(f" Total articles: {merged.shape[0]}")

# merge in engagement stats
# find script path
# import os
# script_path = os.path.dirname(os.path.realpath(__file__))
# engagement = pd.read_csv(os.path.join(script_path,"august.csv"))
# # keep only the columns we need: Url, PageViews
# engagement = engagement[['Title','PageViews']]
# # strip  - Azure Machine Learning from the title
# engagement['Title'] = engagement['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
# engagement['PageViews'] = engagement['PageViews'].str.replace(',', '')
# engagement['PageViews'] = pd.to_numeric(engagement['PageViews'])
# articles = articles.merge(engagement, how='left', left_on='title', right_on='Title')

# Convert ms.date to datetime
articles['ms.date'] = pd.to_datetime(articles['ms.date'], errors='coerce')


# find the date when refresh needed
articles['refresh'] = articles['ms.date'] + pd.DateOffset(days=180)
# now truncate refresh to the month
articles['refresh'] = articles['refresh'].dt.strftime('%Y-%m')
# save all articles to a csv file
articles.to_csv(csvfile, index=False)
print (f"Saved to {csvfile}")
