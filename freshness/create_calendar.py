# list old articles
import get_filelist as h
import fix_titles as f
import pandas as pd
import os

# inputs here
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/ai-foundry"
ago = 90
csvfile = "ai-studio-list.csv"
# end of inputs

# get script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
csvfile = os.path.join(script_dir, csvfile)
eng_file = os.path.join(script_dir, "freshness.csv")
# Checkout the branch and pull latest changes if needed...
# h.checkout(repo_path, "main")
authors_df = h.get_filelist(repo_path, "ms.author")
dates_df = h.get_filelist(repo_path, "ms.date")
titles_df = h.get_filelist(repo_path, "title")
# description_df = h.get_filelist(repo_path, "description")

# remove quotes from titles
titles_df['title'] = titles_df['title'].str.replace(r'"', '')
titles_df['title'] = titles_df['title'].str.replace(r"'", '')
# add - Azure AI Foundry to the titles
titles_df['title'] = titles_df['title'] + " - Azure AI Foundry"

merged = pd.merge(dates_df, authors_df, on='filename')
articles = pd.merge(merged, titles_df, on='filename')
# articles = pd.merge(articles, description_df, on='filename')

print(f" Total articles: {merged.shape[0]}")

# # merge in engagement stats
engagement = pd.read_csv(eng_file, usecols=['Title', 'PageViews'])
print(engagement.head())
articles = articles.merge(engagement, how='left', left_on='title', right_on='Title')

# save to a csv file
articles.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")
exit()

# Convert ms.date to datetime
articles['ms.date'] = pd.to_datetime(articles['ms.date'], errors='coerce')

# filter out articles that are in the includes folder:
articles = articles[~articles['filename'].str.startswith('includes')]

# find the date when refresh needed
articles['refresh'] = articles['ms.date'] + pd.DateOffset(days=ago)

# now truncate refresh to the month
articles['refresh'] = articles['refresh'].dt.to_period('M').dt.to_timestamp()

# read work items and merge by title
work_items = pd.read_csv(os.path.join(script_dir, "existing-items.csv"))
work_items = f.fix_titles(work_items)

# merge articles with work_items:
articles = articles.merge(work_items, how='left', left_on='title', right_on='Title')

# create work item spreadsheet for Feb - if refresh is Feb or before:
cutoff_date = pd.Timestamp('2025-03-01')
work_items = articles[articles['refresh'] < cutoff_date]

# filter out ones with a work item already
work_items = work_items[work_items['ID'].isnull()]
# save to a csv file
work_items.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")

