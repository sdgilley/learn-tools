# Freshness tools

This directory contains tools for checking the freshness of the articles in your repository.


## Freshness scripts

Use these scripts to check the freshness of the data in the repository, and to create work items in Azure DevOps for items that need to be updated.
Open each script and fill in the inputs before running.

* `find-stale-items.py`: Finds the list of files that need to be refreshed for either this month or next month. Starts with an engagement report download, but then merges in the most recent dates from your local repository, so you don't recreate work items that were just closed.  Also queries to see if a work item is already present for any remaining items.  Outputs a csv file with the items that need to be created.  It's a good idea to check this file before using the next script to create the items in DevOps.

* `create-work-items.py`: Reads an Excel or csv file and creates a work item in Azure DevOps for each row in the file. One way to use this is to start with an export from the Engagement report, then remove rows that are not needed.  Or, use `find-stale-items.py` which creates a .csv instead.  The following columns are expected in the input file:
    * Url
    * MSAuthor
    * Freshness
    * LastReviewed
    * PageViews
    * Engagement
    * Flags
    * BounceRate
    * ClickThroughRate
    * CopyTryScrollRate

## Functions

You don't need to run these directly, but they are used by the scripts above:

* `fix_items.py`: Function to standardize the text and format in the title to be used prior to a merge.
* `get_filelist.py`: Function to get a list of all files in the local repository. Call with arguments to get the metadata, then merge by the file URL.
* `query_work_items.py`: Function to query the work items in DevOps.  Call with a title string to search for, and a days argument. The days argument is used to remove items that were last touched this many days ago, as it's time to re-do this file again. Returns a pandas dataframe with the results.
* `devops_query.py`: Not used in scripts, but can use stand-alone - add any query specification and any columns to get a devops query result in a dataframe.

## Reference

I developed the `create-work-items.py` script based on the .ps1 file below.  (And by "I", I mean mostly "Copilot".) I'm leaving the script here for reference, but I was unable to use it.  It requires a PAT for DevOps that I couldn't figure out how to create anymore.  Also, I've made lots of little modifications to the Python version.

* `CreateWorkitemsFromExcelFile.ps1`: PowerShell script to create work items in Azure DevOps. Requires a PAT from DevOps.