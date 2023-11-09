'''
This script creates lines to add to the CODEOWNERS file in azureml-examples.
Lines in the resulting file go into CODEOWNERS on the branch corresponding to the 
path_to_root variable in the azure-docs-pr openpublishing.publish.config.json

This script reads the contents of your local azure-docs-pr repo. 
Do a git pull upstream to get the latest changes before running this script.

You'll create a codeowners file for a specific branch in azureml-examples.
Place the contents of the file in the CODEOWNERS file in azureml-examples repo for that branch.
'''

###################### INPUT HERE ############################
# Path to your local repo.  MAKE SURE YOU'RE ON THE BRANCH YOU WANT TO USE. (Usually main)

# Path to your local repo. 
repo_path = 'c:\\GitPrivate\\azure-docs-pr\\articles\\machine-learning'
path_to_root = "azureml-examples-main" # from .openpublishing.publish.config.json in azure-docs-pr
result_fn = f"{path_to_root}-codeowners.txt"
############################ DONE ############################

# open the file to write the results to.
f = open(result_fn, 'w+')

# iterate through the files in the folder.  
import os
import re
import utilities as h

files = os.listdir(repo_path)

# find the file names from the directory.  
for file in files:
    if file.endswith('.md'):
        file_path = os.path.join(repo_path,file)
        lines = h.read_file(file_path)
        for line in lines:
            # snippets have ~\azureml-examples in them.  Find all snippets and write them to the file.
            match_snippet = re.findall(r'\(~\/azureml-examples[^)]*\)|source="~\/azureml-examples[^"]*"', line)
            if match_snippet:
                for match in match_snippet:
                    path, ref_file, branch, match, name = h.cleanup_matches(match)
                    # now put back together and add to file if it's on the path-to-root you specified
                    if branch == path_to_root:
                        # escape spaces in the file name
                        if " " in ref_file:
                            ref_file = ref_file.replace(" ", "\ ")
                        # write to the results file
                        f.write(f"/{ref_file} @sdgilley @msakande @Blackmist @ssalgadodev @lgayhardt @fbsolo-ms1 \n")

# close the txt file.
f.close()

# delete duplicates and sort, write final file
h.remove_duplicates_and_sort(result_fn)
