![tools](media/toolbox.png) 
# learn-tools

Some handy scripts for working with markdown articles on learn.microsoft.com


##  ![Python](media/python-logo.png) Python scripts:

* [fix-nb.py](fix-nb.py) - Change notebook links and images to markdown syntax. 
* [move-to-v1.py](move-to-v1.py) - Fix links in a file that you're going to move to the v1 folder.

These scripts are used to help us maintain our code references:
* [create-codeowners.py](create-codeowners.py) - create a CODEOWNERS file for the azureml-examples repo.  Use this to generate content to replace the lines in https://github.com/Azure/azureml-examples/blob/main/.github/CODEOWNERS.
  
* [find-sippets.py](find-snippets.py) - Useful for reviewing and summarizing code snippets. Also required to run this before running [pr-report.py](pr-report.py). Reads through your local repo to find instances of code snippets pulled from azureml-examples. Creates a csv file with the following columns:
    * **from_file** - the file in azure-docs-pr that references the snippet
    * **match** - the full text of the code reference.  (i.e., ~/azureml-examples-main/path/filename?name=x)
    * **branch** - the branch of azureml-examples that the snippet is from, using the path_to_root specified in 
    .openpublishing.publish.config.json in our repo (i.e., azureml-examples-main)
    * **path** - path to the file in azureml-examples 
    * **ref_file** - the file where the code is located in azureml-examples
    * **notebook_cell** - if a cell in a notebook, this is the name of the cell.  Otherwise, blank.
* [pr-report.py](pr-report.py) - Use this to evaluate whether a PR in azureml-examples will cause problems in
    our docs build.  Before you use this script, run [find-sippets.py](find-snippets.py) to get the most recent version of code snippets referenced by azure-docs-pr.

The following files provide functions used in the above scripts:

* [utilities.py](utilities.py) - functions used by create-codeowners and pr-report
* [auth_request.py](auth.py) - function used by pr-report to authenticate to github. 
    
    You'll need to set a GH_ACCESS_TOKEN environment variable before using auth-request.py. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens to create a token.  Then add the token to an environment variable called GH_ACCESS_TOKEN.


## Other repos

Also see these repos for other handy tools:

* ![Python](media/python-logo.png) (Python) [Search images](https://github.com/sdgilley/search-images) - find text inside images 
* ![R](media/r-logo.png) (R) [toc-to-csv](https://github.com/sdgilley/toc-to-csv) - convert a markdown table of contents to a csv file 
*  ![R](media/r-logo.png) (R) [MonthlyReport](https://github.com/sdgilley/MonthlyReport) - Summarizes file modification from git logs 