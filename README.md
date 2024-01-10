![tools](media/toolbox.png) 
# learn-tools

Some handy scripts for working with markdown articles on learn.microsoft.com

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/learn-tools?quickstart=1)

##  ![Python](media/python-logo.png) Python scripts:

* [fix-nb.py](fix-nb.py) - Change notebook links and images to markdown syntax. 
* [move-to-v1.py](move-to-v1.py) - Fix links in a file that you're going to move to the v1 folder.
* [include-usage.py](include-usage.py) - Count how many times your include files are used by your documents.

### GitHub folder

Scripts in the GitHub folder are used to help us maintain our code references.  Make sure you have `pyGithub` installed (`pip install pyGithub`) to run these scripts.

* [create-codeowners.py](GitHub/create-codeowners.py) - create a CODEOWNERS file for the azureml-examples repo.  Use this to generate content to replace the lines in https://github.com/Azure/azureml-examples/blob/main/.github/CODEOWNERS.
  
* [find-snippets.py](GitHub/find-snippets.py)
    * creates the file refs-found.csv.  This file is used for both the pr-report and merge-report scripts.
    * create a CODEOWNERS file for the azureml-examples repo.  Use this to generate content to replace the lines in https://github.com/Azure/azureml-examples/blob/main/.github/CODEOWNERS.
* [pr-report.py](GitHub/pr-report.py) - Use this to evaluate whether a PR in azureml-examples will cause problems in
    our docs build.  If you're using it for the first time in a while, first run [find-sippets.py](find-snippets.py) to get the most recent version of code snippets referenced by azure-docs.
* [merge-report.py](GitHub/merge-report.py) - Use this to see what PRs in azureml-examples have merged 
    in the last N days that might require a docs update (default is 7 days). If you're using it for the first time in a while, first run[find-sippets.py](find-snippets.py) to get the most recent version of code snippets referenced by azure-docs.

The following files provide functions used in the above scripts:

* [utilities.py](GitHub/utilities.py) - functions used by find-snippets, pr-report, and merge-report
* [auth_request.py](GitHub/auth.py) - function used by pr-report and merge-report to authenticate to github.
    
    You'll need to set a GH_ACCESS_TOKEN environment variable before using auth-request.py. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens to create a token.  Then add the token to an environment variable called GH_ACCESS_TOKEN.


## Other repos

Also see these repos for other handy tools:

* ![Python](media/python-logo.png) (Python) [Search images](https://github.com/sdgilley/search-images) - find text inside images 
* ![R](media/r-logo.png) (R) [toc-to-csv](https://github.com/sdgilley/toc-to-csv) - convert a markdown table of contents to a csv file 
*  ![R](media/r-logo.png) (R) [MonthlyReport](https://github.com/sdgilley/MonthlyReport) - Summarizes file modification from git logs 
