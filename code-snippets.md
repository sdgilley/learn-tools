# Maintain code snippets in Azure docs

This repository contains scripts to help maintain code snippets in Azure documentation. The scripts are designed to be run in a GitHub Codespace.

If you're evaluating a file for FRESHNESS, see the [Freshness Dashboard](https://sdgilley.github.io/learn-tools/).

## Setup for Codespaces

Use these steps to [create/update a GitHub access token](create-update-auth.md) for use with the scripts in this repo.

Once your secret is stored, perform all maintenance tasks using the button below to open this repo in GitHub Codespaces. No additional setup needed. Use the Codespace terminal to run the scripts.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/learn-tools?quickstart=1)

## Daily tasks

1. Check for [PRs that need approval](https://github.com/Azure/azureml-examples/pulls?q=is%3Apr+is%3Aopen+user-review-requested%3A%40me )

1. (Requires the GH_ACCESS_TOKEN secret) For each PR number that you need to investigate, in the terminal, run:

    ```bash
    python GitHub/pr-report.py <PR number> 
    ```

1. Approve if no issues reported.
1. If issues are present, see [Fix the Problem](fix-the-problem.md)

## Weekly tasks

### Update snippet references and codeowners files

1. Run this script (takes about two minutes):

    ```bash
    python GitHub/find-snippets.py
    ```

1. If changes to .txt and .csv files appear, commit them to this repo (learn-tools). You can do this from a Codespace, but you'll first need to switch to a new branch.
1. If changes to CODEOWNERS appear, commit them to azureml-examples [CODEOWNERS](https://github.com/Azure/azureml-examples/blob/main/.github/CODEOWNERS) file

### Update docs

1. Run the merge report.  If last run 7 days ago, simply run:

    ```bash
    python GitHub/merge-report.py 
    ```

    The report will show PRs merged in the last 8 days.  (The extra day insures that you don't miss a merge that happened after your report 7 days ago.)

1. If longer than 7 days since last run:

    ```bash
    python GitHub/merge-report.py <days>
    ```

1. Modify the files in azure-docs-pr as listed in the report.
1. Copy the report output to your work item.  This will let you see when it was last run, so that you can adjust days accordingly for your next report.  
