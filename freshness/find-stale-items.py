# !IMPORTANT - sign in with az login --use-device-code before running this script
# Finds the list of files that need to be refreshed for either this month or next month.
# creates a csv file with the list of files that need to be refreshed.
import helpers.get_filelist as h
import helpers.fix_titles as f
import helpers.azdo as a
import pandas as pd
import os

################################## inputs
repo_path = "C:/GitPrivate/azure-ai-docs-pr/articles/ai-foundry" # your local repo
offset = 2  # for items going stale next month, use offset = 2. 
            # for this month's items use offset = 1
req = 90 # required freshness in days
suffix = " - Azure AI Foundry" # title suffix for your docs. Crucial for merging correctly.
eng_file = "Feb-Foundry-Engagement.xlsx" # Engagement file to read`
# NOTE: you need to set the Sensitivity label to General on the Excel file!
csvfile = "Apr-foundry-work-items.csv" # This is the file that will be created with the work items

################################## end of inputs

# Calculate the cutoff date - items older than this will be stale
now = pd.Timestamp.now()
end_of_month = now + pd.offsets.MonthEnd(offset)
cutoff_date = end_of_month - pd.Timedelta(days=req)
print(f"Cutoff date: {cutoff_date}")
freshness_title = f"Freshness - over {req}:"  

# suppress future warnings for downcasting
pd.set_option('future.no_silent_downcasting', True)

# get script directory to read/write all files to same directory
script_dir = os.path.dirname(os.path.realpath(__file__))
csvfile = os.path.join(script_dir, csvfile)
eng_file = os.path.join(script_dir, eng_file)

# Step 1 - read the engagement stats
engagement = pd.read_excel(eng_file, sheet_name="Export",
                           usecols=['Title', 'PageViews',
                                            'Url', 'MSAuthor', 'Freshness', 
                                            'LastReviewed', 'Engagement',
                                            'Flags', 'BounceRate', 'ClickThroughRate', 
                                            'CopyTryScrollRate'])



# Step 2 - Get dates from the local repo - this is the most recent date, 
# since engagement is a month old.  Helps to cut out ones already updated.
# Checkout the branch and pull latest changes if needed...
# h.checkout(repo_path, "main")
# get most recent dates from local repo
dates_df = h.get_filelist(repo_path, "ms.date")
titles_df = h.get_filelist(repo_path, "title")
# merge the dates and titles
articles = pd.merge(dates_df, titles_df, on='filename')
# now we have updated dates and corresponding titles
print(f" Total files: {articles.shape[0]}")

# merge in engagement stats
# Make sure titles will match in two dfs
# Make sure titles will match in two dfs
engagement['Title'] = engagement['Title'].apply(lambda x: f.fix_titles(x, suffix))
articles['title'] = articles['title'].apply(lambda x: f.fix_titles(x))


articles = articles.merge(engagement, how='right', left_on='title', right_on='Title')
print(f" After engagement merge, total articles: {articles.shape[0]}")
# note ms.date is coming from the local repo, not the engagements stats.  

# Step 3 - find existing work items and merge by title
print("Starting query for current work items...")
work_items = a.query_freshness(freshness_title, req)
# fix the titles so that they match the metadata from the repo``

work_items['Title'] = work_items['Title'].apply(lambda x:f.fix_titles(x, suffix, freshness_title))

print(f"Total work items: {work_items.shape[0]}")
# DEBUG: save work items to csv to figure out what happened...
work_items.to_csv(os.path.join(script_dir,"debug-work-items.csv"), index=False)
# DEBUG: save work items to csv to figure out what happened...
work_items.to_csv(os.path.join(script_dir,"debug-work-items.csv"), index=False)

# now merge to articles
articles = articles.merge(work_items, how='left', left_on='Title', right_on='Title')
# DEBUG: save all items to csv to figure out what happened...
articles.to_csv(os.path.join(script_dir,"debug-all-files.csv"), index=False)

# DEBUG: save all items to csv to figure out what happened...
articles.to_csv(os.path.join(script_dir,"debug-all-files.csv"), index=False)

# filter out ones with a work item already
articles = articles[articles['Id'].isnull()]
print(f"Articles without current work items, before cutoff date: {articles.shape[0]}")

# Step 4 - filter out articles that are not stale

# Step 4 - filter out articles that are not stale
cutoff_date = pd.Timestamp(cutoff_date)
# if ms.date is missing, use LastReviewed instead
articles['ms.date'] = articles['ms.date'].fillna(articles['LastReviewed']).infer_objects(copy=False)
# Convert ms.date to datetime
articles['ms.date'] = pd.to_datetime(articles['ms.date'], errors='coerce')
# filter out if beyond the cutoff date
articles = articles[articles['ms.date'] < cutoff_date]
print(f"Articles after filtering for cutoff_date of {cutoff_date}: {articles.shape[0]}")
print(f"Articles after filtering for cutoff_date of {cutoff_date}: {articles.shape[0]}")
articles.to_csv(csvfile, index=False)
print(f"Saved to {csvfile}")