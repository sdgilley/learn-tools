'''
This script creates lines to add to the CODEOWNERS file for the azureml-examples folder.
All files referenced from the main branch will be added to the CODEOWNERS file.
'''

###################### INPUT HERE ############################
# Name the file and the path to your repo.  MAKE SURE YOU'RE ON THE MAIN BRANCH!
repo_path = 'c:\\GitPrivate\\azure-docs-pr\\articles\\machine-learning'
result_fn = "codeowners.txt"
############################ DONE ############################

# Function to delete duplicate rows
def remove_duplicates(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove duplicates by converting the list to a set and back to a list
    lines = list(set(lines))

    with open(file_path, 'w') as f:
        f.writelines(lines)

# open a file to write the results
f = open(result_fn, 'w+')

# iterate through the files in the folder.  
import os
import re
files = os.listdir(repo_path)
for file in files:
    if file.endswith('.md'):
        file_path = os.path.join(repo_path,file)
        # open the file and read through it line by line.
        with open(file_path, 'r') as target_file:
            try: # some of our files contain characters that cause errors.  skip them.
                for line in target_file.readlines():
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
                            if branch == "azureml-examples-main":
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
            except: # record the files that wouldn't open
                # f.write(f"{file}, error\n")
                print(f"error reading {file}")
# close the txt file.
f.close()

# delete duplicates
remove_duplicates(result_fn)
