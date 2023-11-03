'''
This script creates lines to add to the CODEOWNERS file for the azureml-examples folder.
Lines in the resulting file go into CODEOWNERS on the branch corresponding to the 
path_to_root variable in the azure-docs-pr openpublishing.publish.config.json
'''

###################### INPUT HERE ############################
# Path to your local repo.  MAKE SURE YOU'RE ON THE MAIN BRANCH!
repo_path = 'c:\\GitPrivate\\azure-docs-pr\\articles\\machine-learning'
path_to_root = "azureml-examples-main" # from .openpublishing.publish.config.json in azure-docs-pr
result_fn = f"{path_to_root}-codeowners.txt"
############################ DONE ############################

# open the file to write the results to.
f = open(result_fn, 'w+')

# iterate through the files in the folder.  
import os
import re
files = os.listdir(repo_path)

# function to read the file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as target_file:
            lines = target_file.readlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as target_file:
                lines = target_file.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            lines = []
    return lines

# Function to delete duplicate rows
def remove_duplicates(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove duplicates by converting the list to a set and back to a list
    lines = list(set(lines))

    with open(file_path, 'w') as f:
        f.writelines(lines)


# find the file names from the directory.  
for file in files:
    if file.endswith('.md'):
        file_path = os.path.join(repo_path,file)
        lines = read_file(file_path)
        for line in lines:
            # snippets have ~\azureml-examples in them.  Find all snippets and write them to the file.
            match_snippet = re.findall(r'\(~\/azureml-examples[^)]*\)|source="~\/azureml-examples[^"]*"', line)
            if match_snippet:
                for match in match_snippet:
                    match= match.replace('(', '').replace(')', '').replace('"', '').replace(',', '').replace('source=', '')
                    # split up the match into parts here.
                    path = os.path.dirname(match)
                    ref_file = os.path.basename(match)
                    branch = path.split('/')[1]
                    path = path.replace('~', '').replace(branch,'')
                    if "?" in ref_file: #strip out the argument 
                        ref_file = ref_file.split('?'[0])
                    # now put back together and add to file if it's on the main branch
                    if branch == path_to_root:
                        ref_file = f"{path}/{ref_file}"
                        ref_file = ref_file.replace('//', '/')
                        # fix entries like this 
                        # /sdk/python/resources/workspace/['workspace.ipynb', 'name=subscription_id'] mldocs@microsoft.com 
                        if "['" in ref_file:
                            # Remove single quotes and brackets
                            ref_file = ref_file.replace("'", "").replace("[", "").replace("]", "")
                            # Remove everything after the ','
                            ref_file = ref_file.split(',')[0]
                            # (f"REPLACED new string is {ref_file}")
                        # Finally, fix files that have spaces in them
                        if " " in ref_file:
                            ref_file = ref_file.replace(" ", "\ ")
                        # write to the results file
                        f.write(f"{ref_file} @sdgilley @msakande @Blackmist @ssalgadodev @lgayhardt @fbsolo-ms1 \n")

# close the txt file.
f.close()

# delete duplicates
remove_duplicates(result_fn)
