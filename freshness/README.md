# Freshness tools

This directory contains tools for checking the freshness of the articles in your repository.

!IMPORTANT - sign in first with `az login --use-device-code` before running these scripts to authenticate with Azure DevOps.


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

* `devops_query.py`: An example of executing a generic DevOps query. Input any query specification and any columns to get a devops query result in a dataframe.
    * Note: This is not used in the other scripts, but is a good example of how to query DevOps using Python.  It uses the `azdo.py` helper function to authenticate and run the query.

## Helper functions

You don't need to run these directly, but they are used by the scripts above.  They are in the **helpers** directory.

* `azdo.py`: Functions to query work items in DevOps. Contains these functions:
    * `authenticate_ado`: Call to get a connection to the database.  This is used by other functions.
    * `query_work_items`: A generic query.  Input the columns you want returned and the query you want to run.  Returns a pandas dataframe with the results.
    * `freshness_query`: A specific query for freshness. Call with a title string to search for, and a days argument. The days argument is used to remove items that were created this many days ago, as it's time to re-do this file again.  Returns a pandas dataframe with the results. (Note: only finds the last year's worth of data, to avoid errors with too many results.)
* `fix_titles.py`: Function to standardize the text and format of titles to be used prior to a merge. Supply the title string to be fixed, the suffix that is added to the title found in the file metadata, and optionally, a prefix.  Both prefix and suffix will be removed from the output title.
* `get_filelist.py`: Function to get a list of all files in the local repository. Call with arguments to get the metadata, then merge by the file URL.


## Reference

I developed the `create-work-items.py` script based on the .ps1 file below.  (And by "I", I mean mostly "Copilot".) I'm leaving the script here for reference, but I was unable to use it.  It requires a PAT for DevOps that I couldn't figure out how to create anymore.  Also, I've made lots of little modifications to the Python version. The Python version works with Entra ID, and does not require a PAT.  

* `CreateWorkitemsFromExcelFile.ps1`: PowerShell script to create work items in Azure DevOps. Requires a PAT from DevOps.