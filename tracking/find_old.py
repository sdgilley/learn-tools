# list old articles
from get_filelist import get_filelist
import pandas as pd

# inputs here
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/machine-learning"
me = 'sgilley'
ago = 180
csvfile = "machine-learning.csv"
pull = False # change to True first time you run, then to False to save time
# end of inputs

articles = get_filelist(repo_path, "main", pull=pull) 
print(f" Total articles: {articles.shape[0]}")

# merge in engagement stats
# find script path
import os
script_path = os.path.dirname(os.path.realpath(__file__))
engagement = pd.read_csv(os.path.join(script_path,"july.csv"))
# keep only the columns we need: Url, PageViews
engagement = engagement[['Title','PageViews']]
# strip  - Azure Machine Learning from the title
engagement['Title'] = engagement['Title'].str.replace(r' - Azure Machine Learning$', '', regex=True)
engagement['PageViews'] = engagement['PageViews'].str.replace(',', '')
engagement['PageViews'] = pd.to_numeric(engagement['PageViews'])
# drop .md from filename for the merge
# articles['filename'] = articles['filename'].str.replace(r'\.md$', '', regex=True)
# print (articles.head())
# print (engagement.head())
# exit()
articles = articles.merge(engagement, how='left', left_on='title', right_on='Title')
# save all articles to a csv file
articles.to_csv(csvfile, index=False)

# recent_articles = articles[articles['date'] > pd.Timestamp('today') - pd.DateOffset(days=30)]
# Find old articles
old_articles = articles[articles['date'] < pd.Timestamp('today') - pd.DateOffset(days=ago)]
print(f"Over {ago} days old (all): {old_articles.shape[0]}")
# now find those old articles without 'v1\' in the filename
old_articles = old_articles[~old_articles['filename'].str.contains(r'v1\\')]
print(f"Over {ago}  days old (no v1): {old_articles.shape[0]}")

# find my old articles
my_articles = old_articles[old_articles['author'] == me]
print(f"My articles over {ago} days old: {my_articles.shape[0]}")

# sort by PageView
print(my_articles.sort_values(by='PageViews', ascending=False))
