# !IMPORTANT - sign in with az login --use-device-code before running this script
# Finds the list of files that need to be refreshed for either this month or next month.
# creates a csv file with the list of files that need to be refreshed.
import get_filelist as h
import fix_items as f
import query_work_items as q
import pandas as pd
import os

################################## inputs
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/machine-learning" # your local repo
offset = 1  # for items going stale next month, use offset = 2. 
            # for this month's items use offset = 1
req = 360 # required freshness in days
csvfile = "mar-foundry-work-items.csv" # This is the file that will be created with the work items
allfiles = "all-files-revised.csv" # This is the file that will be created with all the files
eng_file = "Jan-engagement.xlsx" # where the engagement stats are
# NOTE: you need to set the Sensitivity label to General on the Excel file
################################## end of inputs

# Calculate the cutoff date (90 days before the end of the month)
now = pd.Timestamp.now()
end_of_month = now + pd.offsets.MonthEnd(offset)
cutoff_date = end_of_month - pd.Timedelta(days=req)
print(f"Cutoff date: {cutoff_date}")
freshness_title = f"Freshness - over {req}:  "  

# get script directory to read/write all files to same directory
script_dir = os.path.dirname(os.path.realpath(__file__))
csvfile = os.path.join(script_dir, csvfile)
allfiles = os.path.join(script_dir, allfiles)
eng_file = os.path.join(script_dir, eng_file)

# Step 1 - read the engagement stats
engagement = pd.read_excel(eng_file, sheet_name="Export",
                           usecols=['Title', 'PageViews',
                                            'Url', 'MSAuthor', 'Freshness', 
                                            'LastReviewed', 'Engagement',
                                            'Flags', 'BounceRate', 'ClickThroughRate', 
                                            'CopyTryScrollRate'])

# Step 2 - Get dates from the local repo
# Checkout the branch and pull latest changes if needed...
# h.checkout(repo_path, "main")
# get most recent dates from local repo
dates_df = h.get_filelist(repo_path, "ms.date")
titles_df = h.get_filelist(repo_path, "title")
# description_df = h.get_filelist(repo_path, "description")

# merge the dates and titles
articles = pd.merge(dates_df, titles_df, on='filename')
# now we have updated dates and corresponding titles
print(f" Total articles: {articles.shape[0]}")

# merge in engagement stats
articles = articles.merge(engagement, how='right', left_on='title', right_on='Title')
print(f" After engagement merge, total articles: {articles.shape[0]}")
# note ms.date is coming from the local repo, not the engagements stats.  
# engagement stats can be a month old for items just updated last month
# Convert ms.date to datetime
articles['ms.date'] = pd.to_datetime(articles['ms.date'], errors='coerce')

# Step 3 - find existing work items and merge by title
work_items = q.query_work_items(freshness_title, req)
# fix the titles
work_items = f.fix_work_items(work_items, freshness_title)

print(f"Total work items: {work_items.shape[0]}")
# save work items to csv to figure out what happened...
# work_items.to_csv(os.path.join(script_dir,"work_items.csv"), index=False)

# now merge to articles
articles = articles.merge(work_items, how='left', left_on='Title', right_on='Title')
articles.to_csv(allfiles, index=False)
print(f" saved all articles to {allfiles}")
# filter out ones with a work item already
articles = articles[articles['ID'].isnull()]
print(f"Articles without current work items, before cutoff date: {articles.shape[0]}")
# create work item spreadsheet for cutoff date
articles.to_csv(csvfile, index=False)

cutoff_date = pd.Timestamp(cutoff_date)
print(f"Articles after filtering for cutoff_date of {cutoff_date}: {articles.shape[0]}")
articles.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")