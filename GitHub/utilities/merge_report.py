"""
This script finds PRs that were merged in the last X days (defaults to 8)
and reports on doc files that need updating because of those merges.

Use "ai", ai2, "ml", or  as the argument to specify which repo to check. Default is "ml".
Example:
    python merge-report.py 8 ai

    # these are all equivalent:
    python merge-report.py 8 ml
    python merge-report.py 8
    python merge-report.py
"""


def merge_report(days, service):

    from utilities import helpers as h
    from utilities import find_pr_files as f
    import os

    if service == "ai":
        repo_name = ["azureai-samples", "foundry-samples"]
        owner_name = ["Azure-Samples", "azure-ai-foundry"]
        # add more here if needed; at that time, will have to loop through the repos
    elif service == "ml":
        repo_name = ["azureml-examples"]
        owner_name = ["Azure"]


    mydir = os.path.abspath(__file__)
    # loop through all the repos that contain snippets for this service
    for owner_name, repo_name in zip(owner_name, repo_name):
        # get the refs-found file for this service
        fn = os.path.join(os.path.dirname(os.path.dirname(mydir)), f"refs-found-{repo_name}.csv")
        # print(f"Reading {fn} for {repo_name} snippets")
        # read the snippets for this repo
        snippets = h.read_snippets(fn)  # read the snippets file
        f.find_pr_files(owner_name, repo_name, snippets, days)
    return

if __name__ == "__main__":
    
    merge_report(9, "ai")