# GitHub scripts

See [Maintain code snippets in Azure docs](../code-snippets.md) for more information on how to use these scripts.

Scripts in this folder are used to help us maintain our code references.  

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/learn-tools?quickstart=1) 

If running locally instead of Codespaces, make sure you have `pyGithub` installed (`pip install pyGithub`) to run these scripts
  
* [find-snippets.py](find-snippets.py) - use arguments (ai, ml, all) to specify which repo. If no arguments, defaults to all.
    * creates the file refs-found-xx.csv.  This file is used for both the pr-report and merge-report scripts.
    * create a CODEOWNERS file for the specified repo.  Use the content in this file to update the corresponding CODEOWNERS file in the repo.
    * Examples:
        * `python find-snippets.py ai` to find all code snippets in both ai repos: foundry-examples &  azureai-samples repo.
        * `python find-snippets.py ml` to find all code snippets in the azureml-examples repo.
        * `python find-snippets.py all` to find all code snippets in all repos.
* [pr-report.py](pr-report.py) - add argument `ai` to use for foundry-samples instead of azureml-examples. Use this to evaluate whether a PR in azureml-examples/azureai-samples or azure-ai-foundry/foundry-samples will cause problems in our docs build.  If you're using it for the first time in a while, first run [find-sippets.py](find-snippets.py) to get the most recent version of code snippets referenced by azure-ai-docs.
    * Examples:
        * `python pr-report.py 91` to check PR 91 in  azureml-examples repo.
        * `python pr-report.py 169 ai` to check PR 169 in foundry-samples repo. (this should show a comment removed that would break our build)

* [merge-report.py](merge-report.py) - - use arguments (ai, ml, all) to speciy which repo. If no arguments, defaults to all.  Use this to see what PRs in azureml-examples or foundry-examples ave merged in the last N days that might require a docs update (default is 8 days). If you're using it for the first time in a while, first run [find-sippets.py](find-snippets.py) to get the most recent version of code snippets referenced by azure-ai-docs.
    * Examples:
        * `python merge-report.py ml` to check the azureml-examples repo.
        * `python merge-report.py ai` to check the foundry-samples & azureai-samples repos.
        * `python merge-report.py` to check all repos.

The following files provide functions used in the above scripts:

* [utilities.py](utilities.py) - functions used by find-snippets, pr-report, and merge-report
* [auth_request.py](auth.py) - function used by pr-report and merge-report to authenticate to github.
    
    You'll need to set a GH_ACCESS_TOKEN environment variable before using auth_request.py. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens to create a token.  Then add the token to an environment variable called GH_ACCESS_TOKEN.
