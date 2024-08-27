"""
This script finds PRs that were merged in the last X days (defaults to 8)
and reports on doc files that need updating because of those merges.

Use "ai", "ml", or "fabric" as the argument to specify which repo to check. Default is "ml".
Example:
    python merge-report.py 8 ai

    # these are all equivalent:
    python merge-report.py 8 ml
    python merge-report.py 8
    python merge-report.py
"""


def merge_report(days, service):

    import utilities as h
    import find_pr_files as f

    if service == "ai":
        repo_name = ["rag-data-openai-python-promptflow"]
        owner_name = ["Azure-Samples"]
        # add more here if needed; at that time, will have to loop through the repos
    elif service == "ml":
        repo_name = ["azureml-examples"]
        owner_name = ["Azure"]
    elif service == "fabric":
        repo_name = ["fabric-samples"]
        owner_name = ["Microsoft"]

    # get the refs-found file for this service
    fn = f"refs-found-{service}.csv"
    # read the snippets for this repo
    snippets = h.read_snippets(fn)  # read the snippets file

    # loop through all the repos that contain snippets for this service
    for owner_name, repo_name in zip(owner_name, repo_name):
        f.find_pr_files(owner_name, repo_name, snippets, days)
    return

if __name__ == "__main__":
    
    merge_report(9, "ml")